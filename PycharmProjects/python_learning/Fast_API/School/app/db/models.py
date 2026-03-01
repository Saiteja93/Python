from .database import Base
from sqlalchemy import String, Integer, Column, Boolean, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime



class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, nullable=False)
    phone_number = Column(String)

  # Relationships
    student = relationship("Students", back_populates="user", uselist=False)
    teacher = relationship("Teachers", back_populates="user", uselist=False)

class Students(Base):
    __tablename__ ='students'
    id = Column(Integer,primary_key = True, index=True)
    grade = Column(String)
    created_at = Column(DateTime)
    owner_id = Column(Integer, ForeignKey('users.id'), unique=True)

    # Relationships
    user = relationship("Users", back_populates="student")
    enrollments = relationship("Enrollment", back_populates="student")


class Teachers(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String)
    created_at = Column(DateTime)
    owner_id = Column(Integer, ForeignKey('users.id'), unique=True)

    # Relationships
    user = relationship("Users", back_populates="teacher")
    courses = relationship("Courses", back_populates="teacher")

class Courses(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String)
    description = Column(String)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))

    # Relationships
    teacher = relationship("Teachers", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")


class Enrollment(Base):
    __tablename__ = 'enrollments'
    id = Column(Integer,primary_key=True, index=True)
    student_id =  Column(Integer, ForeignKey("students.id"))
    course_id =  Column(Integer, ForeignKey("courses.id"))
    enrolled_at = Column(DateTime)

    # Relationships
    student = relationship("Students", back_populates="enrollments")
    course = relationship("Courses", back_populates="enrollments")