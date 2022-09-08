from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange, length

class StoragePoolForm(FlaskForm):
    name = StringField(
        "Storage Pool name",
        validators=[
            DataRequired(message="必須の項目です"),
            length(max=32, message="最大32文字です"),
        ],
    )
    resource_group_uuid = SelectField(
        "Resource group",
        coerce=str
    )
    capacity = IntegerField(
        "Capacity",
        validators=[
            DataRequired(message="必須の項目です"),
            NumberRange(min=1, max=32, message="1~32で指定してください")
        ]
    )

    submit = SubmitField("作成")

class VolumeForm(FlaskForm):
    name = StringField(
        "Volume name",
        validators=[
            DataRequired(message="必須の項目です"),
            length(max=32, message="最大32文字です"),
        ],
    )
    storage_pool_uuid = SelectField(
        "Storage pool",
        coerce=str
    )
    capacity = IntegerField(
        "Capacity",
        validators=[
            DataRequired(message="必須の項目です"),
            NumberRange(min=1, max=32, message="1~32で指定してください")
        ]
    )

    submit = SubmitField("作成")