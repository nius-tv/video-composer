from config import *
from google.cloud import error_reporting
from utils import *


if __name__ == '__main__':
	error_client = error_reporting.Client()
	try:
		story = load_story()
		duration = get_duration(ADJUSTED_VIDEO_FILE_PATH)
		# Cut mask to match story duration
		mask_video_file_path = story['library']['maskVideoFilePath']
		tmp_mask_file_path = get_tmp_file_path(mask_video_file_path)
		cut_video(mask_video_file_path, tmp_mask_file_path, duration)

		video_file_paths = (
			ADJUSTED_VIDEO_FILE_PATH,
			tmp_mask_file_path
		)
		overlay_videos(video_file_paths, STORY_VIDEO_WITH_MASK_FILE_PATH,
					   with_audio=False)
	except Exception:
		error_client.report_exception()
		raise
