from src.database import db
from datetime import datetime
import uuid

class PromptHistory(db.Model):
    __tablename__ = 'prompt_history'
    __table_args__ = {'extend_existing': True}
    
    prompt_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    prompt_text = db.Column(db.Text, nullable=False)
    response_text = db.Column(db.Text, nullable=False)
    country_context = db.Column(db.String(10), nullable=False)
    coins_consumed = db.Column(db.Integer, default=1)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    prompt_type = db.Column(db.String(50), default='query')  # query, template, workflow
    template_type = db.Column(db.String(100))  # if prompt_type is template
    
    # Relationship
    user = db.relationship('User', backref='prompt_history')

    def __repr__(self):
        return f'<PromptHistory {self.prompt_id}>'

    def to_dict(self):
        return {
            'prompt_id': self.prompt_id,
            'user_id': self.user_id,
            'prompt_text': self.prompt_text,
            'response_text': self.response_text,
            'country_context': self.country_context,
            'coins_consumed': self.coins_consumed,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'prompt_type': self.prompt_type,
            'template_type': self.template_type
        }

