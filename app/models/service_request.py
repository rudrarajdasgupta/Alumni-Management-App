from .timestamp_mixin import db, TimestampMixin

class ServiceRequest(db.Model, TimestampMixin):
    __tablename__ = 'service_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    raised_by = db.Column(db.String(80), nullable=False)
    assigned_to = db.Column(db.String(80))
    assigned_by = db.Column(db.String(80))
    status = db.Column(db.String(20), default='UNASSIGNED', nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    attachment_url = db.Column(db.String(255))
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    comments = db.relationship('Comment', backref='service_request', lazy=True)

    def __init__(self, raised_by, subject, content, employee_id, assigned_to=None, assigned_by=None, status='UNASSIGNED', attachment_url=None):
        self.raised_by = raised_by
        self.assigned_to = assigned_to
        self.assigned_by = assigned_by
        self.status = status
        self.subject = subject
        self.content = content
        self.attachment_url = attachment_url
        self.employee_id = employee_id