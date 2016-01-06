import logging, re
from os import path
from sentence import Sentence
from drill import Drill
from drill_section import DrillSection

class CannotParseLineException(Exception):
    pass


class Label(object):

    regex = re.compile('(?P<start>\d+,\d+)\t(?P<end>\d+,\d+)\t(?P<section>[^;]*);(?P<drill>[^;]*);(?P<text>.*)')

    def __init__(self, line):
        data = self._parse_label_line(line)

        self.start_s = data['start_s']
        self.end_s = data['end_s']
        self.drill = data['drill']
        self.text = data['text']
        self.section = data['section']

    @staticmethod
    def _parse_label_line(line):

        x = Label.regex.match(line)

        if x == None:
            raise CannotParseLineException('the line given does not have the right format')


        return {
            'start_s' : LabelledAudiofile._comma_separated_decimal_to_float(x.group('start')),
            'end_s' : LabelledAudiofile._comma_separated_decimal_to_float(x.group('end')),
            'section' : x.group('section'),
            'drill' : x.group('drill'),
            'text' : x.group('text')
        }

    def __str__(self):
        return '<section:%s|drill:%s|text:%s>' \
            % (self.section, self.drill, self.text)
        

class LabelledAudiofile(object):

    def __init__(self, audiofile_path):

        if not path.exists(audiofile_path):
            raise Exception('no such file: %s' % audiofile_path)

        self._labelfile_path = self._get_labelfile_path(audiofile_path)

        if not path.exists(self._labelfile_path):
            raise Exception('cannot find any labels for %s'
                            % audiofile_path)

        self._audiofile_path = audiofile_path

        self._drill_sections = list()

    

        
    @staticmethod
    def _labels(labelfile_path):
        
        with open(labelfile_path) as f:

            while True:
                
                line = f.readline()

                if line == '': return

                try:
                    label = Label(line)
                except CannotParseLineException:
                    pass
                else:
                    yield label

                


    def parse(self):

        current_drill_section = None
        previous_line = None

        for current in self._labels(self._labelfile_path):
            
            logging.info(current)

            if not current_drill_section or \
               current_drill_section.get_name() != current.section:

                    
                current_drill_section = DrillSection(current.section)

                self._drill_sections.append(current_drill_section)



            if not previous_line:
                previous_line = current
                continue


            assert previous_line.section == current.section


            if previous_line.drill != current.drill:

                example_sentence = Sentence(previous_line.text,
                                            self._audiofile_path,
                                            previous_line.start_s,
                                            previous_line.end_s)

                current_drill_section.set_example(example_sentence)

                previous_line = current

                continue


            assert previous_line.section == current.section
            assert previous_line.drill == current.drill

            teacher_sentence = Sentence(previous_line.text,
                                        self._audiofile_path,
                                        previous_line.start_s,
                                        previous_line.end_s)

            student_sentence = Sentence(current.text,
                                                self._audiofile_path,
                                                current.start_s,
                                                current.end_s)

            new_drill = Drill(teacher_sentence,
                                      student_sentence)

            current_drill_section.add_drill(new_drill)

            previous_line = None

                

    def get_drill_sections(self):
        return self._drill_sections




    @staticmethod
    def _get_labelfile_path(audiofile_path):
        _path, ext = path.splitext(audiofile_path)

        expected_labelfile_extension = 'txt'

        return _path + '.' + expected_labelfile_extension

    @staticmethod
    def _comma_separated_decimal_to_float(comma_separated_decimal,
                                          delimiter=','):

        if comma_separated_decimal.count(delimiter) != 1:
            raise Exception('improper format')

        return float(comma_separated_decimal.replace(delimiter, '.'))
