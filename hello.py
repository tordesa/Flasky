from crypt import methods
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from wtforms import StringField, SubmitField
from wtforms import validators
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm


from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

csrf = CSRFProtect(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('What is your name?', [validators.Length(
        min=4, max=25), validators.DataRequired()])
    submit = SubmitField('Submit')


@ app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name,
                           current_time=datetime.utcnow())


@ app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@ app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@ app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
