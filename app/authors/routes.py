from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.authors import authors_bp
from app.models.author import Author
from app.authors.forms import AuthorForm
from app.extensions import db

@authors_bp.route('/<int:author_id>')
def author_details(author_id):
    author = Author.query.get_or_404(author_id)
    return render_template('authors/author_details.html', title=author.name, author=author)

@authors_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_author():
    form = AuthorForm()

    if form.validate_on_submit():
        author = Author(name=form.name.data, created_by=current_user.id)
        db.session.add(author)
        db.session.commit()
        flash('Author added successfully!', 'success')
        return redirect(url_for('books.add_book'))

    return render_template('authors/add_author.html', title='Add Author', form=form)

@authors_bp.route('/edit/<int:author_id>', methods=['GET', 'POST'])
@login_required
def edit_author(author_id):
    author = Author.query.get_or_404(author_id)

    if author.created_by != current_user.id:
        flash('You can only edit authors you created!', 'danger')
        return redirect(url_for('authors.author_details', author_id=author.id))

    form = AuthorForm(obj=author)

    if form.validate_on_submit():
        author.name = form.name.data
        db.session.commit()
        flash('Author updated successfully!', 'success')
        return redirect(url_for('authors.author_details', author_id=author.id))

    if request.method == 'GET':
        form.name.data = author.name

    return render_template('authors/edit_author.html', title='Edit Author', form=form, author=author)

@authors_bp.route('/delete/<int:author_id>', methods=['POST'])
@login_required
def delete_author(author_id):
    author = Author.query.get_or_404(author_id)

    if author.created_by != current_user.id:
        flash('You can only delete authors you created!', 'danger')
        return redirect(url_for('authors.author_details', author_id=author.id))

    if author.books:
        flash('Cannot delete author with associated books. Delete the books first.', 'danger')
        return redirect(url_for('authors.author_details', author_id=author.id))

    db.session.delete(author)
    db.session.commit()

    flash('Author deleted successfully!', 'success')
    return redirect(url_for('books.all_books'))
