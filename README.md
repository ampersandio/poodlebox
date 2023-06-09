<h1 align="center">
  <br>
  <a href=""><img src="app/assets/poodlebox.png" alt="Markdownify" width="300"></a>
</h1>


## **Introduction**

The Poodlebox API provides a platform for managing online courses, student profiles, user authentication, calendars, and more. It allows students, teachers, and admins to interact with the system and perform various actions.This API documentation provides details about the available endpoints and their functionalities.


## Table of Contents

- [Installation](#installation)
- [Technologies](#technologies-used)
- [Configuration](#configuration)
- [Authentication](#authentication)
- [Authentication](#authentication)
- [Courses](#courses)
- [Students](#students)
- [Admins](#admins)
- [Ads](#ads)
- [Teachers](#teachers)
- [Calendars](#calendars)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)


## **Installation**

Clone this repository using
```sh
$ git clone https://gitlab.com/poodlebox-project-team-12/poodlebox
```
Enter the directory and install all the requirements using
```sh
$ pip3 install -r requirements.txt
```
Run the app using
```sh
$ python3 uvicorn main:app --reload
```
Navigate to 127.0.0.1:8000/docs to see the Homepage

<h1 align="center">
  <br>
  <a href=""><img src="app/assets/clone.gif" alt="Markdownify" style="width: 100%; max-width: 100%;">
</h1>

## **Technologies Used**

The API is built using the following technologies:

- Framework: FastAPI
- Database: MariaDB
- Authentication: JWT (JSON Web Tokens)
- Mail Client: MailJet API
- Video Handling: video-api 

## **Configuration**

The API can be configured using environment variables. The following variables need to be set:

- `DB_NAME` - The name of the database.
- `DB_HOST` - The host address of the database.
- `DB_USER` - The username for connecting to the database.
- `DB_PASSWORD` - The password for connecting to the database.
- `DB_PORT` - The port number for the database connection.

- `SECRET_KEY` - A secret key for securing sensitive information and generating tokens.
- `ACCESS_TOKEN_EXPIRES_MINUTES` - The expiration time for access tokens in minutes.
- `ALGORITHM` - The algorithm used for token generation.

- `API_KEY` - The API key for accessing external services.
- `API_SECRET` - The secret key for accessing external services.

- `VIDEO_API_KEY` - The API key for video-related functionality.

- `DOCKER_TOKEN` - The token for authenticating with Docker registry.


## **Authentication**

The authentication section handles user registration and login. The authentication service includes the following components:

- **Password Hashing**: Passwords are hashed using the bcrypt algorithm to securely store them in the database.
- **Password Validation**: Passwords are validated to ensure they meet the required length and complexity criteria.
- **Token-based Authentication**: JWT (JSON Web Tokens) are used for token-based authentication. When a user logs in successfully, an access token is generated and returned. This access token must be included in the `Authorization` header of subsequent requests to authenticate the user.
- **Access Token Expiration**: Access tokens have an expiration time, typically set to 360 minutes (6 hours) by default. Users need to obtain a new access token after it expires.
- **User Verification**: Users can be marked as verified by updating their profile. This verification can be used to control access to certain endpoints or features.


## **Routers**

### Authentication


| Method | Endpoint                                          | Description             | 
|--------|---------------------------------------------------|-------------------------|
| POST   | `/api/authorization/registration/students`         | Register Student        |
| POST   | `/api/authorization/registration/teachers`         | Register Teacher        |
| POST   | `/api/authorization/login`                         | Login                   |

### Courses

| Method | Endpoint                                          | Description             |
|--------|---------------------------------------------------|-------------------------|
| GET    | `/api/courses/`                                   | Get All Courses         |
| GET    | `/api/courses/popular`                            | Get Most Popular Courses|
| GET    | `/api/courses/{course_id}`                         | Get Course By Id        |
| GET    | `/api/courses/{course_id}/sections/`               | Get Course Sections     |
| GET    | `/api/courses/{course_id}/sections/{section_id}`   | Get Section By Id       |
| POST   | `/api/courses/{course_id}/reviews`                 | Post Review             |
| PUT    | `/api/courses/{course_id}/status`                  | Change Course Status    |
| GET    | `/api/courses/pending_enrollments/reports`         | Get Pending Enrollments |
| PUT    | `/api/courses/pending_enrollments`                 | Judge Enrollment        |

### Students

| Method | Endpoint                                          | Description             |
|--------|---------------------------------------------------|-------------------------|
| GET    | `/api/students/courses/certificates`               | Get Certificates Of Student                |
| GET    | `/api/studentscourses/{course_id}/certificates`    | Get Certificate Of Student For Course       |
| GET    | `/api/students/courses`                            | Get Courses For Student                    |
| GET    | `/api/students/profiles`                           | Get Student Profile                        |
| PUT    | `/api/students/profiles`                           | Change Student Profile                     |
| GET    | `/api/students/courses/{course_id}`                 | Get Course For Student By Id               |
| PUT    | `/api/students/courses/{course_id}`                 | Enroll Or Unenroll From Course             |

### Admins

| Method | Endpoint                                          | Description             |
|--------|---------------------------------------------------|-------------------------|
| PUT    | `/api/admins/students/{student_id}/status/{disabled}` | Change Student Status |
| PUT    | `/api/admins/courses/{course_id}/status/{disabled}`  | Change Course Status  |
| PUT    | `/api/admins/courses/{course_id}/students/{student_id}` | Remove Student From Course |
| GET    | `/api/admins/registrations/`                       | Get Pending             |
| PUT    | `/api/admins/registrations/{teacher_id}`           | Approve                 |
| GET    | `/api/admins/ratings/traceback`                    | Traceback Ratings       |

### Ads

| Method | Endpoint                                          | Description             |
|--------|---------------------------------------------------|-------------------------|
| GET    | `/api/ads/`                                       | Get Users Ad            |

### Teachers

| Method | Endpoint                                          | Description             |
|--------|---------------------------------------------------|-------------------------|
| GET    | `/api/teachers/courses/reports`                    | Get Report              |
| GET    | `/api/teachers/profiles/`                          | View Profile            |
| PUT    | `/api/teachers/profiles/`                          | Edit Profile            |
| POST   | `/api/teachers/courses/`                           | Course Create           |
| POST   | `/api/teachers/courses/{course_id}/thumbnail`       | Upload Photo            |
| POST   | `/api/teachers/courses/{course_id}/sections/`       | Add Section             |
| PUT    | `/api/teachers/courses/{course_id}/sections/{section_id}` | Edit Section      |
| DELETE | `/api/teachers/courses/{course_id}/sections/{section_id}` | Delete Section    |
| POST   | `/api/teachers/courses/{course_id}/sections/{section_id}/content` | Add Content To Section |

### Calendars

| Method | Endpoint                                          | Description             |
|--------|---------------------------------------------------|-------------------------|
| GET    | `/api/calendars/`                                 | Get All Calendars        |
| POST   | `/api/calendars/`                                 | Create Calendars         |
| GET    | `/api/calendars/{calendar_id}`                     | Get Calendar By Calendar Id |
| PUT    | `/api/calendars/{calendar_id}`                     | Change Calendar Owner    |
| GET    | `/api/calendars/{calendar_id}/events`              | Get Events For Calendar  |
| POST   | `/api/calendars/{calendar_id}/events`              | Add Event                |
| GET    | `/api/calendars/{calendar_id}/events/{event_id}`   | Get Event By Event Id    |
| PUT    | `/api/calendars{calendar_id}/events/{event_id}`    | Change Event             |
| DELETE | `/api/calendars/{calendar_id}/events/{event_id}`   | Delete Event             |


## **Requirements**

The following are the important packages and dependencies required for this project:

- fastapi==0.95.0
- fastapi-jwt-auth==0.5.0
- mariadb==1.1.6
- pydantic==1.10.7
- uvicorn==0.21.1
- requests==2.31.0
- python-dotenv==1.0.0
- email-validator==1.1.3
- api.video==1.2.8
- mailjet==1.4.1

Make sure to have these dependencies installed in your environment before running the project. You can install them using the package manager of your choice (e.g., pip).




## **Live Demo**
If you want to see how Redoc will render your OpenAPI definition, you can try it out online at http://13.49.137.204/poodlebox/.
The default Poodlebox E-learning platform is displayed by default. Please feel free to test it 

## Database Schema

[Link to Schema Diagram](app/assets/schema_diagram.png)

