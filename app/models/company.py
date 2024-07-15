from .timestamp_mixin import db, TimestampMixin

class Company(db.Model, TimestampMixin):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    admins = db.relationship('Admin', backref='company', lazy=True)
    hrs = db.relationship('HR', backref='company', lazy=True)
    employees = db.relationship('Employee', backref='company', lazy=True)

    def __init__(self, name):
        self.name = name