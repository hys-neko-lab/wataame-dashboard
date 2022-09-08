from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, length

class ServerlessForm(FlaskForm):
    name = StringField(
        "Serverless name",
        validators=[
            DataRequired(message="必須の項目です"),
            length(max=32, message="最大32文字です"),
        ],
    )
    resource_group_uuid = SelectField(
        "Resource group",
        coerce=str
    )
    source = StringField(
        "Source",
        validators=[
            DataRequired(message="データがないか、保存されていません"),
            length(max=65536, message="最大65536文字です"),
        ]
    )

    submit = SubmitField("作成")