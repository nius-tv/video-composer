import random
import subprocess
import yaml

from config import *
from PIL import Image
from shutil import copyfile
from utils import *


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


def create_transitions(transition_file_path, mid_offset, video_file_paths):
	output_file_paths = []
	last_i = len(video_file_paths)

	for i, video_file_path in enumerate(video_file_paths):
		if not i == 0 and not i == last_i and not TRANSITIONS_BETWEEN_IMAGES_ANIMATION:
			continue
		if i == last_i and not TRANSITIONS_END_ANIMATION:
			continue

		image_start = float(transitions_start) - float(mid_offset) + float(IMAGE_DURATION * i)
		if image_start < 0:
			continue

		generate_offset_video(duration=image_start)

		if not i == 0 or TRANSITIONS_START_ANIMATION:
			concat_file_paths = (
				OFFSET_VIDEO_FILE_PATH,
				transition_file_path
			)
		else:
			concat_file_paths = (OFFSET_VIDEO_FILE_PATH,)

		filename = video_file_path.split('/')[-1]
		filename = filename.split('.')[0]
		output_file_path = '{}/{}-transition.{}'.format(STORY_DIR_PATH, filename, VIDEO_FMT)
		output_file_paths.append(output_file_path)

		concat_videos(concat_file_paths, output_file_path)

	return output_file_paths


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


def images_to_videos(images):
	output_file_paths = []

	for i, image_name in enumerate(images):
		if not image_name == TRANSPARENT_IMAGE_FILE_PATH:
			input_file_path = '{}/{}'.format(STORY_DIR_PATH, image_name)
		else:
			input_file_path = image_name

		filename = image_name.split('/')[-1]
		filename = filename.split('.')[0]
		output_file_path = '{}/{}-image.{}'.format(STORY_DIR_PATH, filename, VIDEO_FMT)
		output_file_paths.append(output_file_path)

		image_to_video(input_file_path, output_file_path)

	return output_file_paths


def load_transitions():
	with open(TRANSITION_FILE_PATH) as f:
		data = f.read()
	return yaml.load(data, Loader=yaml.FullLoader)


if __name__ == '__main__':
	story = load_story()
	transitions = load_transitions()
	# Create transparent image
	img = Image.new('RGBA', VIDEO_SIZE, (0, 0, 0, 0))
	img.save(TRANSPARENT_IMAGE_FILE_PATH)
	# Generate initial transparent video
	transitions_start = story['transitions']['start']
	if transitions_start > 0:
		image_to_video(TRANSPARENT_IMAGE_FILE_PATH,
					   TRANSPARENT_VIDEO_FILE_PATH,
					   TRANSPARENT_VIDEO_DURATION)
		# Generate offset video with audio from transparent video
		generate_offset_video(transitions_start)
	# Generate videos from story images
	num_images = story['transitions']['numImages']
	images = story['images'][0:num_images]
	assert num_images == len(images)

	images.append(TRANSPARENT_IMAGE_FILE_PATH) # avoid last image from "sticking"
	video_file_paths = images_to_videos(images)

	if transitions_start > 0:
		concat_file_paths = [OFFSET_VIDEO_FILE_PATH]
		concat_file_paths.extend(video_file_paths)
		concat_videos(concat_file_paths, IMAGES_VIDEO_FILE_PATH)
	else:
		concat_videos(video_file_paths, IMAGES_VIDEO_FILE_PATH)
	# Generate transitions
	default_transition = transitions[TRANSITION_ID]
	animation_filename = default_transition['name']
	animation_file_path = '{}/{}'.format(TRANSITIONS_LIBRARY_DIR_PATH, animation_filename)
	mid_offset = default_transition['mid']
	transition_file_paths = create_transitions(animation_file_path,
											   mid_offset,
											   video_file_paths)
	# Combine transitions into one
	num_transitions = len(transition_file_paths)
	if num_transitions > 1:
		overlay_videos(transition_file_paths, TRANSITIONS_FILE_PATH)
	elif num_transitions == 1:
		copyfile(transition_file_paths[0], TRANSITIONS_FILE_PATH)
	# Combine images with transitions
	if num_transitions > 0:
		video_file_paths = (
			IMAGES_VIDEO_FILE_PATH,
			TRANSITIONS_FILE_PATH
		)
		overlay_videos(video_file_paths, IMAGES_TRANSITIONS_FILE_PATH)
	else:
		copyfile(IMAGES_VIDEO_FILE_PATH, IMAGES_TRANSITIONS_FILE_PATH)
	# Combine images with transition with story video
	video_file_paths = (
		STORY_WITH_BACKGROUND_VIDEO_FILE_PATH,
		IMAGES_TRANSITIONS_FILE_PATH
	)
	overlay_videos(video_file_paths, COMPOSED_VIDEO_FILE_PATH)
