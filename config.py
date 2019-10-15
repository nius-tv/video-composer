# Warning: the position of these variables is sensitive
ASSETS_DIR_PATH = '/assets'
TMP_DIR_PATH = '{}/tmp'.format(ASSETS_DIR_PATH)
LIBRARY_DIR_PATH = '/library'
# End of sensitive variables
AUDIO_CODEC = 'pcm_s16le'
BACKGROUND_PADDING = 7 # in pixels
CHROMA_OVERLAY = 0.1
CHROMA_SENSITIVITY = 0.3
CROPPED_STORY_VIDEO_FILE_PATH = '{}/cropped-story.mov'.format(TMP_DIR_PATH)
FINAL_VIDEO_FILE_PATH = '{}/video.mov'.format(TMP_DIR_PATH)
FPS = 30
IMAGE_ANIMATION_SPEED_Y = 7
IMAGE_ANIMATION_SPEED_X = 10
IMAGE_DURATION = 4
IMAGES_TRANSITIONS_FILE_PATH = '{}/images-transitions.mov'.format(TMP_DIR_PATH)
IMAGES_VIDEO_FILE_PATH = '{}/images.mov'.format(TMP_DIR_PATH)
OFFSET_VIDEO_FILE_PATH = '{}/offset-transparent.mov'.format(TMP_DIR_PATH)
PIXEL_FMT = 'argb'
SILENCE_AUDIO_FILE_PATH = '{}/silence.wav'.format(TMP_DIR_PATH)
STORY_FILE_PATH = 'story.yaml'
TRANSITION_FILE_PATH = 'transitions.yaml'
TRANSITION_ID = 0
TRANSITIONS_BETWEEN_IMAGES_ANIMATION = True
TRANSITIONS_END_ANIMATION = True
TRANSITIONS_START = 1 # in seconds
TRANSITIONS_START_ANIMATION = False
TRANSITIONS_FILE_PATH = '{}/transitions.mov'.format(TMP_DIR_PATH)
TRANSITIONS_LIBRARY_DIR_PATH = '{}/transitions/30fps-512x1024'.format(LIBRARY_DIR_PATH)
TRANSPARENT_IMAGE_FILE_PATH = '{}/transparent.png'.format(LIBRARY_DIR_PATH)
TRANSPARENT_VIDEO_DURATION = 30
TRANSPARENT_VIDEO_FILE_PATH = '{}/transparent.mov'.format(TMP_DIR_PATH)
VIDEO_CODEC = 'qtrle'
VIDEO_FILE_PATH = '{}/video.mp4'.format(ASSETS_DIR_PATH)
VIDEO_FMT = 'mov'
VIDEO_SIZE = (512, 1024)
