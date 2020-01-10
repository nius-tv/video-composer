from config import *
from google.cloud import error_reporting
from utils import *


if __name__ == '__main__':
	error_client = error_reporting.Client()
	try:
		data = load_story()
		data['duration'] = get_duration(STORY_VIDEO_WITH_CATEGORY_FILE_PATH)
		save_story(data)
	except Exception:
		error_client.report_exception()
		raise
