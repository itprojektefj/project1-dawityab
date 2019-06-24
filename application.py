import os
import sqlite3
from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from form import RegistrationForm, LoginForm, SearchForm, Comment
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from flask_bcrypt import Bcrypt
from datetime import datetime
import csv



app = Flask(__name__)


bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'r\x86/\x1d\x92\xa7\x043\x02\x97\xc6\xee\xf8\xaf\x07\x97'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/sqlite/reader.db'

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)

#Defining database location
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True)

  # User database model
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column('id', db.Integer, primary_key=True)
    user_email = db.Column('user_email',db.String(50), unique=True)
    username = db.Column('username', db.String(50), unique=True)
    password = db.Column('password', db.String(50), unique=False)
    confirm_password = db.Column('confirm_password', db.String(50), unique=False)
    book = db.relationship('Books', backref='read', lazy=True)
    review = db.relationship('Review', backref='read', lazy=True)
    def __init__(self, user_email, username, password, confirm_password):
            self.user_email = user_email
            self.username = username
            self.password = generate_password_hash(password)
            self.confirm_password = confirm_password


    def __repr__(self):
            return '<User %r>' % (self.username)



#Book database model
class Books(db.Model):
    __tablename__ = "books"
    isbn = db.Column('isbn', db.String(50), primary_key=True)
    title = db.Column('title', db.String(100), unique=False)
    author = db.Column('author', db.String(50), unique=False)
    year = db.Column('year', db.Integer,unique=False)
    id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __init__(self, isbn, title, author, year):
            self.isbn = isbn
            self.title = title
            self.author = author
            self.year = year

    def __repr__(self):
            return '<Books %r>' %(self.title)
class Review(db.Model):
     __tablename__ = "review"
     id = db.Column('id', db.Integer, db.ForeignKey('user.id'),nullable=False, primary_key=True)
     text = db.Column('text', db.String(140))
     authoruser = db.Column('authoruser', db.String(50), unique=False)
     isbn = db.Column('isbn', db.String(50), primary_key=True)
     rating = db.Column('rating', db.Integer)
     date = db.Column('date', db.DateTime(), default=datetime.utcnow, index=True)

     def __init__(self, id, text, authoruser, isbn, rating, date):
            self.id = id
            self.text = text
            self.authoruser = authoruser
            self.isbn = isbn
            self.rating = rating
            self.date = date



     def __repr__(self):
          _repr = '<models.Review instance; ID: {}; text_title: {}>'
          return   _repr.format(self.id, self.text.title)

#db.create_all()



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():

    image_file = url_for('static', filename="css/books.jpg")

    return render_template("index.html", image_file=image_file)


@app.route("/register", methods=["GET"])
def show_register():
    image_file = url_for('static', filename="css/library_1.jpg")
    return render_template("register.html", form=RegistrationForm(), image_file=image_file)


@app.route("/register", methods=["POST"])
def register():

    form = RegistrationForm(request.form)
    hashed_password = generate_password_hash(form.password.data)
    user_email = request.form.get("user_email")
    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = hashed_password
    user = User.query.filter_by(user_email=user_email).first()
    if not user_email or not username:
        flash(u'Please enter the required information to register', 'warning')
        return redirect(url_for('register'))

    if user:
        flash(u'Email address already exists.', 'warning')
        return redirect(url_for('register'))

    new_user = User(user_email=user_email, username=username, password=password, confirm_password=confirm_password)

    db.session.add(new_user)
    db.session.commit()

    flash(u'Your account has been created.You can now login.', 'success')
    return redirect(url_for('login'))


@app.route("/login", methods=["GET"])
def login():
        session['next'] = request.args.get('next')
        image_file = url_for('static', filename="css/college_library.jpg")

        return render_template("login.html", image_file=image_file)


@app.route('/login', methods=['POST'])
def login_post():
    user_email = request.form['user_email']
    password = request.form['password']

    user = User.query.filter_by(user_email=user_email).first()
    if not user_email or not check_password_hash(user.password, password):
            flash(u'Invalid credentials','warning')
            return redirect(url_for('login'))
    login_user(user, remember=False)
    flash(u'You were successfully logged in ','success')
    return redirect(url_for('afterlogin'))



@app.route("/after-login", methods=["POST", "GET"])
@login_required
def afterlogin():
    image_file = url_for('static', filename="css/library.jpg")
    return render_template('after-login.html', image_file=image_file)


@app.route('/search_results', methods=['POST'])
@login_required
def search_result():
   notFound = 'Not match'
   title = request.form['title']
   author = request.form['author']
   isbn = request.form['isbn']
   books_retrieved = None


   if(title and not author and not isbn):
       books_retrieved = Books.query.filter(Books.title.like("%" + title + "%")).all()

   if(not title and author and not isbn):
       books_retrieved = Books.query.filter(Books.author.like("%" + author + "%")).all()

   if(not title and not author and isbn):
       books_retrieved = Books.query.filter(Books.isbn.like("%" + isbn + "%")).all()

   if(title and author and not isbn):
       books_retrieved = (Books.query.filter(Books.title.like("%" + title + "%"), (Books.author.like("%" + author + "%")))).all()

   if(title and not author and isbn):
       books_retrieved = (Books.query.filter(Books.title.like("%" + title + "%"), (Books.isbn.like("%" + isbn + "%")))).all()

   if(not title and author and isbn):
       books_retrieved = (Books.query.filter(Books.author.like("%" + author + "%"), (Books.isbn.like("%" + isbn + "%")))).all()

   if(title and author and isbn):
       books_retrieved = (Books.query.filter(Books.title.like("%" + title + "%"), (Books.author.like("%" + author + "%")),
                          (Books.isbn.like("%" + isbn + "%")))).all()
   if(not title and not author and not isbn):
       #books_retrieved = Books.query.all()
     flash('Input required','warning')
     return redirect(url_for('afterlogin'))
   if books_retrieved:
       return render_template('search_result.html', books_retrieved=books_retrieved, title=title, author=author, notFound=notFound)

   notFound = 'Not match'
   return render_template('search_result.html', books_retrieved=None, title=title, author=author, notFound=notFound)

@app.route('/book_review/<string:isbn>', methods=['GET','POST'])
@login_required
def book_detial(isbn):
    reviews_detail = Books.query.filter_by(isbn=isbn).all()
    return render_template('book.html', book=reviews_detail[0])


def comment():
    form = Comment(request.form)
    text = form.text.data
    authoruser = form.authoruser.data
    rating = form.rating.data
    date = form.date.data
    isbn = form.isbn.data
    #user_reviews = Review.query.filter_by(isbn=isbn).first()
    allreview = Review.query.filter_by(text=text, authoruser=authoruser, rating=rating, date=date, isbn=isbn)
    db.session.add(allreview)
    db.session.commit()
    
    return render_template('book.html', allreview=allreview)


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == "__main__":

    db.create_all()
    app.run(debug=True)

