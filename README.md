docker run \
-v $(pwd)/video-composer:/app \
-v $(pwd)/video-composer/assets:/assets \
-v $(pwd)/effects:/library \
-it video-composer \
bash
