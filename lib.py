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


def generate_silence_audio(duration):
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


def get_tmp_file_path(file_path):
	filename = file_path.split('/')[-1]
	filename = 'tmp-{}'.format(filename)
	return '{}/{}'.format(ASSETS_DIR_PATH, filename)


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
