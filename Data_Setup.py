import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
Base = declarative_base()


class PenDriveUser(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    picture = Column(String(300))


class PenDrivesCompanyName(Base):
    __tablename__ = 'pendrivecompany'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(PenDriveUser, backref="pendrivecompany")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self.name,
            'id': self.id
        }


class PenDriveName(Base):
    __tablename__ = 'pendrivefeatures'
    id = Column(Integer, primary_key=True)
    name=Column(String(30))
    drives_number = Column(String(30))
    item_capacity = Column(String(30))
    drive_name = Column(String(30))
    item_color = Column(String(150))
    transferspeed = Column(String(150))
    item_cost = Column(String(30))
    otgfacility = Column(String(30))
    warranty = Column(String(250))
    date = Column(DateTime, nullable=False)
    pendrivecompanyid = Column(Integer, ForeignKey('pendrivecompany.id'))
    pendrivecompany = relationship(
        PenDrivesCompanyName, backref=backref('pendrivefeatures', cascade='all, delete'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(PenDriveUser, backref="pendrivefeatures")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self. name,
            'drives_number': self. drives_number,
            'item_capacity': self. item_capacity,
            'drive_name': self. drive_name,
            'item_color': self. item_color,
            'transferspeed': self. transferspeed,
            'item_cost': self. item_cost,
            'warranty': self. warranty,
            'date': self. date,
            'id': self. id
        }
print("your database is created")
engin = create_engine('sqlite:///pendrives.db')
Base.metadata.create_all(engin)
