"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, length

class SampleForm(FlaskForm):
    name = StringField(
        "Key name",
        validators=[
            DataRequired(message="必須の項目です"),
            length(max=32, message="最大32文字です"),
        ],
    )
    resource_group_uuid = SelectField(
        "Resource group",
        coerce=str
    )

    submit = SubmitField("作成")
"""