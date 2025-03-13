from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.author import Author
from app.models.book import Book
from datetime import datetime, date

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    demo_user = User(username='demo', email='demo@example.com')
    demo_user.set_password('password')
    db.session.add(demo_user)
    db.session.commit()

    author1 = Author(name="J.K. Rowling", created_by=demo_user.id)
    author2 = Author(name="George Orwell", created_by=demo_user.id)
    author3 = Author(name="J.R.R. Tolkien", created_by=demo_user.id)

    db.session.add_all([author1, author2, author3])
    db.session.commit()

    book1 = Book(
        title="Harry Potter and the Philosopher's Stone",
        publish_date=date(1997, 6, 26),
        price=19.99,
        appropriate="8-15",
        author_id=author1.id,
        created_by=demo_user.id,
        image_filename="harrypotterbook.jpg"
    )

    book2 = Book(
        title="1984",
        publish_date=date(1949, 6, 8),
        price=14.99,
        appropriate="adults",
        author_id=author2.id,
        created_by=demo_user.id,
        image_filename="1984.png"
    )

    book3 = Book(
        title="The Hobbit",
        publish_date=date(1937, 9, 21),
        price=12.99,
        appropriate="8-15",
        author_id=author3.id,
        created_by=demo_user.id,
        image_filename="The_Hobbit.jpg"
    )

    db.session.add_all([book1, book2, book3])
    db.session.commit()