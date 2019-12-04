import subprocess

from config import *
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
			width=VIDEO_SIZE[0] - (BACKGROUND_PADDING * 2),
			height=VIDEO_SIZE[1] - (BACKGROUND_PADDING * 2),
			padding=BACKGROUND_PADDING,
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
			padding=BACKGROUND_PADDING,
			video_codec=VIDEO_CODEC,
			pixel_fmt=PIXEL_FMT,
			output_file_path=PADDED_STORY_VIDEO_FILE_PATH)
	subprocess.call(['bash', '-c', cmd])


if __name__ == '__main__':
	crop_story_video()
	pad_story_video()
	# Generate audio for background
	duration = get_duration(PADDED_STORY_VIDEO_FILE_PATH)
	generate_silence_audio(duration)
	# Cut background to match audio duration
	tmp_bg_file_path = get_tmp_file_path(BACKGROUND_VIDEO_FILE_PATH)
	cut_video(BACKGROUND_VIDEO_FILE_PATH, tmp_bg_file_path, duration)
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
