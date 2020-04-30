import subprocess

from config import *
from google.cloud import error_reporting
from utils import *


if __name__ == '__main__':
	error_client = error_reporting.Client()
	try:
		story = load_story()
		duration = get_duration(STORY_VIDEO_FILE_PATH)
		cmd = 'ffmpeg \
			-y \
			-i {video_file_path} \
			-i {background_file_path} \
			-filter_complex " \
				[0:v]colorkey={color}:{chroma}:{overlay}[v0]; \
				[1:v][v0]overlay[v1]" \
			-map [v1] \
			-map 0:a \
			-ss 0 \
			-to {duration} \
			-c:a {audio_codec} \
			-c:v {video_codec} \
			-pix_fmt {pixel_fmt} \
			{output_file_path}'.format(
				video_file_path=STORY_VIDEO_FILE_PATH,
				background_file_path=story['library']['presenterBgVideoFilePath'],
				color=story['chromaColor'],
				chroma=CHROMA_SENSITIVITY,
				overlay=CHROMA_OVERLAY,
				duration=duration,
				audio_codec=AUDIO_CODEC,
				video_codec=VIDEO_CODEC,
				pixel_fmt=PIXEL_FMT,
				output_file_path=STORY_VIDEO_WITH_PRESENTER_BG_FILE_PATH)
		subprocess.call(['bash', '-c', cmd])
	except Exception:
		error_client.report_exception()
		raise
