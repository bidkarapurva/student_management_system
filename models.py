from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# ---- User Model for Authentication ----
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# ---- Student Model ----
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    grade = Column(String)
    email = Column(String, unique=True, index=True)

    # Relationship to enrollments
    enrollments = relationship("Enrollment", back_populates="student")

# ---- Course Model ----
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)

    # Relationship to enrollments
    enrollments = relationship("Enrollment", back_populates="course")

# ---- Enrollment Model (Many-to-Many) ----
class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))

    # Relationships to Student and Course
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
