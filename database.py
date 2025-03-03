from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    hints = db.Column(db.JSON, default=list)  # Liste olarak ipuçlarını saklayacağız
    flag = db.Column(db.String(100), nullable=False)
    solution = db.Column(db.Text)
    points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'hints': self.hints,
            'points': self.points,
            'created_at': self.created_at.isoformat()
        } 