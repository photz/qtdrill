import subprocess, os, string, logging

PATH_TO_AUDIO_PLAYER = 'mpv'

def play_section(path_to_audio_file, start_s, length_s):
    assert os.path.exists(path_to_audio_file)
    assert os.path.isfile(path_to_audio_file)

    start_at_arg = '--start=%f' % start_s

    length_arg = '--length=%f' % length_s

    args = [
        PATH_TO_AUDIO_PLAYER,
        start_at_arg,
        length_arg,
        path_to_audio_file
    ]
            
    logging.debug(' '.join(args))

    with open(os.devnull, 'w') as silent:
        subprocess.call(args, stdout=silent, stderr=silent)
