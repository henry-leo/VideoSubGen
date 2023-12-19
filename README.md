# Video Subtitle Generator (VideoSubGen)

Hello there! This is a tool to help you with your generate and translate the subtitles for your videos.
Basically, the tool is connected to the Google Translate API and faster-whisper to work with the video.

Ps: I just made the IO in these projects, the main code is from the Whisper-faster, and Google Translate API.

## Installation

```bash
git clone https://github.com/henry-leo/VideoSubGen.git

pip install -r requirements.txt
```

## Quick Start

```python
from faster_whisper import WhisperModel

from video_sub_gen.io import VideoSubGen
from video_sub_gen.translator import Google

# write your config here
model_size = 'base'  # 'tiny', 'base', 'small', 'medium', 'large'
video = ''
source_lang = 'en'  # 'en', 'ja', 'zh'
target_lang = 'zh'
output = ''
proxies = {'https': '',
           'http': ''}

# get segments from whisper-fast
model = WhisperModel(model_size, device='cuda', compute_type='float32')
segments, info = model.transcribe(video, language=source_lang, vad_filter=True)

# implement translator
translator = Google(source_lang, 'zh', proxies=proxies)

# do the job
gen = VideoSubGen(segments, translator)
gen.run(output=output)
```

## Acknowledgement

- [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
- [bilingual_book_maker](https://github.com/yihong0618/bilingual_book_maker)