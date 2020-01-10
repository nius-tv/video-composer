from config import *
from google.cloud import error_reporting
from utils import *


if __name__ == '__main__':
	error_client = error_reporting.Client()
	try:
		duration = get_duration(STORY_VIDEO_NO_AUDIO_FILE_PATH)
		# Cut mask to match story duration
		tmp_mask_file_path = get_tmp_file_path(MASK_FILE_PATH)
		cut_video(MASK_FILE_PATH, tmp_mask_file_path, duration)

		video_file_paths = (
			STORY_VIDEO_NO_AUDIO_FILE_PATH,
			tmp_mask_file_path
		)
		overlay_videos(video_file_paths, STORY_VIDEO_WITH_MASK_FILE_PATH,
					   with_audio=False)
	except Exception:
		error_client.report_exception()
		raise
