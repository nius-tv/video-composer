import os
# Warning: the position of these variables is sensitive.
# Keep them on top.
AUDIO_FMT = os.environ.get('AUDIO_FMT')
AUDIO_SAMPLE_RATE = 44100
IMG_FMT = os.environ.get('IMG_FMT')
LIBRARY_DIR_PATH = '/library'
SPECS = '30fps-512x1024'
STORY_DIR_PATH = '/data'
VIDEO_FMT = os.environ.get('VIDEO_FMT')
# End of sensitive variables.
ADJUSTED_VIDEO_FILE_PATH = '{}/adjusted-story.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
ANIMATE_ANCHOR_UPSAMPLING = 2
ANIMATED_ANCHOR_VIDEO_FILE_PATH = '{}/animated-anchor.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
AUDIO_CODEC = os.environ.get('AUDIO_CODEC')
AUDIO_TRACKS_FILE_PATH = '{}/audio-tracks.{}'.format(STORY_DIR_PATH, AUDIO_FMT)
BACKGROUND_WITH_AUDIO_FILE_PATH = '{}/bg-audio.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
BLACK_IMAGE_FILE_PATH = '{}/black.{}'.format(STORY_DIR_PATH, IMG_FMT)
BLACK_VIDEO_DURATION = 1
BLACK_VIDEO_FILE_PATH = '{}/black.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
CATEGORY_VIDEO_DIR_PATH = '{}/categories'.format(LIBRARY_DIR_PATH)
CATEGORY_WITH_AUDIO_VIDEO_FILE_PATH = '{}/category-audio.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
CHROMA_COLOR = '0x477144'
CHROMA_OVERLAY = 0
CHROMA_SENSITIVITY = 0.1
COMPOSED_VIDEO_FILE_PATH = '{}/composed-story.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
CROPPED_STORY_VIDEO_FILE_PATH = '{}/cropped-story.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
DYNAMIC_OVERLAY_VIDEO_FILE_PATH = '{}/dynamic-overlay.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
DYNAMIC_OVERLAY_WITH_AUDIO_VIDEO_FILE_PATH = '{}/dynamic-overlay-audio.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
FPS = float(os.environ.get('FPS'))
IMAGE_ANIMATION_SPEED_X = 10
IMAGE_ANIMATION_SPEED_Y = 7
IMAGE_DURATION = 7
IMAGES_TRANSITIONS_FILE_PATH = '{}/images-transitions.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
IMAGES_TRANSITIONS_WITH_BG_FILE_PATH = '{}/images-transitions-with-bg.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
IMAGES_VIDEO_FILE_PATH = '{}/images.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
NORMALIZED_STORY_VIDEO_FILE_PATH = '{}/normalized-story.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
NORMALIZED_STORY_VIDEO_NO_AUDIO_FILE_PATH = '{}/normalized-story-no-audio.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
OFFSET_VIDEO_FILE_PATH = '{}/offset.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
PADDED_STORY_VIDEO_FILE_PATH = '{}/padded-story.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
PIXEL_FMT = os.environ.get('PIXEL_FMT')
SILENCE_AUDIO_FILE_PATH = '{}/silence.{}'.format(STORY_DIR_PATH, AUDIO_FMT)
STORY_FILE_PATH = '{}/story.yaml'.format(STORY_DIR_PATH)
STORY_VIDEO_FILE_PATH = '{}/story.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
STORY_VIDEO_NO_AUDIO_FILE_PATH = '{}/story-no-audio.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
STORY_VIDEO_WITH_BACKGROUND_FILE_PATH = '{}/bg-story.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
STORY_VIDEO_WITH_CATEGORY_FILE_PATH = '{}/story-with-category.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
STORY_VIDEO_WITH_DYNAMIC_OVERLAY_FILE_PATH = '{}/story-with-overlay.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
STORY_VIDEO_WITH_MASK_FILE_PATH = '{}/story-with-mask.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
STORY_VIDEO_WITH_PRESENTER_BG_FILE_PATH = '{}/presenter-bg-story.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
TRANSITIONS_BETWEEN_IMAGES_ANIMATION = True
TRANSITIONS_END_ANIMATION = True
TRANSITIONS_FILE_PATH = '{}/transitions.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
TRANSITIONS_MAX_START = 5 # in seconds
TRANSITIONS_MIN_START = 3 # in seconds
TRANSITIONS_START_ANIMATION = True
TRANSPARENT_IMAGE_FILE_PATH = '{}/transparent.{}'.format(STORY_DIR_PATH, IMG_FMT)
TRANSPARENT_VIDEO_DURATION = 30
TRANSPARENT_VIDEO_FILE_PATH = '{}/transparent.{}'.format(STORY_DIR_PATH, VIDEO_FMT)
VIDEO_CODEC = os.environ.get('VIDEO_CODEC')
VIDEO_SIZE = (512, 1024)
