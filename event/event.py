class Event(object):
    def __init__(self, name, description, url, host, start=None, end=None, location=None, study_program=None, class_year=None):
        self.name = name
        self.description = description
        self.start = start
        self.end = end
        self.host = host
        self.location = location
        self.url = url
        self.study_program = study_program
        self.class_year = class_year

