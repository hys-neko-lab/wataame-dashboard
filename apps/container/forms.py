from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, length

class ContainerForm(FlaskForm):
    name = StringField(
        "Container name",
        validators=[
            DataRequired(message="必須の項目です"),
            length(max=32, message="最大32文字です"),
        ],
    )
    resource_group_uuid = SelectField(
        "Resource group",
        coerce=str
    )
    network_uuid = SelectField(
        "Network",
        coerce=str,
        validators=[
            DataRequired(message="必須の項目です")
        ],
    )
    image = StringField(
        "Image",
        validators=[
            DataRequired(message="必須の項目です"),
            length(max=128, message="最大32文字です"),
        ]
    )

    submit = SubmitField("作成")