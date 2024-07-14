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
    - [File Management](#file-management)
    - [Company Configuration](#company-configuration)
- [DynamoDB REST APIs example](#dynamodb-rest-apis-example)
    - [Run DynamoDB](#run-dynamodb)
    - [Show Tables](#show-tables)
    - [Create Table via App](#create-table-via-app)
    - [View Table](#view-table)
    - [Delete Table](#delete-table)

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

Companies
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

```JSON
{
  "message": "Company deleted successfully"
}
```

File Management
Create DynamoDB Table for Files: POST /api/files/create-table
Response:

```JSON
{
  "message": "Table created successfully"
}
```

Upload File URL: POST /api/files/upload-url
Request Body:

```JSON
{
  "company_id": "string",
  "employee_id": "string",
  "file_url": "string",
  "file_type": "string"
}
```

Response:

```JSON
{
  "company_id": "string",
  "employee_id": "string",
  "files": [
    {
      "file_url": "string",
      "file_type": "string",
      "uploaded_by": "string",
      "uploaded_date": "datetime"
    }
  ]
}
```

Get File Details: GET /api/files/{company_id}/{employee_id}
Response:

```JSON
{
  "company_id": "string",
  "employee_id": "string",
  "files": [
    {
      "file_url": "string",
      "file_type": "string",
      "uploaded_by": "string",
      "uploaded_date": "datetime"
    }
  ]
}
```

Update File Details: PUT /api/files/{company_id}/{employee_id}
Request Body:

```JSON
{
  "file_url": "string",
  "file_type": "string",
  "index": "integer"
}
```

Response:

```JSON
{
  "company_id": "string",
  "employee_id": "string",
  "files": [
    {
      "file_url": "string",
      "file_type": "string",
      "uploaded_by": "string",
      "uploaded_date": "datetime"
    }
  ]
}
```

Delete File Details: DELETE /api/files/{company_id}/{employee_id}
Query Parameter:

```JSON
{
  "index": "integer"
}
```

Response:

```JSON
{
  "message": "File deleted successfully"
}
```

Company Configuration
Create DynamoDB Table for Configuration: POST /api/config/create-table
Response:

```JSON
{
  "message": "Configuration table created successfully"
}
```

Create Company Configuration: POST /api/config
Request Body:

```JSON
{
  "company_id": "string",
  "naming_convention": {
    "FORM16": "regex_for_form16",
    "PAYSLIP": "regex_for_payslip",
    "APPOINTMENT_LETTER": "regex_for_appointment_letter",
    "RELIEVING_LETTER": "regex_for_relieving_letter",
    "APPRAISAL": "regex_for_appraisal"
  },
  "support_hr_ids": ["hr1", "hr2", "hr3"],
  "upload_hr_ids": ["hr1", "hr4"],
  "valid_file_types": ["FORM16", "PAYSLIP", "APPOINTMENT_LETTER", "RELIEVING_LETTER", "APPRAISAL"]
}
```

Response:

```JSON
{
  "company_id": "string",
  "naming_convention": {
    "FORM16": "regex_for_form16",
    "PAYSLIP": "regex_for_payslip",
    "APPOINTMENT_LETTER": "regex_for_appointment_letter",
    "RELIEVING_LETTER": "regex_for_relieving_letter",
    "APPRAISAL": "regex_for_appraisal"
  },
  "support_hr_ids": ["hr1", "hr2", "hr3"],
  "upload_hr_ids": ["hr1", "hr4"],
  "valid_file_types": ["FORM16", "PAYSLIP", "APPOINTMENT_LETTER", "RELIEVING_LETTER", "APPRAISAL"]
}
```

Get Company Configuration: GET /api/config/{company_id}
Response:

```JSON
{
  "company_id": "string",
  "naming_convention": {
    "FORM16": "regex_for_form16",
    "PAYSLIP": "regex_for_payslip",
    "APPOINTMENT_LETTER": "regex_for_appointment_letter",
    "RELIEVING_LETTER": "regex_for_relieving_letter",
    "APPRAISAL": "regex_for_appraisal"
  },
  "support_hr_ids": ["hr1", "hr2", "hr3"],
  "upload_hr_ids": ["hr1", "hr4"],
  "valid_file_types": ["FORM16", "PAYSLIP", "APPOINTMENT_LETTER", "RELIEVING_LETTER", "APPRAISAL"]
}
```

Update Company Configuration: PUT /api/config/{company_id}
Request Body:

```JSON
{
  "naming_convention": {
    "FORM16": "regex_for_form16",
    "PAYSLIP": "regex_for_payslip",
    "APPOINTMENT_LETTER": "regex_for_appointment_letter",
    "RELIEVING_LETTER": "regex_for_relieving_letter",
    "APPRAISAL": "regex_for_appraisal"
  },
  "support_hr_ids": ["hr1", "hr2", "hr3"],
  "upload_hr_ids": ["hr1", "hr4"],
  "valid_file_types": ["FORM16", "PAYSLIP", "APPOINTMENT_LETTER", "RELIEVING_LETTER", "APPRAISAL"]
}
```

Response:

```JSON
{
  "company_id": "string",
  "naming_convention": {
    "FORM16": "regex_for_form16",
    "PAYSLIP": "regex_for_payslip",
    "APPOINTMENT_LETTER": "regex_for_appointment_letter",
    "RELIEVING_LETTER": "regex_for_relieving_letter",
    "APPRAISAL": "regex_for_appraisal"
  },
  "support_hr_ids": ["hr1", "hr2", "hr3"],
  "upload_hr_ids": ["hr1", "hr4"],
  "valid_file_types": ["FORM16", "PAYSLIP", "APPOINTMENT_LETTER", "RELIEVING_LETTER", "APPRAISAL"]
}
```

Delete Company Configuration: DELETE /api/config/{company_id}
Response:

```JSON
{
  "message": "Company configuration deleted successfully"
}
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

### File Management
Use the /api/files endpoints to manage file URLs associated with employees. Only admins and HRs can access these endpoints.

### Company Configuration
Use the /api/config endpoints to manage configuration settings for each company. Only admins and HRs can access these endpoints.

# DynamoDB REST APIs example

>  https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html
  

### Run DynamoDB

>  java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb

### Show Tables

>  aws dynamodb list-tables --endpoint-url http://localhost:8000

### Create Table via App

>  http://localhost:5000/createTable

### View Table

> aws dynamodb scan --table-name Book --endpoint-url http://localhost:8000

### Delete Table

>  aws dynamodb delete-table --table-name Book --endpoint-url http://localhost:8000