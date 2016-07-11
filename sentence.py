import subprocess
from utils import play_section
from os import path

class Sentence(object):

    def __init__(self, text, audiofile_path, start, end):

        if not (start < end):
            raise ValueError()

        if not path.exists(audiofile_path):
            raise Exception('no such file: %s' % audiofile_path)

        self._text = text
        self._audiofile_path = audiofile_path
        self._start = start
        self._length = end - start
        self._end = end

    def get_text(self):
        return self._text

    def play(self):
        play_section(self._audiofile_path,
                     self._start,
                     self._length)


    def export(self, dest):
        cmd = [
            'sox',
            self._audiofile_path,
            dest,
            'trim',
            '{}'.format(self._start),
            '={}'.format(self._end)
        ]

        subprocess.call(cmd)
