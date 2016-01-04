from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
import mutagen.id3
from random import choice, shuffle
import logging
import string
import subprocess
import os

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
            
    logging.debug(string.join(args, ' '))

    with open(os.devnull, 'w') as silent:
        subprocess.call(args, stdout=silent, stderr=silent)



class DrillSergeant(object):

    SUCCESSIVE_DRILLS_PER_SECTION = 10

    def __init__(self, gui, exercises):

        self.gui = gui
        self.exercises = exercises

        self.current_section = None
        self.current_drill = None

        # the number of drills we've gone through from the current
        # section successively
        # this counter is reset whenever a new section is chosen
        self.section_drill_counter = 0

        gui.set_uncover_callback(self.uncover)

        gui.set_next_callback(self.set_next)

        gui.set_play_student_again_callback(self.play_student_again)

        gui.set_play_teacher_again_callback(self.play_teacher_again)

    def uncover(self):
        if self.current_drill and len(self.current_drill) > 1:
            self.gui.set_student(self.current_drill[1]['text'])
            self.play_student_audio()
        else:
            logging.warning('no exercise')

    def _choose_new_section(self):
        assert not self.current_section

        self.audiofile_path, exercise_set = choice(self.exercises)

        section = choice(exercise_set.values())

        self.current_section = list(section.values())

        shuffle(self.current_section)

    def _current_section_has_drills_left(self):
        return self.current_section and len(self.current_section) > 0


    def _set_next_drill_in_current_section(self):
        assert self.current_section
        assert len(self.current_section) > 0

        self.current_drill = self.current_section.pop()

    def set_next(self):

        if not self._current_section_has_drills_left():

            self._choose_new_section()            

        self._set_next_drill_in_current_section()
        

        self.gui.set_source('%s, %d drills left'
                            % (self.audiofile_path,
                               len(self.current_section)))


        self.gui.set_student('')

        self.play_teacher_audio()
        self.gui.set_teacher(self.current_drill[0]['text'])




    def play_teacher_again(self):
        if not self.current_drill:
            return

        self.play_teacher_audio()

    def play_student_again(self):
        if not self.current_drill:
            return

        self.play_student_audio()


    def play_teacher_audio(self):
        if not self.current_drill:
            raise Exception('no current drill')

        play_section(self.audiofile_path,
                     self.current_drill[0]['start_s'],
                     self.current_drill[0]['end_s'] - self.current_drill[0]['start_s'])

    def play_student_audio(self):
        if not self.current_drill:
            raise Exception('no current drill')

        play_section(self.audiofile_path,
                     self.current_drill[1]['start_s'],
                     self.current_drill[1]['end_s'] - self.current_drill[1]['start_s'])    
