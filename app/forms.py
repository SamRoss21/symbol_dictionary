from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from app.models import User, Concept, SearchWord, Image

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class AddConcept(FlaskForm):
    concept = StringField('New Concept', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_concept(self, concept):
        concepts = Concept.query.filter_by(concept=concept.data).first()
        if concepts is not None:
            if str(concepts.deleted) != '1':
                raise ValidationError('Already Added')

class AddSearchWord(FlaskForm):
    searchWord = StringField('New Search Word', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_searchWord(self, searchWord):
        searchWords = SearchWord.query.filter_by(searchWord=searchWord.data).first()
        if searchWords is not None:
            if str(searchWords.deleted) != '1':
                raise ValidationError('Already Added')

class AddImage(FlaskForm):
    image = StringField('Image URL', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_image(self, image):
        images = Image.query.filter_by(image=image.data).first()
        if images is not None:
            if str(images.deleted) != '1':
                raise ValidationError('Already Added')

class AddImport(FlaskForm):
    path = StringField('Path to File', validators=[DataRequired()])
    submit = SubmitField('Submit')