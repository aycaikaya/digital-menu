from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
import email_validator
from flask_wtf.file import FileField,FileAllowed,FileRequired


#upload menu
class UploadForm(FlaskForm):
    title=StringField('Title',validators=[DataRequired()])
    menu_photo=FileField('Image',validators=[FileRequired(),FileAllowed(['jpg','png'])])
    submit=SubmitField('Upload')
