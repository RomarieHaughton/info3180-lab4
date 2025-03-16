from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])



class UploadForm(FlaskForm):  
    file = FileField('File', validators=[
        FileRequired(), 
        FileAllowed(['jpg', 'png'], 'Only images allowed!')
    ])
    submit = SubmitField('Upload')