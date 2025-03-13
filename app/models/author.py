from app.extensions import db
from datetime import datetime

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    books = db.relationship('Book', backref='author', lazy=True, cascade="all, delete-orphan")
    user = db.relationship('User', backref='authors')

    def __repr__(self):
        return f'<Author {self.name}>'