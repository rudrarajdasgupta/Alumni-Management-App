from app import db
from datetime import datetime, timezone

from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TimestampMixin:
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

class Company(db.Model, TimestampMixin):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    admins = db.relationship('Admin', backref='company', lazy=True)
    hrs = db.relationship('HR', backref='company', lazy=True)
    employees = db.relationship('Employee', backref='company', lazy=True)

    def __init__(self, name):
        self.name = name

class Admin(db.Model, TimestampMixin):
    __tablename__ = 'admin'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)

    def __init__(self, username, email, password, company_id):
        self.username = username
        self.email = email
        self.password = password
        self.company_id = company_id

class HR(db.Model, TimestampMixin):
    __tablename__ = 'hr'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)

    def __init__(self, username, email, password, company_id):
        self.username = username
        self.email = email
        self.password = password
        self.company_id = company_id

class Employee(db.Model, TimestampMixin):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('hr.id'), nullable=False)
    joining_date = db.Column(db.DateTime, nullable=False)
    last_working_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, email, password, company_id, created_by, joining_date, last_working_date):
        self.username = username
        self.email = email
        self.password = password
        self.company_id = company_id
        self.created_by = created_by
        self.joining_date = joining_date
        self.last_working_date = last_working_date
