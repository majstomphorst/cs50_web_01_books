from flask import render_template, flash, redirect, url_for, request

import os, isbnlib
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegisterForm, SearchForm
from app.models import User, Book

import csv

@app.route("/")
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    
    if current_user.is_authenticated and form.validate_on_submit():
        result = Book.query.filter_by(isbn=form.search.data).first()
        rep = form.search.data
        print("----------------")
        print(rep)


    return render_template("index.html", title="Home", form=form)

@app.route('/about')
def about():
    return "about page " # render_template("about.html", title="about")

@app.route('/contact')
def contact():
    return "contact" 

@app.route('/login', methods=['GET', 'POST'])
def login():
    # if a user is allready signin
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        # get user form db
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash("Invalid Username or password")
            return redirect(url_for('login'))
        
        login_user(user)
        return redirect(url_for('index'))

    return render_template("login.html", title="Login", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():

    # if a user is allready signin
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()

    if form.validate_on_submit():

        # creating new user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    

    return render_template("register.html", title="Register", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/import')
def import_boosk_csv():

    bookList = []
    first_row = True
    with open("books.csv") as csv_books:
        csv_reader = csv.reader(csv_books,delimiter=',')
        for row in csv_reader:
            if not first_row:
                isbn = row[0]
                if isbnlib.is_isbn10(isbn):
                    isbn = isbnlib.to_isbn13(isbn)

                book = Book(isbn=int(isbn),
                            title=str(row[1]),
                            author=str(row[2]),
                            year=int(row[3]))
                bookList.append(book)
            first_row = False

        db.session.add_all(bookList)
        db.session.commit()

    return "done"