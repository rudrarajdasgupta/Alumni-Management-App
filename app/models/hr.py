from .timestamp_mixin import db, TimestampMixin

class HR(db.Model, TimestampMixin):
    __tablename__ = 'hr'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    upload_access = db.Column(db.Boolean, default=False)
    support_flag = db.Column(db.Boolean, default=False)

    def __init__(self, username, email, password, company_id, upload_access=False, support_flag=False):
        self.username = username
        self.email = email
        self.password = password
        self.company_id = company_id
        self.upload_access = upload_access
        self.support_flag = support_flag