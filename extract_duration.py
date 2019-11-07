from config import *
from utils import *


if __name__ == '__main__':
	data = load_story()
	data['duration'] = get_duration(STORY_VIDEO_WITH_CATEGORY_FILE_PATH)
	save_story(data)
