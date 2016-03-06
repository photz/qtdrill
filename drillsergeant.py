from random import choice, shuffle, random
import logging
import string
import os
from utils import play_section
from drill_section import DrillSection

class DrillMode(object):
    def __init__(self):
        pass

    def extend(self):
        raise NotImplemented()

    def skip_remaining(self):
        raise NotImplemented()

    def get_student(self):
        raise NotImplemented()

    def get_teacher(self):
        raise NotImplemented()

    def get_next(self):
        raise NotImplemented()



class DrillDirection(object):
    normal = 0
    reverse = 1

class PlainMode(DrillMode):

    options = ['reverse_likelihood',
               'shuffle',
               'always_randomize_likelihood']

    def __init__(self, drill_sergeant):

        self._reverse_likelihood = 0.0
        self._shuffle_drills = True
        self._always_randomize_direction_likelihood = 0.0

        self._current_section = None
        self._drills_queue = None
        self._current_drill = None
        self._current_direction = None
        self._always_randomize_direction = False

        self._drill_sergeant = drill_sergeant


    def extend(self):
        more_drills = list(self._current_section.get_drills())

        if self._shuffle_drills:
            shuffle(more_drills)

        self._drills_queue.extend(more_drills)

        self._drill_sergeant.gui.set_source('%d drills left'
                                            % len(self._drills_queue))



    def set_next(self):
        if not self._current_section_has_drills_left():

            self._choose_new_section()

        self._set_next_drill_in_current_section()

        self._drill_sergeant.gui.set_source('%d drills left'
                                            % len(self._drills_queue))


    def get_teacher(self):
        assert self._current_direction is DrillDirection.normal \
            or self._current_direction is DrillDirection.reverse

        if self._current_direction is DrillDirection.normal:
            return self._current_drill.get_teacher()
        else:
            return self._current_drill.get_student()


    def get_student(self):
        assert self._current_direction is DrillDirection.normal \
            or self._current_direction is DrillDirection.reverse

        if self._current_direction is DrillDirection.normal:
            return self._current_drill.get_student()
        else:
            return self._current_drill.get_teacher()

    def skip_remaining(self):
        self._drills_queue = None
        self._choose_new_section()
        self.set_next()

    def _current_section_has_drills_left(self):
        return self._drills_queue != None and len(self._drills_queue) > 0

    def _choose_new_section(self):

        logging.debug('choosing a new section')

        assert 0 <= self._reverse_likelihood \
            and self._reverse_likelihood <= 1.0

        # throw a dice
        if self._reverse_likelihood < random():
            self._current_direction = DrillDirection.normal
        else:
            self._current_direction = DrillDirection.reverse

            self._always_randomize_direction = \
                random() <= self._always_randomize_direction_likelihood

        self._current_section = \
            choice(self._drill_sergeant._drill_sections)

        assert type(self._current_section) is DrillSection

        self._drills_queue = list(self._current_section.get_drills())

        if self._shuffle_drills:
            shuffle(self._drills_queue)

        if self._current_section.has_example():
            self._current_section.get_example().play()

    def _set_next_drill_in_current_section(self):
        assert self._drills_queue
        assert len(self._drills_queue) > 0

        assert type(self._always_randomize_direction) is bool
        if self._always_randomize_direction:
            # use a constant here rather than the magical number TODO
            r = random()
            logging.debug('p = %f' % r)
            if 0.5 < r:
                self._current_direction = DrillDirection.normal
            else:
                self._current_direction = DrillDirection.reverse
            

        self._current_drill = self._drills_queue.pop(0)



class ReverseMode(DrillMode):
    pass

class MixedMode(DrillMode):
    pass

class SnowballMode(DrillMode):

    def __init__(self, drill_sergeant):

        self._drill_sergeant = drill_sergeant
        self._current_drill = None
        self._current_drill_sections = list()

    def extend(self):
        new_drill_section = choice(self._drill_sergeant._drill_sections)
        self._current_drill_sections.append(new_drill_section)

    def set_next(self):
        drill_section = choice(self._current_drill_sections)
        self._current_drill = choice(drill_section.get_drills())

    def get_teacher(self):
        return self._current_drill.get_teacher()

    def get_student(self):
        return self._current_drill.get_student()

    def skip_remaining(self):
        pass

    
    


class DrillSergeant(object):

    def __init__(self, gui, drill_sections):
        self.gui = gui
        self._drill_sections = drill_sections

        #self._mode = SnowballMode(self)
        self._mode = PlainMode(self)

        gui.set_uncover_callback(self.uncover)

        gui.set_next_callback(self.set_next)

        gui.set_play_student_again_callback(self.play_student_again)

        gui.set_play_teacher_again_callback(self.play_teacher_again)

        gui.set_skip_remaining_callback(self.skip_remaining)

        gui.set_extend_callback(self.extend)


    def extend(self):
        self._mode.extend()

    def skip_remaining(self):
        self._mode.skip_remaining()
        self.set_next()

    def uncover(self):
        self.gui.set_student(self._mode.get_student().get_text())
        self.play_student_again()

    def set_next(self):
        self.gui.set_teacher('')
        self.gui.set_student('')

        self._mode.set_next()

        self.play_teacher_again()
        self.gui.set_teacher(self._mode.get_teacher().get_text())


    def play_teacher_again(self):
        self._mode.get_teacher().play()

    def play_student_again(self):
        self._mode.get_student().play()
