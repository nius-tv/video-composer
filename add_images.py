import random
import subprocess
import yaml

from config import *
from PIL import Image
from shutil import copyfile


def add_silence_to_video(input_file_path, output_file_path):
	cmd = 'ffmpeg \
		-y \
		-i {audio_file_path} \
		-i {video_file_path} \
		-c:a {audio_codec} \
		-c:v {video_codec} \
		-pix_fmt {pixel_fmt} \
		{output_file_path}'.format(
			audio_file_path=SILENCE_AUDIO_FILE_PATH,
			video_file_path=input_file_path,
			audio_codec=AUDIO_CODEC,
			video_codec=VIDEO_CODEC,
			pixel_fmt=PIXEL_FMT,
			output_file_path=output_file_path)
	subprocess.call(['bash', '-c', cmd])


def compute_audio_maps(num_videos):
	maps = []
	
	for i in range(num_videos):
		audio_map = '-map {}:a'.format(i)
		maps.append(audio_map)

	return maps


def compute_inputs_and_filters(video_file_paths, with_audio=True):
	inputs = []
	filters = []

	for i, video_file_path in enumerate(video_file_paths):
		cmd = '-i {}'.format(video_file_path)
		inputs.append(cmd)

		if with_audio:
			cmd = '[{i}:v][{i}:a]'.format(i=i)
		else:
			cmd = '[{}:v]'.format(i)

		filters.append(cmd)

	return inputs, filters


def compute_overlays(filters):
	start = 0
	end = 2
	overlays = []

	for i in range(1, len(filters)):
		v_ref = ''.join(filters[start:end])
		next_v_ref = '[v{}]'.format(i)

		if i == 1:
			overlay = '{}overlay{}'.format(v_ref, next_v_ref)
			overlays.append(overlay)
			start += 1
		else:
			overlay = '{}{}overlay{}'.format(last_v_ref, v_ref, next_v_ref)
			overlays.append(overlay)

		start += 1
		end += 1
		last_v_ref = next_v_ref

	return overlays, last_v_ref


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
			num_videos=len(filters),
			audio_codec=AUDIO_CODEC,
			video_codec=VIDEO_CODEC,
			pixel_fmt=PIXEL_FMT,
			output_file_path=output_file_path)
	subprocess.call(['bash', '-c', cmd])


def create_transitions(transition_file_path, mid_offset, video_file_paths):
	output_file_paths = []
	tmp_video_file_paths = video_file_paths[:] # clone array
	tmp_video_file_paths.append('end') # end transition
	last_i = len(tmp_video_file_paths) - 1

	for i, video_file_path in enumerate(tmp_video_file_paths):
		if not i == 0 or TRANSITIONS_START_ANIMATION:
			concat_file_paths = (
				OFFSET_TRANSPARENT_FILE_PATH,
				transition_file_path
			)
		else:
			concat_file_paths = (OFFSET_TRANSPARENT_FILE_PATH,)
		# We use "last_i - 1" as the last video is actually a transparent video,
		# which prevents the last image to "stick" until the end.
		if not i == 0 and not i == last_i - 1 and not TRANSITIONS_BETWEEN_IMAGES_ANIMATION:
			continue
		if i == last_i - 1 and not TRANSITIONS_END_ANIMATION:
			continue
		# Here we break as the last video is a transparent video.
		if i == last_i:
			break

		image_start = float(TRANSITIONS_START) - float(mid_offset) + float(IMAGE_DURATION * i)
		if image_start < 0:
			continue

		generate_offset(duration=image_start)

		if not video_file_path == tmp_video_file_paths[-1]:
			filename = video_file_path.split('/')[-1].split('.')[0]
		else:
			filename = video_file_path
		output_file_path = '{}/tmp/{}-transition.mov'.format(ASSETS_DIR_PATH, filename)
		output_file_paths.append(output_file_path)

		concat_videos(concat_file_paths, output_file_path)

	return output_file_paths


def generate_offset(duration):
	tmp_output_file_path = get_temp_file_path(OFFSET_TRANSPARENT_FILE_PATH)
	cmd = 'ffmpeg \
		-y \
		-i {input_file_path} \
		-ss 0 \
		-to {duration} \
		-c:v {video_codec} \
		-pix_fmt {pixel_fmt} \
		{output_file_path}'.format(
			input_file_path=TRANSPARENT_VIDEO_FILE_PATH,
			duration=duration,
			video_codec=VIDEO_CODEC,
			pixel_fmt=PIXEL_FMT,
			output_file_path=tmp_output_file_path)
	subprocess.call(['bash', '-c', cmd])

	generate_silence(duration)
	add_silence_to_video(tmp_output_file_path, OFFSET_TRANSPARENT_FILE_PATH)


def generate_silence(duration):
	cmd = 'ffmpeg \
		-y \
		-f lavfi \
		-i anullsrc \
		-t {duration} \
		-c:a {audio_codec} \
		{output_file_path}'.format(
			duration=duration,
			audio_codec=AUDIO_CODEC,
			output_file_path=SILENCE_AUDIO_FILE_PATH)
	subprocess.call(['bash', '-c', cmd])


def get_formulas():
	if random.randrange(2) == 0:
		return (
			'x=t*(in_w-out_w)/{}'.format(IMAGE_ANIMATION_SPEED_X),
			'x=(in_w-out_w)-t*(in_w-out_w)/{}'.format(IMAGE_ANIMATION_SPEED_X)
		)
	else:
		return (
			'y=t*(in_h-out_h)/{}'.format(IMAGE_ANIMATION_SPEED_Y),
			'y=(in_h-out_h)-t*(in_h-out_h)/7'.format(IMAGE_ANIMATION_SPEED_Y)
		)


def get_temp_file_path(file_path):
	filename = file_path.split('/')[-1]
	filename = 'tmp-{}'.format(filename)
	return '{}/{}'.format(TMP_DIR_PATH, filename)


def image_to_video(image_file_path, output_file_path, duration=IMAGE_DURATION):
	tmp_output_file_path = get_temp_file_path(output_file_path)
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

	generate_silence(duration)
	add_silence_to_video(tmp_output_file_path, output_file_path)


def images_to_videos(images):
	output_file_paths = []

	for i, image_name in enumerate(images):
		if not image_name == TRANSPARENT_IMAGE_FILE_PATH:
			input_file_path = '{}/{}'.format(ASSETS_DIR_PATH, image_name)
		else:
			input_file_path = image_name

		filename = image_name.split('/')[-1].split('.')[0]
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
	inputs, filters = compute_inputs_and_filters(video_file_paths, with_audio=False)
	overlays, last_v_ref = compute_overlays(filters)
	audio_maps = compute_audio_maps(len(video_file_paths))
	cmd = 'ffmpeg \
		-y \
		{inputs} \
		-filter_complex "{overlays}" \
		{audio_maps} \
		-map {last_v_ref} \
		-c:a {audio_codec} \
		-c:v {video_codec} \
		-pix_fmt {pixel_fmt} \
		{output_file_path}'.format(
			inputs=' '.join(inputs),
			overlays=';'.join(overlays),
			audio_maps=' '.join(audio_maps),
			last_v_ref=last_v_ref,
			audio_codec=AUDIO_CODEC,
			video_codec=VIDEO_CODEC,
			pixel_fmt=PIXEL_FMT,
			output_file_path=output_file_path)
	subprocess.call(['bash', '-c', cmd])


if __name__ == '__main__':
	story = load_story()
	transitions = load_transitions()

	image_to_video(TRANSPARENT_IMAGE_FILE_PATH,
				   TRANSPARENT_VIDEO_FILE_PATH,
				   TRANSPARENT_VIDEO_DURATION)

	if TRANSITIONS_START > 0:
		generate_offset_video(TRANSITIONS_START)

	images = story['transitions']['images']
	images.append(TRANSPARENT_IMAGE_FILE_PATH)
	video_file_paths = images_to_videos(images)

	if TRANSITIONS_START > 0:
		concat_file_paths = [OFFSET_VIDEO_FILE_PATH]
		concat_file_paths.extend(video_file_paths)
		concat_videos(concat_file_paths, IMAGES_VIDEO_FILE_PATH)
	else:
		concat_videos(video_file_paths, IMAGES_VIDEO_FILE_PATH)

	default_transition = transitions[TRANSITION_ID]
	animation_filename = default_transition['name']
	animation_file_path = '{}/{}'.format(TRANSITIONS_LIBRARY_DIR_PATH, animation_filename)
	mid_offset = default_transition['mid']
	transition_file_paths = create_transitions(animation_file_path,
											   mid_offset,
											   video_file_paths)

	num_transitions = len(transition_file_paths)

	if num_transitions > 1:
		overlay_videos(transition_file_paths, TRANSITIONS_FILE_PATH)
	elif num_transitions == 1:
		copyfile(transition_file_paths[0], TRANSITIONS_FILE_PATH)

	if num_transitions > 0:
		video_file_paths = (
			IMAGES_VIDEO_FILE_PATH,
			TRANSITIONS_FILE_PATH
		)
		overlay_videos(video_file_paths, IMAGES_TRANSITIONS_FILE_PATH)
	else:
		copyfile(IMAGES_VIDEO_FILE_PATH, IMAGES_TRANSITIONS_FILE_PATH)

	video_file_paths = (
		STORY_WITH_BACKGROUND_VIDEO_FILE_PATH,
		IMAGES_TRANSITIONS_FILE_PATH
	)
	overlay_videos(video_file_paths, FINAL_VIDEO_FILE_PATH)
