import subprocess

from config import *


def get_tmp_file_path(file_path):
	filename = file_path.split('/')[-1]
	filename = 'tmp-{}'.format(filename)
	return '{}/{}'.format(TMP_DIR_PATH, filename)


def cut_video(input_file_path, output_file_path, duration):
	cmd = 'ffmpeg \
		-y \
		-i {input_file_path} \
		-ss 0 \
		-to {duration} \
		-c:v {video_codec} \
		-pix_fmt {pixel_fmt} \
		{output_file_path}'.format(
			input_file_path=input_file_path,
			duration=duration,
			video_codec=VIDEO_CODEC,
			pixel_fmt=PIXEL_FMT,
			output_file_path=output_file_path)
	subprocess.call(['bash', '-c', cmd])
