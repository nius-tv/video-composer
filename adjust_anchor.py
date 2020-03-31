import subprocess

from config import *
from google.cloud import error_reporting
from utils import *


if __name__ == '__main__':
	error_client = error_reporting.Client()
	try:
		anchor = load_story()['adjustAnchor']
		cmd = 'ffmpeg \
			-y \
			-i {video_file_path} \
			-vf " \
				rotate={rotate}*PI/180, \
				scale={scaleWidth}:{scaleHeight}, \
				pad=width={width}:height={height}:x={x}:y={y} " \
			-c:v {video_codec} \
			-pix_fmt {pixel_fmt} \
			{output_file_path}'.format(
				video_file_path=STORY_VIDEO_NO_AUDIO_FILE_PATH,
				rotate=anchor['rotate'],
				scaleWidth=anchor['scaleWidth'],
				scaleHeight=anchor['scaleHeight'],
				width=VIDEO_SIZE[0],
				height=VIDEO_SIZE[1],
				x=anchor['x'],
				y=anchor['y'],
				video_codec=VIDEO_CODEC,
				pixel_fmt=PIXEL_FMT,
				output_file_path=ADJUSTED_VIDEO_FILE_PATH)
		subprocess.call(['bash', '-c', cmd])
	except Exception:
		error_client.report_exception()
		raise
