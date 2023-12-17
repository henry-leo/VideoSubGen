import time


def convert_seconds_to_timeframe(seconds):
    """Converts seconds to time frame.
    Args:
      seconds: time in seconds.
    Returns:
      str, converted time string.
    """
    # convert seconds to struct_time
    time_struct = time.gmtime(seconds)
    # get time components
    h = time_struct.tm_hour
    m = time_struct.tm_min
    s = time_struct.tm_sec
    ms = int((seconds - int(seconds)) * 1000)
    # format time string
    time_string = "{:02d}:{:02d}:{:02d},{:03d}".format(h, m, s, ms)

    return time_string


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
