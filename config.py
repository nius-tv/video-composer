# Warning: the position of these variables is sensitive
LIBRARY_DIR_PATH = '/library'
STORY_DIR_PATH = '/data'
VIDEO_FMT = 'mov'
# End of sensitive variables
AUDIO_CODEC = 'pcm_s16le'
BACKGROUND_PADDING = 7 # in pixels
BACKGROUND_VIDEO_FILE_PATH = '{}/backgrounds/30fps-512x1024/49.{}'.format(LIBRARY_DIR_PATH, VIDEO_FMT)
BACKGROUND_WITH_AUDIO_FILE_PATH = '{}/bg-audio.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
CHROMA_OVERLAY = 0.1
CHROMA_SENSITIVITY = 0.3
CROPPED_STORY_VIDEO_FILE_PATH = '{}/cropped-story.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
FINAL_VIDEO_FILE_PATH = '{}/composed-story.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
FPS = 30
IMAGE_ANIMATION_SPEED_X = 10
IMAGE_ANIMATION_SPEED_Y = 7
IMAGE_DURATION = 4
IMAGES_TRANSITIONS_FILE_PATH = '{}/images-transitions.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
IMAGES_VIDEO_FILE_PATH = '{}/images.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
OFFSET_VIDEO_FILE_PATH = '{}/offset.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
PADDED_STORY_VIDEO_FILE_PATH = '{}/padded-story.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
PIXEL_FMT = 'argb'
PRESENTER_BACKGROUND_VIDEO_FILE_PATH = '{}/presenter-bgs/1.{}'.format(LIBRARY_DIR_PATH, VIDEO_FMT)
SILENCE_AUDIO_FILE_PATH = '{}/silence.wav'.format(STORY_DIR_PATH)
STORY_FILE_PATH = '{}/story.yaml'.format(STORY_DIR_PATH)
STORY_VIDEO_FILE_PATH = '{}/story.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
STORY_VIDEO_WITH_PRESENTER_BG_FILE_PATH = '{}/presenter-bg-story.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
STORY_WITH_BACKGROUND_VIDEO_FILE_PATH = '{}/bg-story.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
TRANSITION_FILE_PATH = '{}/transitions/mid.yaml'.format(LIBRARY_DIR_PATH)
TRANSITION_ID = 0
TRANSITIONS_BETWEEN_IMAGES_ANIMATION = True
TRANSITIONS_END_ANIMATION = True
TRANSITIONS_FILE_PATH = '{}/transitions.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
TRANSITIONS_LIBRARY_DIR_PATH = '{}/transitions/30fps-512x1024'.format(LIBRARY_DIR_PATH)
TRANSITIONS_START = 1 # in seconds
TRANSITIONS_START_ANIMATION = True
TRANSPARENT_IMAGE_FILE_PATH = '{}/transparent.png'.format(LIBRARY_DIR_PATH)
TRANSPARENT_VIDEO_DURATION = 30
TRANSPARENT_VIDEO_FILE_PATH = '{}/transparent.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
VIDEO_CODEC = 'qtrle'
VIDEO_SIZE = (512, 1024)
