from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField, PasswordField, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL
from rally_app.models import Rallyevent, Rallyspot, eventCategory, User

class RallyspotForm(FlaskForm):
    """Form for adding/updating a Rallyspot."""
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=150)])
    address = StringField('Address', validators=[DataRequired(), Length(min=3, max=150)])
    submit = SubmitField('Submit')

class RallyeventForm(FlaskForm):
    """Form for adding/updating a Rallyevent."""
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=150)])
    price = FloatField('Price')
    category = SelectField('Category', choices=[('PRODUCE', 'Produce'), ('DELI', 'Deli'), ('BAKERY', 'Bakery'), ('PANTRY', 'Pantry'), ('FROZEN', 'Frozen'), ('OTHER', 'Other')])
    photo_url = StringField('Photo', validators=[URL()])
    spot = QuerySelectField('spot', query_factory=lambda: Rallyspot.query)
    submit = SubmitField('Submit')

class SignUpForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please chose another one.')

class LoginForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')