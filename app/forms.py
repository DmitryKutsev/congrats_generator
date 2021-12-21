from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import Required

class PersonForm(Form):
    openid = TextField('openid', validators = [Required()])
