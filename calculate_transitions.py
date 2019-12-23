import math
import random

from config import *
from utils import *


if __name__ == '__main__':
	story = load_story()
	oov_frames = story['outOfVocabularyFrames']
	oov_frames_keys = sorted(oov_frames)
	duration = get_duration(STORY_VIDEO_WITH_BACKGROUND_FILE_PATH)
	start = 0
	to_sec = 0

	if len(oov_frames_keys) > 0:
		from_sec = float(oov_frames_keys[0]) / FPS
		last_key = oov_frames_keys[-1]
		to_sec = float(oov_frames[last_key]) / FPS

		if from_sec > float(TRANSITIONS_MIN_START) and \
			from_sec < float(TRANSITIONS_MAX_START):
			start = from_sec

		elif random.randrange(5) > 0 and \
			from_sec > float(TRANSITIONS_MAX_START):
			start = random.randrange(TRANSITIONS_MIN_START, TRANSITIONS_MAX_START)

	elif random.randrange(5) > 0:
		start = random.randrange(TRANSITIONS_MIN_START, TRANSITIONS_MAX_START)

	story_images = len(story['images'])
	
	if to_sec - start > story_images * float(IMAGE_DURATION):
		raise

	num_images = math.ceil((duration - start) / float(IMAGE_DURATION))

	if random.randrange(5) > 0 and \
		(num_images - 1) * IMAGE_DURATION > to_sec - start:
		num_images -= 1

	if num_images > story_images:
		num_images = story_images

	story['transitions'] = {
		'start': start,
		'numImages': num_images
	}
	save_story(story)
