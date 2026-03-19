from datetime import datetime
from models import db


class SMS(db.Model):
    __tablename__ = 'sms_messages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipient = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, sent, failed
    twilio_sid = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'recipient': self.recipient,
            'message': self.message,
            'status': self.status,
            'twilio_sid': self.twilio_sid,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
            'user_id': self.user_id
        }

    def __repr__(self):
        return f'<SMS {self.id} to {self.recipient} [{self.status}]>'
