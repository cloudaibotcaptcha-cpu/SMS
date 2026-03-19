from datetime import datetime, timedelta
from models import db


class OTP(db.Model):
    __tablename__ = 'otp_codes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(20), nullable=False)
    code = db.Column(db.String(6), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    attempts = db.Column(db.Integer, default=0)
    max_attempts = db.Column(db.Integer, default=3)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_expired(self):
        return datetime.utcnow() > self.expires_at

    def is_max_attempts(self):
        return self.attempts >= self.max_attempts

    def to_dict(self):
        return {
            'id': self.id,
            'phone': self.phone,
            'is_verified': self.is_verified,
            'attempts': self.attempts,
            'expires_at': self.expires_at.strftime('%Y-%m-%d %H:%M:%S') if self.expires_at else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }

    def __repr__(self):
        return f'<OTP {self.phone} [{self.code}]>'
