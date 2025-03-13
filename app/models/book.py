from app.extensions import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    publish_date = db.Column(db.Date, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    price = db.Column(db.Float, nullable=False)
    appropriate = db.Column(db.String(20), nullable=False)
    image_filename = db.Column(db.String(255), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='books')

    def __repr__(self):
        return f'<Book {self.title}>'
