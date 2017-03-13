#from flask_wtf import Form
from wtforms import Form, StringField, TextField, validators, TextAreaField, SubmitField
#from wtforms.validators import DataRequired


class MessageForm(Form):
    to_input = TextField('To: ', validators=[validators.required(), validators.Length(min=3, max=100)])
    from_input = TextField('From: ', validators=[validators.required(), validators.Length(min=3, max=100)])
    message_input = TextAreaField('Message: ', validators=[validators.required(), validators.Length(max=1000)])
