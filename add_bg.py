import subprocess

from add_images import (add_audio_to_video,
						generate_silence_audio,
						overlay_videos)
from config import *


def crop_story_video():
	cmd = 'ffmpeg \
		-y \
		-i {input_file_path} \
		-vf "crop={width}:{height}:0:0" \
		-c:v {video_codec} \
		-pix_fmt {pixel_fmt} \
		{output_file_path}'.format(
			input_file_path=STORY_VIDEO_WITH_PRESENTER_BG_FILE_PATH,
			width=VIDEO_SIZE[0] - (BACKGROUND_PADDING * 2),
			height=VIDEO_SIZE[1] - (BACKGROUND_PADDING * 2),
			video_codec=VIDEO_CODEC,
			pixel_fmt=PIXEL_FMT,
			output_file_path=CROPPED_STORY_VIDEO_FILE_PATH)
	subprocess.call(['bash', '-c', cmd])


def get_duration(input_file_path):
	# -sexagesimal outputs HOURS:MM:SS.MICROSECONDS time unit format
	cmd = 'ffprobe \
		-sexagesimal \
		-show_entries format=duration \
		-of default=noprint_wrappers=1:nokey=1 \
		{}'.format(input_file_path)
	data = subprocess.check_output(['bash', '-c', cmd])
	return data.decode('utf-8').strip() # binary to utf-8 string, removes \n

	
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

	duration = get_duration(PADDED_STORY_VIDEO_FILE_PATH)
	generate_silence_audio(duration, SILENCE_AUDIO_FILE_PATH)
	add_audio_to_video(SILENCE_AUDIO_FILE_PATH,
					   BACKGROUND_FILE_PATH,
					   BACKGROUND_WITH_AUDIO_FILE_PATH)

	video_file_paths = (
		BACKGROUND_WITH_AUDIO_FILE_PATH,
		PADDED_STORY_VIDEO_FILE_PATH
	)
	overlay_videos(video_file_paths, STORY_WITH_BACKGROUND_FILE_PATH)
