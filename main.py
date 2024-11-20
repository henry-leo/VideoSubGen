from faster_whisper import WhisperModel

from video_sub_gen.io import VideoSubGen
from video_sub_gen.translator import Google

# write your config here

# 'tiny', 'base', 'small', 'medium', 'large'
# or 'mlx-community/whisper-tiny-mlx-q4', 'mlx-community/whisper-large-v3-mlx'
model_size = 'base'
video = ''
source_lang = 'en'  # 'en', 'ja', 'zh'
target_lang = 'zh'
output = ''
proxies = {'https': '',
           'http': ''}

# get segments from whisper-fast
model = WhisperModel(model_size, device='cuda', compute_type='float32')
segments, info = model.transcribe(video, language=source_lang, vad_filter=True)
# get segments for mlx-whisper
# import mlx_whisper
# segments = mlx_whisper.transcribe(
#     video,
#     path_or_hf_repo=model_size,
#     verbose=False,
#     word_timestamps=True)['segments']

# implement translator
translator = Google(source_lang, 'zh', proxies=proxies)

# do the job
gen = VideoSubGen(segments, translator)
gen.run(output=output)
