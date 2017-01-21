import logging, string, re, sys, os
from sentence import Sentence


class CannotParseLineException(Exception):
    pass

class Section(object):
    def __init__(self, drills):
        self._drills = drills

    def has_example(self):
        return False

    def get_drills(self):
        return self._drills


class Drill(object):
    def __init__(self, teacher, student):
        self._teacher = teacher
        self._student = student

    def get_student(self):
        return self._student

    def get_teacher(self):
        return self._teacher

    def play(self):
        logging.info('nothing to play')

class SentenceWithoutAudio(object):
    def __init__(self, sentence):
        self._sentence = sentence

    def get_text(self):
        return self._sentence

    def play(self):
        logging.info('nothing to play')
        


class SimpleLabelFile(object):

    def __init__(self, path):
        self._path = path

    def parse(self):
        with open(self._get_labelfile_path(self._path)) as labelfile:
            self._drills = self._parse_labelfile(labelfile)

    def get_drill_sections(self):
        return [Section(self._drills)]
        

    @staticmethod
    def _get_labelfile_path(audiofile_path):
        path, ext = os.path.splitext(audiofile_path)

        expected_labelfile_extension = 'txt'

        return path + '.' + expected_labelfile_extension

    
    @staticmethod
    def _comma_separated_decimal_to_float(comma_separated_decimal,
                                          delimiter=','):

        #if comma_separated_decimal.count(delimiter) != 1:
        #raise Exception('improper format')

        return float(comma_separated_decimal.replace(delimiter, '.'))



    def _label_to_drill(self, line):

        regex = re.compile('(?P<start>\d+[\.,]\d+)\t(?P<end>\d+[\.,]\d+)\t(?P<teacher>[^;]*);(?P<student>.*)')

        x = regex.match(line)

        if x == None:
            raise CannotParseLineException('the line given does not have the right format')


        start = self._comma_separated_decimal_to_float(x.group('start'))

        end = self._comma_separated_decimal_to_float(x.group('end'))

        teacher = SentenceWithoutAudio(x.group('teacher'))
        student = Sentence(x.group('student'),
                           self._path,
                           start,
                           end)

        drill = Drill(teacher,
                      student)

        return drill


    def _parse_labelfile(self, labelfile):

        lines = labelfile.readlines()
    
        logging.info('%d labels have been found.' % len(lines))

        exercises = []

        for line_no, line in enumerate(lines):

            try:
                exercise = self._label_to_drill(line)
            except CannotParseLineException:
                logging.info('skipping line %d because it could not be parsed: %s' % (line_no, line))
            else:
                exercises.append(exercise)
    
        return exercises
