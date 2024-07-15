from .timestamp_mixin import db, TimestampMixin

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