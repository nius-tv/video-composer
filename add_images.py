def concat_videos(video_file_paths, output_file_path):
	inputs, filters = compute_inputs_and_filters(video_file_paths)
	cmd = 'ffmpeg \
		-y \
		{inputs} \
		-filter_complex "{filters}concat=n={num_videos}:v=1:a=1:unsafe=1[v][a]" \
		-map [a] \
		-map [v] \
		-c:a {audio_codec} \
		-c:v {video_codec} \
		-pix_fmt {pixel_fmt} \
		{output_file_path}'.format(
			inputs=' '.join(inputs),
			filters=''.join(filters),
			num_videos=len(video_file_paths),
			audio_codec=AUDIO_CODEC,
			video_codec=VIDEO_CODEC,
			pixel_fmt=PIXEL_FMT,
			output_file_path=output_file_path)
	subprocess.call(['bash', '-c', cmd])


