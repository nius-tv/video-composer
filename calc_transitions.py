import math
import random

from config import *
from utils import *


if __name__ == '__main__':
	story = load_story()
	duration = story['duration']
	oov_frames = story['outOfVocabularyFrames']
	oov_frames_keys = sorted(oov_frames)

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
		num_images = random.randrange(1, max_num_images)

	story['transitions'] = {
		'start': start,
		'numImages': num_images
	}
	save_story(story)
