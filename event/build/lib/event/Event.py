from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
import os

host = os.environ.get("EVENT_DB_HOST", localhost)
port = os.environ.get("EVENT_DB_PORT", "3307")
user = "root"
pwd = os.environ.get("EVENT_DB_PWD")
db = "event_app"

engine = db.create_engine(f"mysql://{user}:{pwd}@{host}:{port}/{db}")
Base = declarative_base()


class Event(Base):
    __tablename__ = 'events'

    id=Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    start = Column(DateTime)
    end = Column(DateTime)
    location = Column(String(200))
    url = Column(String(400), nullable=False)
    type = Column(String(200))
    study_program = Column(Strign(200))
    class_year = Column(Integer)
    image_source = Column(String(400))
    
