import json
import subprocess

from config import *


def compute_audio_maps(indexes):
	file_paths = []
	maps = []

	for index in indexes:
		file_path = '{story_dir_path}/audio-track{index}.{audio_fmt}'.format(
			story_dir_path=STORY_DIR_PATH,
			index=index,
			audio_fmt=AUDIO_FMT)
		file_paths.append(file_path)

		cmd = '-map 0:a:{index} \
			-c:a {audio_codec} \
			-ar {sample_rate} \
			{file_path}'.format(
				index=index,
				audio_codec=AUDIO_CODEC,
				sample_rate=AUDIO_SAMPLE_RATE,
				file_path=file_path)
		maps.append(cmd)

	return file_paths, maps


def extract_audio_and_video(audio_maps):
	cmd = 'ffmpeg \
		-y \
		-i {input_file_path} \
		-map 0:v:0 \
		-c:v {video_codec} \
		-pix_fmt {pixel_fmt} \
		{output_file_path}'.format(
			input_file_path=STORY_VIDEO_WITH_CATEGORY_FILE_PATH,
			video_codec=VIDEO_CODEC,
			pixel_fmt=PIXEL_FMT,
			output_file_path=NORMALIZED_STORY_VIDEO_NO_AUDIO_FILE_PATH)
	tmp_audio_maps = ' '.join(audio_maps)
	cmd = '{} {}'.format(cmd, tmp_audio_maps)
	subprocess.call(['bash', '-c', cmd])


def get_audio_indexes():
	cmd = 'ffprobe \
		-loglevel quiet \
		-select_streams a \
		-show_entries stream \
		-print_format json \
		{}'.format(STORY_VIDEO_WITH_CATEGORY_FILE_PATH)
	data = subprocess.check_output(['bash', '-c', cmd])
	data = data.decode('utf-8') # binary to utf-8 string
	data = json.loads(data)

	ids = []
	for stream in data['streams']:
		ids.append(stream['index'])
	return ids


def merge_audios(file_paths):
	tmp_file_paths = ' '.join(file_paths)
	cmd = 'sox -m {} {}'.format(tmp_file_paths, AUDIO_TRACKS_FILE_PATH)
	subprocess.call(['bash', '-c', cmd])


def merge_audio_and_video():
	cmd = 'ffmpeg \
		-y \
		-i {audio_file_path} \
		-i {video_file_path} \
		-c:a {audio_codec} \
		-c:v {video_codec} \
		-pix_fmt {pixel_fmt} \
		{output_file_path}'.format(
			audio_file_path=AUDIO_TRACKS_FILE_PATH,
			video_file_path=NORMALIZED_STORY_VIDEO_NO_AUDIO_FILE_PATH,
			audio_codec=AUDIO_CODEC,
			video_codec=VIDEO_CODEC,
			pixel_fmt=PIXEL_FMT,
			output_file_path=NORMALIZED_STORY_VIDEO_FILE_PATH)
	subprocess.call(['bash', '-c', cmd])


if __name__ == '__main__':
	indexes = get_audio_indexes()
	audio_file_paths, audio_maps = compute_audio_maps(indexes)
	extract_audio_and_video(audio_maps)
	merge_audios(audio_file_paths)
	merge_audio_and_video()
