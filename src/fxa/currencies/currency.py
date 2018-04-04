from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Float

Base = declarative_base()


class Currency(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True)
    date = Column(TIMESTAMP)
    base_currency = Column(String)
    currency = Column(String)
    value = Column(Float)

    def __repr__(self):
        return "<Currency(date='%s', base='%s', currency='%s', value='%f')>" % (
            self.date,
            self.base_currency,
            self.currency,
            self.value
        )
