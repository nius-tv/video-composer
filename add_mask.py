from config import *
from utils import *


if __name__ == '__main__':
	duration = get_duration(STORY_VIDEO_FILE_PATH)
	generate_silence_audio(duration)
	# Cut mask to match audio duration
	tmp_mask_file_path = get_tmp_file_path(MASK_FILE_PATH)
	cut_video(MASK_FILE_PATH, tmp_mask_file_path, duration)
	# Add audio to mask
	add_audio_to_video(SILENCE_AUDIO_FILE_PATH,
					   tmp_mask_file_path,
					   MASK_WITH_AUDIO_FILE_PATH)
	video_file_paths = (
		STORY_VIDEO_FILE_PATH,
		MASK_WITH_AUDIO_FILE_PATH
	)
	overlay_videos(video_file_paths, STORY_WITH_MASK_VIDEO_FILE_PATH)
