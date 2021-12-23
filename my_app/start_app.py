
from flask import Flask, render_template, request
from flask_wtf import CSRFProtect

from forms import PersonForm
from generator import Generator



def starrt():

    app = Flask(__name__)
    csrf = CSRFProtect(app)
    little_pu = Generator()
    app.config['SECRET_KEY'] = "secretkey"
    print('app started')


    @app.route('/', methods=['GET', 'POST'])
    def congrats_page():
        congrat = None
        form = PersonForm()

        if form.validate_on_submit():
            congrat = little_pu.generate_congrats(str(form.data['persone_name']))
            congrat = congrat[0]['generated_text']
            # print(congrat[0]['generated_text'])
        return render_template('main.html', title='Congratulations', form=form, content=congrat)
    return app





