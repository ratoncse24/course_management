# Course Management System

Create course and enroll student to the created course.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API documentation](#api-documentation)
- [Run Test](#test)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Docker: [Installation Guide](https://docs.docker.com/get-docker/)
- Docker Compose: [Installation Guide](https://docs.docker.com/compose/install/)

## Installation

To set up the project, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/ratoncse24/course_management.git
    ```

2. Navigate to the project directory:

    ```bash
    cd course_management
    ```

3. Create a `.env` file based on the provided `.env.example` file:

    ```bash
    cp .env.example .env
    ```


## Usage

To run the project locally using Docker Compose, follow these steps:

1. Build and start the Docker containers:

    ```bash
    docker-compose up --build
    ```

2. Access the application in your web browser:

    ```
    http://localhost:8000
    ```

3. Stop the Docker containers:

    ```bash
    docker-compose down -v
    ```

## API documentation

## Base URL

The base URL for all API endpoints is `http://localhost:8000/api/v1`.

## Endpoints

### 1. Create Courses

- **URL:** `/courses`
- **Method:** POST
- **Description:** Create a new Course
- **Request Body:**
  - `title` (required): Course title (string)
  - `instructor` (required): Course instructor (string)
  - `description` (required): Course description (string)
  - `duration` (required): Course duration (integer)
  - `price` (required): Course price (float)
- **Response:**
  - Status Code: 201 CREATED
  - Content Type: application/json
  - Body: Newly created course objects in JSON format

Example Request:
  - `POST http://localhost:8000/api/v1/courses`
  - Example Request Body:
```json
   {
     "title": "Course 4",
     "description": "This is description",
     "instructor": "Samsul",
     "duration": 120,
     "price": 49.99
   }
```

Example Response Body:
```json
   {
       "course_id": 1,
       "title": "Course 4",
       "description": "This is description",
       "instructor": "Samsul",
       "duration": 120,
       "price": 49.99
   }
```

### 2. List of Courses with Filtering

- **URL:** `/courses`
- **Method:** GET
- **Description:** Get list of courses with optional filtering options.
- **Request Parameters:**
  - `title` (optional): Filter courses by title (string)
  - `instructor` (optional): Filter courses by instructor name (string)
  - `duration` (optional): Filter courses with duration to the specified value (integer)
  - `price` (optional): Filter courses with price equal to the specified value (float)
- **Response:**
  - Status Code: 200 OK
  - Content Type: application/json
  - Body: Array of course objects in JSON format, filtered based on the provided parameters.

Example Request:
  - Without filtering: `GET http://localhost:8000/api/v1/courses`
  - With filtering: `GET http://localhost:8000/api/v1/courses?title=python`

Example Response Body:
```json
[
  {
    "course_id": 1,
    "title": "Course 1",
    "description": "Description of Course 1",
    "instructor": "Instructor 1",
    "duration": 60,
    "price": 100.00
  },
  {
    "course_id": 2,
    "title": "Course 2",
    "description": "Description of Course 2",
    "instructor": "Instructor 2",
    "duration": 90,
    "price": 150.00
  }
]
```

### 3. Course details

- **URL:** `/courses/:id`
- **Method:** GET
- **Description:** Get details of a course with the student enrollments.
- **Response:**
  - Status Code: 200 OK
  - Content Type: application/json
  - Body: **course_details**: contain the course details, **student_enrollments**: All the enrollment of the course

Example Request:
  - `GET http://localhost:8000/api/v1/courses/1`

Example Response Body:
```json
{
    "course_details": {
        "course_id": 1,
        "title": "Course 4",
        "description": "This is description",
        "instructor": "My Instructor",
        "duration": 30,
        "price": 50.0
    },
    "student_enrollments": [
        {
            "enrollment_id": 1,
            "student_name": "Raton Hosen",
            "course_id": 1,
            "enrollment_date": "2024-10-10"
        },
        {
            "enrollment_id": 2,
            "student_name": "Habib",
            "course_id": 1,
            "enrollment_date": "2024-10-10"
        }
    ]
}
```


### 4. Create Enrollment for a Course

- **URL:** `/enrollments`
- **Method:** POST
- **Description:** Create a new Enrollment
- **Request Body:**
  - `student_name` (required): Enroll student name (string). Validation: Can't contain any special character, Name can't be fully numeric
  - `enrollment_date` (required): Course enrollment date (date). Validation: Date must be greater than or equal to current date.
  - `course_id` (required): Course reference ID (integer). Validation: Course reference must be exist in the database
- **Response:**
  - Status Code: 201 CREATED
  - Content Type: application/json
  - Body: Newly created enrollment objects in JSON format

Example Request:
  - `POST http://localhost:8000/api/v1/enrollments`
  - Example Request Body:
```json
   {
           "student_name": "Habib",
           "course_id": 1,
           "enrollment_date": "2024-10-10"
   }
```

Example Response Body:
```json
   {
       "student_name": "Habib",
       "course_id": 1,
       "enrollment_date": "2024-10-10"
   }
```

## Test
Open terminal and run below command to Run the test:

```bash
 docker exec -it course_management_backend python manage.py test
```