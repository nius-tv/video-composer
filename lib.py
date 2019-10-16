import subprocess

from config import *


def add_audio_to_video(audio_file_path, video_file_path, output_file_path):
	cmd = 'ffmpeg \
		-y \
		-i {audio_file_path} \
		-i {video_file_path} \
		-c:a {audio_codec} \
		-c:v {video_codec} \
		-pix_fmt {pixel_fmt} \
		{output_file_path}'.format(
			audio_file_path=audio_file_path,
			video_file_path=video_file_path,
			audio_codec=AUDIO_CODEC,
			video_codec=VIDEO_CODEC,
			pixel_fmt=PIXEL_FMT,
			output_file_path=output_file_path)
	subprocess.call(['bash', '-c', cmd])


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


def get_tmp_file_path(file_path):
	filename = file_path.split('/')[-1]
	filename = 'tmp-{}'.format(filename)
	return '{}/{}'.format(TMP_DIR_PATH, filename)
