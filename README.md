# student_management_system
# Student Course Enrollment Management API

## Overview
This project is a **Student Course Enrollment Management System** built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL** (with optional SQLite for simplicity). The API provides functionalities to manage students, courses, and enrollments, complete with JWT-based authentication, error handling, and comprehensive documentation.

---

## Features
- **Student Management**: Create and retrieve student details.
- **Course Management**: Create and retrieve course details.
- **Enrollment Management**: Enroll students in courses and fetch enrolled courses.
- **Authentication**: JWT-based token authentication for secure access.
- **Logging**: API request and response logging.
- **Testing**: Unit tests with `pytest` and `TestClient`.
- **Documentation**: Interactive API documentation via Swagger UI and ReDoc.

---

## Requirements

### Core Functionalities
1. **Student Management**
   - **Create Student**
     - Endpoint: `POST /students/`
   - **Get Student**
     - Endpoint: `GET /students/{student_id}`

2. **Course Management**
   - **Create Course**
     - Endpoint: `POST /courses/`
     - Note: Course ID is auto-generated.
   - **Get Course**
     - Endpoint: `GET /courses/{course_id}`

3. **Enrollment Management**
   - **Enroll Student in Course**
     - Endpoint: `POST /enrollments/`
   - **Get Student's Enrolled Courses**
     - Endpoint: `GET /students/{student_id}/courses/`

---

## Technical Requirements

### a) API Development
- Developed using **FastAPI**.
- **Pydantic models** used for request validation.
- **Async endpoints** implemented where applicable.
- Proper HTTP status codes returned for different responses.

### b) Database Integration
- **PostgreSQL** used (with optional **SQLite** for testing).
- **SQLAlchemy** with async ORM support.
- **Alembic** used for database migrations.

### c) Authentication & Authorization
- **JWT-based authentication** implemented.
- Authentication required for data modification (Create, Update, Delete).
- Only authenticated users can access student and course details.

### d) Error Handling & Logging
- Custom error handling for validation and business logic errors.
- Logging of API requests and responses using Python's `logging` module.

### e) Testing
- Unit tests written using `pytest`.
- API endpoint testing with `TestClient` from FastAPI.
- In-memory **SQLite** instance used for database testing.

### f) Documentation & API Testing
- Built-in **Swagger UI** available at `/docs`.


