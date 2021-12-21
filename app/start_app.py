
from flask import Flask, render_template, flash, redirect
from congrats_generator.app.forms import PersonForm

app = Flask(__name__)
app.config.from_object('config')

@app.route('/congrats', methods = ['GET', 'POST'])
def congrats_page():
    form = PersonForm()
    return render_template('login.html',
        title = 'Sign In',
        form = form)