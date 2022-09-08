from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, IPAddress, NumberRange, length

class NetworkForm(FlaskForm):
    name = StringField(
        "Network name",
        validators=[
            DataRequired(message="必須の項目です"),
            length(max=32, message="最大32文字です"),
        ],
    )
    resource_group_uuid = SelectField(
        "Resource group",
        coerce=str
    )
    cidr = StringField(
        "CIDR",
        validators=[
            DataRequired(message="必須の項目です"),
            IPAddress(ipv4=True,ipv6=False,message="無効なアドレスです")
        ]
    )
    # NOTE:netmaskはlibvirtのdhcpの仕様上、16より小さい値(ホスト数>65535)を設定できない
    netmask = IntegerField(
        "Netmask",
        validators=[
            DataRequired(message="必須の項目です"),
            NumberRange(min=16, max=28, message="16~28で指定してください")
        ]
    )

    submit = SubmitField("作成")

class BridgeForm(FlaskForm):
    name = StringField(
        "Network name",
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