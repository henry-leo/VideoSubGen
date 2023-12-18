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
