from .timestamp_mixin import db, TimestampMixin

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