from src.database import db
from datetime import datetime
import uuid

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    user_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    country_context = db.Column(db.String(100), default='US')
    coins = db.Column(db.Integer, default=100) # For subscription model

    # Relationships
    employees = db.relationship('Employee', back_populates='user', lazy=True, cascade='all, delete-orphan')
    subscriptions = db.relationship('Subscription', back_populates='user', lazy=True, cascade='all, delete-orphan')
    prompt_history = db.relationship('PromptHistory', back_populates='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'country_context': self.country_context,
            'coins': self.coins
        }


