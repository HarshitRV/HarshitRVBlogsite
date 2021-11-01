from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField

class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])

    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

class CreateLoginForm(FlaskForm):
    email = StringField("Your email", validators=[DataRequired(), Email()])
    password = PasswordField("Your password", validators=[DataRequired()])
    submit = SubmitField("Login")

class CreateRegisterForm(FlaskForm):
    email = StringField("Your email", validators=[DataRequired(), Email()])
    password = PasswordField("Your password", validators=[DataRequired()])
    name = StringField("Your name", validators=[DataRequired()])
    submit = SubmitField("Register")

class CommentForm(FlaskForm):
    body = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Comment")