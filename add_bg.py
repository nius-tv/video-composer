import subprocess

from config import *
from google.cloud import error_reporting
from utils import *


def crop_story_video():
	cmd = 'ffmpeg \
		-y \
		-i {input_file_path} \
		-vf "crop={width}:{height}:{padding}:{padding}" \
		-c:v {video_codec} \
		-pix_fmt {pixel_fmt} \
		{output_file_path}'.format(
			input_file_path=STORY_VIDEO_WITH_PRESENTER_BG_FILE_PATH,
			width=VIDEO_SIZE[0] - (bg_padding * 2),
			height=VIDEO_SIZE[1] - (bg_padding * 2),
			padding=bg_padding,
			video_codec=VIDEO_CODEC,
			pixel_fmt=PIXEL_FMT,
			output_file_path=CROPPED_STORY_VIDEO_FILE_PATH)
	subprocess.call(['bash', '-c', cmd])


def pad_story_video():
	# @0 = opacity 0
	cmd = 'ffmpeg \
		-y \
		-i {input_file_path} \
		-vf "pad={width}:{height}:{padding}:{padding}:color=black@0" \
		-c:v {video_codec} \
		-pix_fmt {pixel_fmt} \
		{output_file_path}'.format(
			input_file_path=CROPPED_STORY_VIDEO_FILE_PATH,
			width=VIDEO_SIZE[0],
			height=VIDEO_SIZE[1],
			padding=bg_padding,
			video_codec=VIDEO_CODEC,
			pixel_fmt=PIXEL_FMT,
			output_file_path=PADDED_STORY_VIDEO_FILE_PATH)
	subprocess.call(['bash', '-c', cmd])


if __name__ == '__main__':
	error_client = error_reporting.Client()
	try:
		story = load_story()
		bg_padding = story['bgPadding']
		crop_story_video()
		pad_story_video()
		# Generate audio for background
		duration = get_duration(PADDED_STORY_VIDEO_FILE_PATH)
		generate_silence_audio(duration)
		# Cut background to match audio duration
		bg_video_file_path = story['library']['bgVideoFilePath']
		tmp_bg_file_path = get_tmp_file_path(bg_video_file_path)
		cut_video(bg_video_file_path, tmp_bg_file_path, duration)
		# Add audio to background
		add_audio_to_video(SILENCE_AUDIO_FILE_PATH,
						   tmp_bg_file_path,
						   BACKGROUND_WITH_AUDIO_FILE_PATH)
		# Merge background with story
		video_file_paths = (
			BACKGROUND_WITH_AUDIO_FILE_PATH,
			PADDED_STORY_VIDEO_FILE_PATH
		)
		overlay_videos(video_file_paths, STORY_VIDEO_WITH_BACKGROUND_FILE_PATH)
	except Exception:
		error_client.report_exception()
		raise
