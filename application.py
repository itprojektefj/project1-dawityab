import os
import sqlite3
from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from form import RegistrationForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'r\x86/\x1d\x92\xa7\x043\x02\x97\xc6\xee\xf8\xaf\x07\x97'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/sqlite/reader.db'
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True)
#db_session = sessionmaker(
 #   autocommit=False,
  #  autoflush=False,
  #  bind=engine)

#c = engine.cursor()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column('id', db.Integer, primary_key=True)
    user_email = db.Column('user_email',db.String(50), unique=True)
    username = db.Column('username', db.String(50), unique=True)
    password = db.Column('password', db.String(50), unique=False)
    confirm_password = db.Column('confirm_password', db.String(50), unique=False)
    book = db.relationship('Books', backref='read', lazy=True)

    def __init__(self, user_email, username, password, confirm_password):
            self.user_email = user_email
            self.username = username
            self.password = generate_password_hash(password)
            self.confirm_password = confirm_password

    def __repr__(self):
            return '<User %r>' % (self.username)


class Books(db.Model):
    __tablename__ = "books"
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.String(100), unique=False)
    author = db.Column('author', db.String(50), unique=False)
    year = db.Column('year', db.Integer,unique=False)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __init__(self,title, author, year):
            self.title = title
            self.author = author
            self.year = year

    def __repr__(self):
            return '<Books %r>' %(self.title)


db.create_all()


@app.route('/')
def index():
    print('we are here haha')
    image_file = url_for('static', filename="css/books.jpg")

    return render_template("index.html", image_file=image_file)


@app.route("/register", methods=["GET"])
def show_register():
    return render_template("register.html",form=RegistrationForm())


@app.route('/register', methods=['POST'])
def register():
    print('we are here hihi')
    form = RegistrationForm(request.form)

    if request.method == 'POST':
     if form.user_email.data is None or form.password.data is None:
      flash("User email and password is required")
    if User.query.filter_by(username=form.username.data).first() is not None:
      flash("User name already existing")

    hashed_password = generate_password_hash(form.password.data)
    print('hashed password:'+ hashed_password)
    """user = User(request.form['user_email'],
                request.form['username'],
                request.form['password'],
                request.form['confirm_password'])"""

    user = User(username=form.username.data,
                    user_email=form.user_email.data,
                    password=form.password.data,
                    confirm_password=hashed_password)


    db.session.add(user)
    db.session.commit()

    flash('Your account has been created.You can now login','success')

    return redirect(url_for('login'))
    # TODO add if else statement return render_template('register.html', form=form)


@app.route("/login", methods=["GET"])
def login():
    image_file = url_for('static', filename="css/college_library.jpg")
    return render_template("login.html", image_file=image_file)


@app.route('/login', methods=['POST'])
def login_post():

    form = LoginForm(request.form)

    if request.method == 'POST':
      if form.user_email.data is None or form.password.data is None:
       flash("User email and password is required")
    user = User.query.filter_by(name=request.form['user_email']).first()
    if user:
     if check_password_hash(user.password, form.password.data):
      return redirect(url_for('afterlogin'))
    flash('Invalid user name or password')
    return render_template('login.html', form=form)


@app.route("/after-login", methods=["POST","GET"])
def afterlogin():
    flash("Profile Page")

    return render_template("after-login.html")


''''@app.route('/search')
def searchresults(searchs):
    results = []
    searchs_ = searchs.data['search']
    if searchs.data['search'] == '':
       qry = db_session.query(Books.title)
    results = qry.all()
    if not results:
        flash('No results found!')
        return redirect('/')
    else:

       return render_template('search.html', results=results)

'''

@app.route('/logout')
def logout():

    return redirect(url_for('index'))


if __name__ == "__main__":

    db.create_all()
    app.run(debug = True)
