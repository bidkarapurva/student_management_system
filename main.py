from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import jwt
import bcrypt

import models
import database

# FastAPI App Instance
app = FastAPI()

# JWT Configuration
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 Scheme for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get database session
async def get_db():
    async with database.SessionLocal() as session:
        yield session

# ---- Authentication Functions ----

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {**data, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(select(models.User).where(models.User.email == email))
    user = result.scalars().first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise credentials_exception
        result = await db.execute(select(models.User).where(models.User.email == user_email))
        user = result.scalars().first()
        if user is None:
            raise credentials_exception
        return user
    except jwt.PyJWTError:
        raise credentials_exception

# ---- Authentication Endpoints ----

class UserCreate(BaseModel):
    email: str
    password: str

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    return {"message": "User created successfully!"}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# ---- Student Endpoints ----

class StudentCreate(BaseModel):
    name: str
    age: int
    email: str

class StudentResponse(StudentCreate):
    id: int
    class Config:
        from_attributes = True

@app.post("/students/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(student: StudentCreate, db: AsyncSession = Depends(get_db), user: models.User = Depends(get_current_user)):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    return db_student

@app.get("/students/{student_id}", response_model=StudentResponse)
async def get_student(student_id: int, db: AsyncSession = Depends(get_db), user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.Student).where(models.Student.id == student_id))
    student = result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# ---- Course Endpoints ----

class CourseCreate(BaseModel):
    title: str
    description: str

class CourseResponse(CourseCreate):
    id: int
    class Config:
        from_attributes = True

@app.post("/courses/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db), user: models.User = Depends(get_current_user)):
    db_course = models.Course(**course.dict())
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    return db_course

@app.get("/courses/{course_id}", response_model=CourseResponse)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db), user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.Course).where(models.Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# ---- Enrollment Endpoints ----

class EnrollmentRequest(BaseModel):
    student_id: int
    course_id: int

@app.post("/enrollments/", status_code=status.HTTP_201_CREATED)
async def enroll_student(enrollment: EnrollmentRequest, db: AsyncSession = Depends(get_db), user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.Student).where(models.Student.id == enrollment.student_id))
    student = result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    result = await db.execute(select(models.Course).where(models.Course.id == enrollment.course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    new_enrollment = models.Enrollment(student_id=enrollment.student_id, course_id=enrollment.course_id)
    db.add(new_enrollment)
    await db.commit()
    return {"message": "Enrollment successful"}

@app.get("/students/{student_id}/courses/")
async def get_student_courses(student_id: int, db: AsyncSession = Depends(get_db), user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.Enrollment).where(models.Enrollment.student_id == student_id))
    enrollments = result.scalars().all()
    course_ids = [enrollment.course_id for enrollment in enrollments]
    return {"enrolled_courses": course_ids}
@app.get("/courses/{course_id}/students/")
async def get_course_students(course_id: int, db: AsyncSession = Depends(get_db), user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.Enrollment).where(models.Enrollment.course_id == course_id))
    enrollments = result.scalars().all()        
    student_ids = [enrollment.student_id for enrollment in enrollments]
    return {"enrolled_students": student_ids}