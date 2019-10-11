import random
import subprocess
import yaml

from config import *
from PIL import Image


def concat_videos(video_file_paths, output_file_path):
	inputs, filters = generate_inputs_and_filters(video_file_paths)
	cmd = 'ffmpeg \
		-y \
		{inputs} \
		-filter_complex "{filters}concat=n={num_videos}:v=1:a=0[v]" \
		-map [v] \
		-c:v {video_codec} \
		-pix_fmt {pixel_fmt} \
		{output_file_path}'.format(
			inputs=' '.join(inputs),
			filters=''.join(filters),
			num_videos=len(filters),
			video_codec=VIDEO_CODEC,
			pixel_fmt=PIXEL_FMT,
			output_file_path=output_file_path)
	subprocess.call(['bash', '-c', cmd])


def create_transitions(transitions_start, transition_file_path, mid_offset, video_file_paths):
	output_file_paths = []
	concat_file_paths = (
		GEN_TRANSPARENT_FILE_PATH,
		transition_file_path
	)

	for i, video_file_path in enumerate(video_file_paths):
		image_start = float(transitions_start) - float(mid_offset) + float(IMAGE_DURATION * i)
		generate_offset(duration=image_start)

		filename = video_file_path.split('/')[-1].split('.')[0]
		output_file_path = '{}/tmp/{}-transition.mov'.format(ASSETS_DIR_PATH, filename)
		output_file_paths.append(output_file_path)

		concat_videos(concat_file_paths, output_file_path)

	return output_file_paths


def generate_inputs_and_filters(video_file_paths):
	inputs = []
	filters = []

	for i, video_file_path in enumerate(video_file_paths):
		cmd = '-i {}'.format(video_file_path)
		inputs.append(cmd)

		cmd = '[{}:v]'.format(i)
		filters.append(cmd)

	return inputs, filters


def generate_offset(duration):
	cmd = 'ffmpeg \
		-y \
		-i {input_file_path} \
		-ss 0 \
		-to {duration} \
		-c:v {video_codec} \
		-pix_fmt {pixel_fmt} \
		{output_file_path}'.format(
			input_file_path=TRANSPARENT_FILE_PATH,
			duration=duration,
			video_codec=VIDEO_CODEC,
			pixel_fmt=PIXEL_FMT,
			output_file_path=GEN_TRANSPARENT_FILE_PATH)
	subprocess.call(['bash', '-c', cmd])


def get_formulas():
	if random.randrange(2) == 0:
		formulas_x = ['t*(in_w-out_w)', '(in_w-out_w)-t*(in_w-out_w)']
		formulas_y = [0]
	else:
		formulas_x = [0]
		formulas_y = ['t*(in_h-out_h)', '(in_h-out_h)-t*(in_h-out_h)']

	return formulas_x, formulas_y


def image_to_video(image_file_path, output_file_path):
	image = Image.open(image_file_path)
	formulas = get_formulas()
	cmd = 'ffmpeg \
		-y \
		-loop 1 \
		-i {image_file_path} \
		-t {duration} \
		-c:v {video_codec} \
		-pix_fmt {pixel_fmt} \
		{output_file_path}'.format(
			image_file_path=image_file_path,
			duration=IMAGE_DURATION,
			fps=FPS,
			image_width=image.size[0],
			image_height=image.size[1],
			video_width=VIDEO_SIZE[0],
			video_height=VIDEO_SIZE[1],
			f_x=random.choice(formulas[0]),
			f_y=random.choice(formulas[1]),
			video_codec=VIDEO_CODEC,
			pixel_fmt=PIXEL_FMT,
			output_file_path=output_file_path)
	subprocess.call(['bash', '-c', cmd])


def images_to_videos(images):
	output_file_paths = []

	for i, image_name in enumerate(images):
		input_file_path = '{}/{}'.format(ASSETS_DIR_PATH, image_name)
		filename = image_name.split('.')[0]
		output_file_path = '{}/tmp/{}-image.{}'.format(ASSETS_DIR_PATH, filename, VIDEO_FMT)
		output_file_paths.append(output_file_path)

		image_to_video(input_file_path, output_file_path)

	return output_file_paths


def load_story():
	with open(STORY_FILE_PATH) as f:
		data = f.read()
	return yaml.load(data, Loader=yaml.FullLoader)


def load_transitions():
	with open(TRANSITION_FILE_PATH) as f:
		data = f.read()
	return yaml.load(data, Loader=yaml.FullLoader)


def overlay_videos(video_file_paths, output_file_path):
	inputs, filters = generate_inputs_and_filters(video_file_paths)
	cmd = 'ffmpeg \
		-y \
		{inputs} \
		-filter_complex "{filters}overlay[v]" \
		-map [v] \
		-c:v {video_codec} \
		-pix_fmt {pixel_fmt} \
		{output_file_path}'.format(
			inputs=' '.join(inputs),
			filters=''.join(filters),
			video_codec=VIDEO_CODEC,
			pixel_fmt=PIXEL_FMT,
			output_file_path=output_file_path)
	subprocess.call(['bash', '-c', cmd])


if __name__ == '__main__':
	story = load_story()
	transitions = load_transitions()

	transitions_start = story['transitions']['start']
	generate_offset(transitions_start)

	images = story['transitions']['images']
	video_file_paths = images_to_videos(images)

	concat_file_paths = [GEN_TRANSPARENT_FILE_PATH]
	concat_file_paths.extend(video_file_paths)
	concat_videos(concat_file_paths, IMAGES_VIDEO_FILE_PATH)

	default_transition = transitions[TRANSITION_ID]
	animation_filename = default_transition['name']
	animation_file_path = '{}/{}'.format(TRANSITIONS_LIBRARY_DIR_PATH, animation_filename)
	mid_offset = default_transition['mid']
	transition_file_paths = create_transitions(transitions_start,
											   animation_file_path,
											   mid_offset,
											   video_file_paths)

	overlay_videos(transition_file_paths, TRANSITIONS_FILE_PATH)

	video_file_paths = [
		IMAGES_VIDEO_FILE_PATH,
		TRANSITIONS_FILE_PATH
	]
	overlay_videos(video_file_paths, IMAGES_TRANSITIONS_FILE_PATH)

	video_file_paths = [
		VIDEO_FILE_PATH,
		IMAGES_TRANSITIONS_FILE_PATH
	]
	overlay_videos(video_file_paths, FINAL_VIDEO_FILE_PATH)
