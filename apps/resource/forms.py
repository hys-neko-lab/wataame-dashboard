from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, length

class ResourceForm(FlaskForm):
    name = StringField(
        "Resource group name",
        validators=[
            DataRequired(message="必須の項目です"),
            length(max=32, message="最大32文字です"),
        ],
    )
    submit = SubmitField("作成")