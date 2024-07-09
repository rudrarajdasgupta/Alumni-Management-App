# Alumni Management API

This is an API for managing alumni, admins, HRs, and companies. It is built using Flask, Flask-Restx, Flask-JWT-Extended, and SQLAlchemy.

## Table of Contents

- [Alumni Management API](#alumni-management-api)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Setup](#setup)
  - [Running the Application](#running-the-application)
  - [API Endpoints](#api-endpoints)
    - [Authentication](#authentication)
    - [Admins](#admins)
    - [HRs](#hrs)
    - [Employees](#employees)
    - [Companies](#companies)
  - [Usage](#usage)
    - [Register a User:](#register-a-user)
    - [Login:](#login)
    - [Manage Admins, HRs, Employees, and Companies:](#manage-admins-hrs-employees-and-companies)

## Requirements

- Python 3.8+
- SQLite (for local development)

## Installation

1. Clone the repository:

   git clone https://github.com/yourusername/alumni-management-api.git
   cd alumni-management-api



## Setup

Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
Install the dependencies:
```bash
pip install -r requirements.txt
```
Create a .env file in the root directory and add the following environment variables:

env
```bash
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
SQLALCHEMY_DATABASE_URI=sqlite:///alumni.db
```

Initialize the database:

```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```
## Running the Application

Run the Flask application:

```bash
flask run
```
The API will be available at http://127.0.0.1:5000/api.

## API Endpoints
### Authentication

Register: POST /api/auth/register

Request Body:
 
 ```JSON
{
  "username": "string",
  "email": "string",
  "password": "string",
  "role": "string (admin, hr, employee)",
  "company_id": "integer"
}
```

Response:
 
 
 ```JSON
{
  "message": "User registered successfully"
}
```
Login: POST /api/auth/login

Request Body:
 
 
 ```JSON
{
  "username": "string",
  "password": "string"
}
```
Response:
 
 
 ```
JSON{
  "access_token": "string"
}
```

### Admins

Get All Admins: GET /api/admins

Response:
 
```JSON
[
   {
    "id": "integer",
    "username": "string",
    "email": "string",
    "company_id": "integer",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```

Create Admin: POST /api/admins

Request Body:
 
 
 ```JSON
{
  "username": "string",
  "email": "string",
  "company_id": "integer",
  "password": "string"
}
```
Response:
 
 
 ```JSON
{
  "message": "Admin created successfully"
}
```

Get Admin by ID: GET /api/admins/{id}

Response:
  
 ```JSON
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "company_id": "integer",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

Update Admin by ID: PUT /api/admins/{id}

Request Body:
  
 ```JSON
{
  "username": "string",
  "email": "string",
  "company_id": "integer",
  "password": "string"
}
```

Response:
  
 ```JSON
{
  "message": "Admin updated successfully"
}
```

Delete Admin by ID: DELETE /api/admins/{id}

Response: 
 
 ```JSON
{
  "message": "Admin deleted successfully"
}
```

### HRs

Get All HRs: GET /api/hrs

Response: 

```JSON
[
   {
    "id": "integer",
    "username": "string",
    "email": "string",
    "company_id": "integer",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```

Create HR: POST /api/hrs

Request Body:
  
 ```JSON
{
  "username": "string",
  "email": "string",
  "company_id": "integer",
  "password": "string"
}
```

Response: 
 
 ```JSON
{
  "message": "HR created successfully"
}
```

Get HR by ID: GET /api/hrs/{id}

Response:
  
 ```JSON
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "company_id": "integer",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

Update HR by ID: PUT /api/hrs/{id}

Request Body:
  
 ```JSON
{
  "username": "string",
  "email": "string",
  "company_id": "integer",
  "password": "string"
}
```

Response:
  
 ```JSON
{
  "message": "HR updated successfully"
}
```

Delete HR by ID: DELETE /api/hrs/{id}

Response: 
 
 ```JSON
{
  "message": "HR deleted successfully"
}
```

### Employees

Get All Employees: GET /api/employees

Response:

```JSON
[
   {
    "id": "integer",
    "username": "string",
    "email": "string",
    "company_id": "integer",
    "joining_date": "datetime",
    "last_working_date": "datetime",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```
Create Employee: POST /api/employees

Request Body:
 
 ```JSON
{
  "username": "string",
  "email": "string",
  "company_id": "integer",
  "password": "string",
  "joining_date": "datetime",
  "last_working_date": "datetime"
}
```

Response:
  
 ```JSON
{
  "message": "Employee created successfully"
}
```

Get Employee by ID: GET /api/employees/{id}

Response:
  
 ```JSON
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "company_id": "integer",
  "joining_date": "datetime",
  "last_working_date": "datetime",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

Update Employee by ID: PUT /api/employees/{id}

Request Body:
  
 ```JSON
{
  "username": "string",
  "email": "string",
  "company_id": "integer",
  "password": "string",
  "joining_date": "datetime",
  "last_working_date": "datetime"
}
```

Response: 
 
 ```JSON
{
  "message": "Employee updated successfully"
}
```
Delete Employee by ID: DELETE /api/employees/{id}

Response: 
 
 ```JSON
{
  "message": "Employee deleted successfully"
}
```

### Companies

Get All Companies: GET /api/companies

Response:

```JSON
[
   {
    "id": "integer",
    "name": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```

Create Company: POST /api/companies

Request Body:
 
 ```JSON
{
  "name": "string"
}
```

Response:
 
 ```JSON
{
  "message": "Company created successfully"
}
```

Get Company by ID: GET /api/companies/{id}

Response:
 
 
 ```JSON
{
  "id": "integer",
  "name": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

Update Company by ID: PUT /api/companies/{id}

Request Body:
 
 
 ```JSON
{
  "name": "string"
}
```

Response:
  
 ```JSON
{
  "message": "Company updated successfully"
}
```

Delete Company by ID: DELETE /api/companies/{id}

Response:
 
 
 ```JSON{
  "message": "Company deleted successfully"
}
```

Get HRs by Company ID: GET /api/companies/ ```JSON{company_id}```/hrs

Response:
 
```JSON
[
   {
    "id": "integer",
    "username": "string",
    "email": "string",
    "company_id": "integer",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```

Get Employees by Company ID: GET /api/companies/ ```JSON{company_id}```/employees

Response:
 
```JSON
[
   {
    "id": "integer",
    "username": "string",
    "email": "string",
    "company_id": "integer",
    "joining_date": "datetime",
    "last_working_date": "datetime",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```

## Usage
### Register a User:

Use the /api/auth/register endpoint to register a new admin, HR, or employee.
Provide the username, email, password, role, and company ID in the request body.

### Login:

Use the /api/auth/login endpoint to obtain a JWT token.
Provide the username and password in the request body.
Use the JWT token in the Authorization header with the Bearer scheme to access protected endpoints.

### Manage Admins, HRs, Employees, and Companies:

Use the respective CRUD endpoints for managing admins, HRs, employees, and companies.
Ensure that the appropriate role (admin or HR) is used for accessing specific endpoints.
