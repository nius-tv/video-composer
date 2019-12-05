import math
import random

from config import *
from utils import *


if __name__ == '__main__':
	story = load_story()
	oov_frames = story['outOfVocabularyFrames']
	oov_frames_keys = sorted(oov_frames)
	duration = get_duration(STORY_VIDEO_WITH_BACKGROUND_FILE_PATH)

	if len(oov_frames_keys) > 1:
		from_sec = float(oov_frames_keys[0]) / FPS
		last_key = oov_frames_keys[-1]
		to_sec = float(oov_frames[last_key]) / FPS

		start = 0
		if from_sec > TRANSITIONS_MIN_START:
			start = from_sec

		end = duration
		if to_sec < duration - TRANSITIONS_MIN_END:
			end = to_sec

		num_images = math.ceil((end - start) / float(IMAGE_DURATION))
	else:
		start = random.randrange(TRANSITIONS_MIN_START)
		max_num_images = math.floor((duration - TRANSITIONS_MIN_START - TRANSITIONS_MIN_END) / float(IMAGE_DURATION))
		
		if max_num_images > MIN_NUM_OF_IMAGES:
			num_images = random.randrange(MIN_NUM_OF_IMAGES, max_num_images)
		else:
			num_images = MIN_NUM_OF_IMAGES

	story['transitions'] = {
		'start': start,
		'numImages': num_images
	}
	save_story(story)
