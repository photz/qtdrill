import logging, yaml


class Section(object):
    def __init__(self, x):
        _, section = x

        self._section = section

    def has_example(self):
        return False

    def get_drills(self):
        if 'sentences' in self._section:
            return map(Drill, self._section['sentences'])
        else:
            return list()

class Drill(object):
    def __init__(self, sentence):
        self._german = sentence['german']
        self._korean = sentence['korean']

    def get_student(self):
        return Sentence(self._korean)

    def get_teacher(self):
        return Sentence(self._german)

    def play(self):
        logging.info('nothing to play')

class Sentence(object):
    def __init__(self, sentence):
        self._sentence = sentence

    def get_text(self):
        if type(self._sentence) is list:
            return '<br>'.join(self._sentence)
        else:
            return self._sentence

    def play(self):
        logging.info('nothing to play')
        

class YamlFile(object):
    def __init__(self, path):
        logging.info('opening {}'.format(path))
        with open(path) as fp:
            data = yaml.load(fp.read())

            self._sections = data['sections'].items()

    def parse(self):
        pass

    def get_drill_sections(self):
        return map(Section, self._sections)

