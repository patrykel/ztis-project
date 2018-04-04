from sqlalchemy.ext.declarative import declarative_base
from fxa.config.db import get_session
from sqlalchemy.orm.attributes import InstrumentedAttribute

from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP

Base = declarative_base()


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    publish_date = Column(TIMESTAMP)
    feed = Column(String)
    title = Column(String)
    content = Column(String)
    growth = Column(Boolean)
    currency = Column(String)

    def __repr__(self):
        return "<Note(\n\tid='%s',\n\tfeed='%s',\n\tdate='%s',\n\ttitle='%s',\n\tcontent='%s',\n\tgrowth='%s',\n\tcurrency='%s'\n)>" % (
            self.id,
            self.feed,
            self.publish_date,
            self.title,
            self.content,
            self.growth,
            self.currency
        )

    def get_lang(self):
        return self.feed.split("_")[0]
