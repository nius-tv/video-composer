from config import *
from utils import *


if __name__ == '__main__':
	duration = get_duration(CATEGORY_VIDEO_FILE_PATH)
	generate_silence_audio(duration)
	add_audio_to_video(SILENCE_AUDIO_FILE_PATH,
					   CATEGORY_VIDEO_FILE_PATH,
					   CATEGORY_WITH_AUDIO_VIDEO_FILE_PATH)
	video_file_paths = (
		COMPOSED_VIDEO_FILE_PATH,
		CATEGORY_WITH_AUDIO_VIDEO_FILE_PATH
	)
	overlay_videos(video_file_paths, STORY_VIDEO_WITH_CATEGORY_FILE_PATH)
