import subprocess

from config import *
from google.cloud import error_reporting
from shutil import copyfile
from utils import *


if __name__ == '__main__':
	error_client = error_reporting.Client()
	try:
		animation = load_story()['anchorAnimation']
		speed = animation['speed']

		if speed is None:
			copyfile(STORY_VIDEO_WITH_MASK_FILE_PATH, ANIMATED_ANCHOR_VIDEO_FILE_PATH)

		else:
			scale_width = VIDEO_SIZE[0] * ANIMATE_ANCHOR_UPSAMPLING
			scale_height = VIDEO_SIZE[1] * ANIMATE_ANCHOR_UPSAMPLING
			offset = animation['offset']
			cmd = 'ffmpeg \
				-y \
				-i {input_file_path} \
				-filter_complex " \
					[0:v]scale={scale_width}x{scale_height},crop={crop_width}:{crop_height}:y={offset}-(n*{speed})[0v]; \
					[0v]scale={original_width}x{original_height}[v] \
				-c:v {video_codec} \
				-pix_fmt {pixel_fmt} \
				{output_file_path}'.format(
					input_file_path=STORY_VIDEO_WITH_MASK_FILE_PATH,
					scale_width=scale_width,
					scale_height=scale_height,
					crop_width=scale_width - offset,
					crop_height=scale_height - offset,
					offset=offset,
					speed=speed,
					original_width=VIDEO_SIZE[0],
					original_height=VIDEO_SIZE[1],
					video_codec=VIDEO_CODEC,
					pixel_fmt=PIXEL_FMT,
					output_file_path=ANIMATED_ANCHOR_VIDEO_FILE_PATH)
			subprocess.call(['bash', '-c', cmd])
	except Exception:
		error_client.report_exception()
		raise
