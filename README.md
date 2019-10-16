docker run \
-v $(pwd)/video-composer:/app \
-v $(pwd)/video-composer/assets:/assets \
-v $(pwd)/nius-library:/library \
-it video-composer \
bash


python3 add_presenter_bg.py && \
python3 add_bg.py && \
python3 add_images.py