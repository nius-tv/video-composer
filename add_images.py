import random
import subprocess
import yaml

from config import *
from lib import *
from PIL import Image
from shutil import copyfile


def concat_videos(video_file_paths, output_file_path):
	inputs, filters = compute_inputs_and_filters(video_file_paths)
	cmd = 'ffmpeg \
		-y \
		{inputs} \
		-filter_complex "{filters}concat=n={num_videos}:v=1:a=1:unsafe=1[v][a]" \
		-map [a] \
		-map [v] \
		-c:a {audio_codec} \
		-c:v {video_codec} \
		-pix_fmt {pixel_fmt} \
		{output_file_path}'.format(
			inputs=' '.join(inputs),
			filters=''.join(filters),
			num_videos=len(video_file_paths),
			audio_codec=AUDIO_CODEC,
			video_codec=VIDEO_CODEC,
			pixel_fmt=PIXEL_FMT,
			output_file_path=output_file_path)
	subprocess.call(['bash', '-c', cmd])


def generate_offset_video(duration):
	tmp_output_file_path = get_tmp_file_path(OFFSET_VIDEO_FILE_PATH)
	cut_video(TRANSPARENT_VIDEO_FILE_PATH, tmp_output_file_path, duration)
	generate_silence_audio(duration)
	add_audio_to_video(SILENCE_AUDIO_FILE_PATH,
					   tmp_output_file_path,
					   OFFSET_VIDEO_FILE_PATH)


def get_formulas():
	if random.randrange(2) == 0:
		return (
			'x=t*(in_w-out_w)/{}'.format(IMAGE_ANIMATION_SPEED_X),
			'x=(in_w-out_w)-t*(in_w-out_w)/{}'.format(IMAGE_ANIMATION_SPEED_X)
		)
	else:
		return (
			'y=t*(in_h-out_h)/{}'.format(IMAGE_ANIMATION_SPEED_Y),
			'y=(in_h-out_h)-t*(in_h-out_h)/{}'.format(IMAGE_ANIMATION_SPEED_Y)
		)


def image_to_video(image_file_path, output_file_path, duration=IMAGE_DURATION):
	tmp_output_file_path = get_tmp_file_path(output_file_path)
	image = Image.open(image_file_path)
	formulas = get_formulas()
	cmd = 'ffmpeg \
		-y \
		-loop 1 \
		-i {image_file_path} \
		-t {duration} \
		-filter_complex " \
			fps={fps}, \
			scale=w={image_width}:h={image_height}, \
			crop=w={video_width}:h={video_height}:{xy}" \
		-c:v {video_codec} \
		-pix_fmt {pixel_fmt} \
		{output_file_path}'.format(
			image_file_path=image_file_path,
			duration=duration,
			fps=FPS,
			image_width=image.size[0],
			image_height=image.size[1],
			video_width=VIDEO_SIZE[0],
			video_height=VIDEO_SIZE[1],
			xy=random.choice(formulas),
			video_codec=VIDEO_CODEC,
			pixel_fmt=PIXEL_FMT,
			output_file_path=tmp_output_file_path)
	subprocess.call(['bash', '-c', cmd])

	generate_silence_audio(duration)
	add_audio_to_video(SILENCE_AUDIO_FILE_PATH,
					   tmp_output_file_path,
					   output_file_path)


def load_story():
	with open(STORY_FILE_PATH) as f:
		data = f.read()
	return yaml.load(data, Loader=yaml.FullLoader)


def load_transitions():
	with open(TRANSITION_FILE_PATH) as f:
		data = f.read()
	return yaml.load(data, Loader=yaml.FullLoader)


