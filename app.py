from datetime import datetime

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Article(db.Model):
    user_id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>'.format(self.body)

class LoginForm(FlaskForm):
    username = wtforms.StringField('Username', validators=[DataRequired()])
    password = wtforms.PasswordField('Password', validators=[DataRequired()])
    remember_me = wtforms.BooleanField('Remember Me')
    submit = wtforms.SubmitField('Sign In')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow,  onupdate=datetime.utcnow)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/def')
def privacy():
    return render_template('privacy.html')


@app.route('/arts', methods=['POST', 'GET'])
def articles():
    if request.method == "POST":
        print(request.form)
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

    else:
        return render_template('article.html')


@app.route('/login', methods=['GET', 'POST'])
def user():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

if __name__ == '__main__':
    app.run(debug=True)