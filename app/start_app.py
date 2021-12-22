
from flask import Flask, render_template, request
from flask_wtf import CSRFProtect

from congrats_generator.app.forms import PersonForm
from congrats_generator.app.generator import Generator


app = Flask(__name__)
csrf = CSRFProtect(app)
# app.config.from_object('config')
little_pu = Generator()



@app.route('/', methods=['GET', 'POST'])
def congrats_page():
    congrat = None
    form = PersonForm()
    if form.validate_on_submit():
        print((form.data))
        congrat = little_pu.generate_congrats(str(form.data['persone_name']))
        congrat = congrat[0]['generated_text']
        print(congrat[0]['generated_text'])
    return render_template('main.html', title='Congratulations', form=form, content=congrat)

if __name__ == '__main__':
    app.config['SECRET_KEY'] = "secretkey"
    app.run()