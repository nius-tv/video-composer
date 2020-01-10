from config import *
from google.cloud import error_reporting
from utils import *


def cut_overlay(duration):
	tmp_file_path = get_tmp_file_path(DYNAMIC_OVERLAY_VIDEO_FILE_PATH)
	cut_video(DYNAMIC_OVERLAY_VIDEO_FILE_PATH, tmp_file_path, duration)
	return tmp_file_path


if __name__ == '__main__':
	error_client = error_reporting.Client()
	try:
		duration = get_duration(STORY_VIDEO_WITH_CATEGORY_FILE_PATH)
		tmp_overlay_video_file_path = cut_overlay(duration)
		generate_silence_audio(duration)
		add_audio_to_video(SILENCE_AUDIO_FILE_PATH,
						   tmp_overlay_video_file_path,
						   DYNAMIC_OVERLAY_WITH_AUDIO_VIDEO_FILE_PATH)
		video_file_paths = (
			STORY_VIDEO_WITH_CATEGORY_FILE_PATH,
			DYNAMIC_OVERLAY_WITH_AUDIO_VIDEO_FILE_PATH
		)
		overlay_videos(video_file_paths, STORY_VIDEO_WITH_DYNAMIC_OVERLAY_FILE_PATH)
	except Exception:
		error_client.report_exception()
		raise
