class DrillSection(object):

    def __init__(self, name):
        self._name = name
        self._drills = list()
        self._example = None

    def set_example(self, example):
        if self._example:
            raise Exception('drill section %s already has an example'
                            % self._name)

        self._example = example

    def has_example(self):
        return self._example

    def add_drill(self, drill):
        self._drills.append(drill)

    def get_example(self):
        return self._example

    def get_name(self):
        return self._name

    def get_drills(self):
        return self._drills
