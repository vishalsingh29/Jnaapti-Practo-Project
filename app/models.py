import datetime
from sqlalchemy import Column, Integer, String, ForeignKey , DateTime
from sqlalchemy.orm import relationship, backref
from database import Base

class Doctors(Base):
    __tablename__ = 'doctors'
    id = Column(Integer,primary_key=True)
    name = Column(String(100),nullable = False)
    email = Column(String(100),nullable = False)
    phone = Column(String(15),nullable = False)
    experience = Column(Integer,nullable=False)
    description = Column(String(500),nullable=False)
    qualification = Column(String(500),nullable=False)
    recommendation = Column(Integer,nullable=True)
    #qualifications = relationship('Qualification', backref='doctors',lazy='dynamic')
    clinics = relationship('Clinic', backref='dcotors',lazy='dynamic')
    specialities = relationship('Speciality',backref='doctors',lazy='dynamic')


class Clinic(Base):
    __tablename__ = 'Clinic'
    id = Column(Integer,primary_key=True)
    clinicName = Column(String(100))
    area = Column(String(100))
    address = Column(String(500))
    startTime = Column(String(30))
    endTime = Column(String(30))
    doctor_id = Column(Integer,ForeignKey('doctors.id'))

    def __init__(self,clinicName,area,address,startTime,endTime,doctor=None):
        self.clinicName = clinicName
        self.area = area
        self.address = address
        self.startTime = startTime
        self.endTime = endTime

    def __repr__(self):
        return "<Clinic(%s)>" %(self.name)

class Speciality(Base):
    __tablename__ = 'Speciality'
    id = Column(Integer,primary_key=True)
    specialityName = Column(String(100))
    doctor_id = Column(Integer,ForeignKey('doctors.id'))

    def __init__(self,specialityName=None):
        self.specialityName = specialityName

    def __repr__(self):
        return "<Speciality(%s)>" %(self.specialityName)
