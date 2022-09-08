from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, length

class ComputeForm(FlaskForm):
    name = StringField(
        "VM name",
        validators=[
            DataRequired(message="必須の項目です"),
            length(max=32, message="最大32文字です"),
        ],
    )
    resource_group_uuid = SelectField(
        "Resource group",
        coerce=str,
        validators=[
            DataRequired(message="必須の項目です")
        ],
    )
    network_uuid = SelectField(
        "Network",
        coerce=str,
        validators=[
            DataRequired(message="必須の項目です")
        ],
    )
    image_id = SelectField(
        "Image",
        coerce=int
    )
    type_id = SelectField(
        "Machine type",
        coerce=int
    )

    # for cloud-init
    hostname = StringField(
        "Hostname",
        validators=[
            DataRequired(message="必須の項目です"),
            length(max=32, message="最大32文字です"),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="必須の項目です"),
        ],
    )
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="必須の項目です"),
            length(max=32, message="最大32文字です"),
        ],
    )
    keypair = SelectField(
        "Key pair",
        coerce=str
    )

    submit = SubmitField("作成")