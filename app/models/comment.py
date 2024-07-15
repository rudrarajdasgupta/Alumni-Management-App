from .timestamp_mixin import db, TimestampMixin

class Comment(db.Model, TimestampMixin):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    attachment_url = db.Column(db.String(255))
    servicerequest_id = db.Column(db.Integer, db.ForeignKey('service_requests.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)

    def __init__(self, comment, servicerequest_id, employee_id, attachment_url=None):
        self.comment = comment
        self.attachment_url = attachment_url
        self.servicerequest_id = servicerequest_id
        self.employee_id = employee_id