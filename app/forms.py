from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class MessageForm(Form):
    from_input = StringField('from_input',validators=[DataRequired()])
    to_input = StringField('to_input', validators=[DataRequired()])
    message_input = StringField('message_input',validators=[DataRequired()])
