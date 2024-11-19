from typing import Optional, Iterable, List, Dict, Generator

import tqdm
from faster_whisper.transcribe import Segment

from video_sub_gen.translator import Google
from video_sub_gen.utils import convert_seconds_to_timeframe


def read_srt(srt_path):
    """Reads srt file and returns a list of subtitles.

    Args:
      srt_path: str, path to srt file.

    Returns:
      list, list of subtitles.
    """
    # read srt file
    with open(srt_path, 'r', encoding='utf-8') as f:
        srt = f.readlines()

    # remove new line characters
    srt = [line.strip() for line in srt]

    # remove empty lines
    srt = [line for line in srt if line]

    # get indexes of subtitles
    indexes = [i for i, line in enumerate(srt) if line.isdigit()]

    # get subtitles
    subtitles = []
    for i in range(len(indexes)):
        # get subtitle index
        index = indexes[i]
        # get subtitle time frame
        time_frame = srt[index + 1]
        # get subtitle text
        text = srt[index + 2]
        # create subtitle
        subtitle = {"index": i + 1, "time_frame": time_frame, "text": text}
        # append subtitle to subtitles
        subtitles.append(subtitle)

    return subtitles


def rewrite_srt(srt_path: str, subtitles: list) -> None:
    """Rewrites srt file.

    Args:
      srt_path: str, path to srt file.
      subtitles: list, list of subtitles.
    """
    # open srt file
    with open(srt_path, 'w', encoding='utf-8') as f:
        # iterate over subtitles
        for subtitle in subtitles:
            # get subtitle index
            index = subtitle["index"]
            # get subtitle time frame
            time_frame = subtitle["time_frame"]
            # get subtitle text
            text = subtitle["text"]
            # write subtitle to file
            f.write(str(index) + "\n")
            f.write(time_frame + "\n")
            f.write(text + "\n\n")


def write_srt_from_segments(
    srt_path: str,
    segments: Iterable[Segment] | List[Dict[str, str | int | list]],
    verbose: Optional[bool] = False,
    mode: str = 'faster-whisper'
) -> None:
    """Writes srt file from segments.

    Args:
        srt_path: str, output srt file path.
        segments: iter, segments from whisper-fast.
        verbose: bool, verbose mode, print subtitles, default False.
        mode: str, the typy of whisper
    """
    with open(srt_path, 'w', encoding='utf-8') as f:
        f.write('')

    if mode == 'faster-whisper':
        process_func = parse_segment_from_whisper_fast
    elif mode == 'mlx-whisper':
        process_func = parse_segment_from_mlx_whisper
    else:
        raise NotImplementedError

    n = 0
    if verbose:
        for segment in segments:
            n += 1
            word = process_func(segment, n)
            with open(srt_path, 'a', encoding='utf-8') as f:
                f.write(word)
            print(word)
    else:
        with tqdm.tqdm(segments, desc='Generating subtitles', unit='segments') as pbar:
            for segment in pbar:
                n += 1
                word = process_func(segment, n)
                with open(srt_path, 'a', encoding='utf-8') as f:
                    f.write(word)


def parse_segment_from_whisper_fast(segment: Segment, subtitle_index: int) -> str:
    """Parses faster-whisper segment and returns a subtitle.

    Args:
      segment: dict, segment.
      subtitle_index: int, subtitle index.

    Returns:
      dict, subtitle.
    """
    # get segment start time
    start = convert_seconds_to_timeframe(segment.start)
    # get segment end time
    end = convert_seconds_to_timeframe(segment.end)
    # create subtitle
    word = (f'{subtitle_index}\n'
            f'{start} --> {end}\n'
            f'{segment.text}\n\n')

    return word


def parse_segment_from_mlx_whisper(segment: Dict[str, str | int | list], subtitle_index: int) -> str:
    """Parses mlx-whisper segment and returns a subtitle.

    Args:
        segment: Dict[str, str | int | list], mlx-whisper segment
        subtitle_index: int, subtitle index

    Returns:
        str, subtitle
    """
    # get segment start time
    start = convert_seconds_to_timeframe(segment['start'])
    # get segment end time
    end = convert_seconds_to_timeframe(segment['end'])

    text = segment['text']
    # create subtitle
    word = (f'{subtitle_index}\n'
            f'{start} --> {end}\n'
            f'{text}\n\n')

    return word


class VideoSubGen:
    def __init__(
        self,
        segments: Iterable[Segment] | List[Dict[str, str | int | list]],
        translator: Google
    ):
        self.segments = segments
        self.translator = translator

    def run(self, output: str, translate_frame: int = 50) -> None:
        """Main function of the VideoSubGen

        Args:
            output: str, output srt file path.
            translate_frame: int, the number of subtitles to translate at a time.
        """
        # generate native subtitles from whisper-fast and save it to srt file
        if isinstance(self.segments, Generator):
            write_srt_from_segments(output, self.segments)
        elif isinstance(self.segments, list):
            write_srt_from_segments(output, self.segments, mode='mlx-whisper')
        else:
            raise TypeError

        # read srt file
        srt = read_srt(output)

        # translate the subtitles with Translator
        srt = self._run_translate(srt, translate_frame)

        # rewrite srt file with translated subtitles
        rewrite_srt(output, srt)

    def _run_translate(self, srt: list, translate_frame: int = 50):
        """

        Args:
            srt: list, list of parsed subtitles.
            translate_frame: int, the number of subtitles to translate at a time.

        Returns:
            list, list of translated subtitles.
        """
        translate_collection = []
        with tqdm.tqdm(srt, desc='Translating', unit='segments') as pbar:
            for i in pbar:
                translate_collection.append(i['text'])
                translate_text = '\n'.join(translate_collection)
                if len(translate_collection) == translate_frame:
                    translate_text = self.translator.translate(translate_text)
                    translate_collection = []
                    for j in range(0, translate_frame):
                        srt[i['index'] - j - 1]['text'] = translate_text.split('\n')[translate_frame - j - 1]
                elif len(translate_text) > 2000:
                    translate_text = self.translator.translate(translate_text)
                    translate_collection = []
                    for j in range(0, len(translate_text.split('\n'))):
                        srt[i['index'] - j - 1]['text'] = \
                            translate_text.split('\n')[len(translate_text.split('\n')) - j - 1]

        if translate_collection:
            translate_text = '\n'.join(translate_collection)
            translate_text = self.translator.translate(translate_text)
            for j in range(0, len(translate_collection)):
                srt[len(srt) - j - 1]['text'] = translate_text.split('\n')[len(translate_collection) - j - 1]

        return srt
