import math
import random

from config import *
from google.cloud import error_reporting
from utils import *


def calc_images():
	oov_frames = story['outOfVocabularyFrames']
	oov_frames_keys = sorted(oov_frames)
	start = 0
	to_sec = 0

	if len(oov_frames_keys) > 0:
		from_sec = float(oov_frames_keys[0]) / FPS
		last_key = oov_frames_keys[-1]
		to_sec = float(oov_frames[last_key]) / FPS

		if from_sec > float(TRANSITIONS_MIN_START) and \
			from_sec < float(TRANSITIONS_MAX_START):
			start = from_sec

		elif random.randrange(10) > 0 and \
			from_sec > float(TRANSITIONS_MAX_START):
			start = random.randrange(TRANSITIONS_MIN_START, TRANSITIONS_MAX_START)

	elif random.randrange(10) > 0:
		start = random.randrange(TRANSITIONS_MIN_START, TRANSITIONS_MAX_START)

	story_images = len(story['images'])
	
	if to_sec - start > story_images * float(IMAGE_DURATION):
		raise

	num_images = math.ceil((duration - start) / float(IMAGE_DURATION))

	if random.randrange(10) > 0 and \
		(num_images - 1) * IMAGE_DURATION > to_sec - start:
		num_images -= 1

	if num_images > story_images:
		num_images = story_images

	return start, num_images


if __name__ == '__main__':
	error_client = error_reporting.Client()
	try:
		story = load_story()
		duration = get_duration(STORY_VIDEO_WITH_BACKGROUND_FILE_PATH)

		if 'showAnchor' in story and not story['showAnchor']:
			start = 0
			num_images = math.ceil(duration / float(IMAGE_DURATION))
		else:
			start, num_images = calc_images()

		story['transitions'] = {
			'start': start,
			'numImages': num_images
		}
		save_story(story)

	except Exception:
		error_client.report_exception()
		raise
