from flask import render_template, redirect, url_for, request, flash, abort, current_app
from flask_login import login_required, current_user
from app.books import books_bp
from app.models.book import Book
from app.models.author import Author
from app.books.forms import BookForm
from app.extensions import db
import os
from werkzeug.utils import secure_filename
from datetime import datetime

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@books_bp.route('/')
def all_books():
    books = Book.query.all()
    return render_template('books/all_books.html', title='All Books', books=books)

@books_bp.route('/<int:book_id>')
@login_required
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('books/book_details.html', title=book.title, book=book)

@books_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_book():
    form = BookForm(current_user=current_user)

    if form.validate_on_submit():
        filename = None
        if form.cover_image.data:
            file = form.cover_image.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        book = Book(
            title=form.title.data,
            publish_date=form.publish_date.data,
            price=form.price.data,
            appropriate=form.appropriate.data,
            author_id=form.author.data,
            image_filename=filename,
            created_by=current_user.id
        )

        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('books.all_books'))

    if len(form.author.choices) == 0:
        flash('You need to add an author first!', 'warning')
        return redirect(url_for('authors.add_author'))

    return render_template('books/add_book.html', title='Add Book', form=form)

@books_bp.route('/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)

    if book.created_by != current_user.id:
        flash('You can only edit books you created!', 'danger')
        return redirect(url_for('books.book_details', book_id=book.id))

    form = BookForm(current_user=current_user, obj=book)

    if form.validate_on_submit():
        book.title = form.title.data
        book.publish_date = form.publish_date.data
        book.price = form.price.data
        book.appropriate = form.appropriate.data
        book.author_id = form.author.data

        if form.cover_image.data:
            file = form.cover_image.data
            if file and allowed_file(file.filename):
                if book.image_filename:
                    old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], book.image_filename)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)

                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                book.image_filename = filename

        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('books.book_details', book_id=book.id))

    if request.method == 'GET':
        form.title.data = book.title
        form.publish_date.data = book.publish_date
        form.price.data = book.price
        form.appropriate.data = book.appropriate
        form.author.data = book.author_id

    return render_template('books/edit_book.html', title='Edit Book', form=form, book=book)

@books_bp.route('/delete/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)

    if book.created_by != current_user.id:
        flash('You can only delete books you created!', 'danger')
        return redirect(url_for('books.book_details', book_id=book.id))

    if book.image_filename:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], book.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(book)
    db.session.commit()

    flash('Book deleted successfully!', 'success')
    return redirect(url_for('books.all_books'))