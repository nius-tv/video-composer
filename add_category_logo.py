from config import *
from utils import *


if __name__ == '__main__':
	category = load_story()['category']
	category_video_file_path = '{}/{}.{}'.format(CATEGORY_VIDEO_DIR_PATH, category, VIDEO_FMT)
	duration = get_duration(category_video_file_path)
	generate_silence_audio(duration)
	add_audio_to_video(SILENCE_AUDIO_FILE_PATH,
					   category_video_file_path,
					   CATEGORY_WITH_AUDIO_VIDEO_FILE_PATH)
	video_file_paths = (
		COMPOSED_VIDEO_FILE_PATH,
		CATEGORY_WITH_AUDIO_VIDEO_FILE_PATH
	)
	overlay_videos(video_file_paths, STORY_VIDEO_WITH_CATEGORY_FILE_PATH)
