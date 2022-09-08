from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, length

class UserForm(FlaskForm):
    username = StringField(
        "User name",
        validators=[
            DataRequired(message="必須の項目です"),
            length(max=30, message="最大30文字です"),
        ],
    )
    email = StringField(
        "E-mail",
        validators=[
            DataRequired(message="必須の項目です"),
            Email(message="無効なアドレスです"),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="必須の項目です"),
        ],
    )
    submit = SubmitField("登録")

class SigninForm(FlaskForm):
    email = StringField(
        "E-mail",
        validators=[
            DataRequired(message="必須の項目です"),
            Email(message="形式が無効です"),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="必須の項目です"),
        ],
    )
    submit = SubmitField("サインイン")
