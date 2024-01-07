from sqlalchemy import Date, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship # , declarative_base
# from .db import Base
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(150), nullable=False)


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(150), nullable=False)

    group_id = Column('group_id', ForeignKey('group.id', ondelete='CASCADE'))
    group = relationship(Group, backref='student')


class Discipline(Base):
    __tablename__ = 'discipline'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    
    teacher_id = Column('teacher_id', ForeignKey('teacher.id', ondelete='CASCADE'))
    teacher = relationship(Teacher, backref='discipline')


class Grade(Base):
    __tablename__ = 'grade'
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=True)
    date_of = Column('date_of', Date, nullable=True)
    
    student_id = Column('student_id', ForeignKey('student.id', ondelete='CASCADE'))
    student = relationship(Student, backref='grade')

    discipline_id = Column('discipline_id', ForeignKey('discipline.id', ondelete='CASCADE'))
    discipline = relationship(Discipline, backref='grade')