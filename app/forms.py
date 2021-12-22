from flask_wtf import FlaskForm
from wtforms import Form, StringField, validators


class PersonForm(FlaskForm):
    persone_name = StringField(u'Full Name', [validators.length(min=3)])
