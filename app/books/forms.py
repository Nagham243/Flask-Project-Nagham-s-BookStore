from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, FloatField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired
from app.models.author import Author

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    publish_date = DateField('Publish Date', validators=[DataRequired()], format='%Y-%m-%d')
    price = FloatField('Price', validators=[DataRequired()])
    appropriate = SelectField('Appropriate Age', choices=[
        ('under 8', 'Under 8'),
        ('8-15', '8-15'),
        ('adults', 'Adults')
    ], validators=[DataRequired()])
    author = SelectField('Author', coerce=int, validators=[DataRequired()])
    cover_image = FileField('Book Cover', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Save Book')

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.author.choices = []
        if 'current_user' in kwargs and kwargs['current_user']:
            self.author.choices = [(a.id, a.name) for a in Author.query.filter_by(created_by=kwargs['current_user'].id).all()]