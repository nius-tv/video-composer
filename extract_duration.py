import yaml

from config import *
from utils import *


def save_story(data):
	with open(STORY_FILE_PATH, 'w') as f:
		yaml.dump(data, f, default_flow_style=False)


if __name__ == '__main__':
	data = load_story()
	data['duration'] = get_duration(STORY_VIDEO_FILE_PATH)
	save_story(data)
