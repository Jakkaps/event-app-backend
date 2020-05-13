class Event(Base):
    def __init__(self, name, description, start=None, end=None,  host=None, location=None, url=None, type=None ,study_program=None, class_year=None, image_source=None):
        self.name = name
        self.description = description
        self.start = start
        self.end = end
        self.host = host
        self.location = location
        self.url = url
        self.type = type
        self.study_program = study_program
        self.class_year = class_year
        self.image_source = image_source
