from wtforms import Form, TextField, validators, TextAreaField


class MessageForm(Form):
    to_input = TextField('To: ', validators=[validators.required(), validators.Length(min=3, max=100)])
    subject_input = TextField('Subject: ', validators=[validators.required(), validators.Length(min=3, max=1000)])
    message_input = TextAreaField('Message: ', validators=[validators.required(), validators.Length(max=10000)])


class DraftForm(Form):
    to_input = TextField('To: ', validators=[validators.Length(max=100)])
    subject_input = TextField('Subject: ', validators=[validators.Length(max=1000)])
    message_input = TextAreaField('Message: ', validators=[validators.Length(max=10000)])

