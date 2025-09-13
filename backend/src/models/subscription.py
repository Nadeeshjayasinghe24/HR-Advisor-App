from src.database import db
from datetime import datetime, date
import uuid

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    subscription_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    plan_type = db.Column(db.String(50), nullable=False)  # 'free_trial', 'basic', 'premium'
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)  # For trials/fixed terms
    status = db.Column(db.String(50), nullable=False)  # 'active', 'expired', 'cancelled'
    coins_balance = db.Column(db.Integer, default=0)  # For free trial
    last_coin_refresh = db.Column(db.Date)  # For free trial

    def __repr__(self):
        return f'<Subscription {self.plan_type} for User {self.user_id}>'

    def to_dict(self):
        return {
            'subscription_id': self.subscription_id,
            'user_id': self.user_id,
            'plan_type': self.plan_type,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'coins_balance': self.coins_balance,
            'last_coin_refresh': self.last_coin_refresh.isoformat() if self.last_coin_refresh else None
        }

class CountryHRData(db.Model):
    __tablename__ = 'country_hr_data'
    
    data_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    country_code = db.Column(db.String(10), nullable=False)  # ISO country code
    category = db.Column(db.String(100), nullable=False)  # 'Labor Law', 'Maternity Leave', 'Template'
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    source_url = db.Column(db.String(255))

    def __repr__(self):
        return f'<CountryHRData {self.title} for {self.country_code}>'

    def to_dict(self):
        return {
            'data_id': self.data_id,
            'country_code': self.country_code,
            'category': self.category,
            'title': self.title,
            'content': self.content,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'source_url': self.source_url
        }

