import subprocess

from config import *


if __name__ == '__main__':
	cmd = 'ffmpeg \
		-y \
		-i {video_file_path} \
		-i {background_file_path} \
		-filter_complex " \
			[0:v]colorkey=green:{chroma}:{overlay}[v0]; \
			[1:v][v0]overlay[v1]" \
		-map [v1] \
		-map 0:a \
		-c:a {audio_codec} \
		-c:v {video_codec} \
		-pix_fmt {pixel_fmt} \
		-shortest \
		{output_file_path}'.format(
			video_file_path=STORY_VIDEO_FILE_PATH,
			background_file_path=PRESENTER_BACKGROUND_VIDEO_FILE_PATH,
			chroma=CHROMA_SENSITIVITY,
			overlay=CHROMA_OVERLAY,
			audio_codec=AUDIO_CODEC,
			video_codec=VIDEO_CODEC,
			pixel_fmt=PIXEL_FMT,
			output_file_path=STORY_VIDEO_WITH_PRESENTER_BG_FILE_PATH)
	subprocess.call(['bash', '-c', cmd])
