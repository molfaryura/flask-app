'''
WebApp on Flask and SQLAlchemy.
In this app the user can store and get 
data from the database about two
people, who are widely known in
narrow circles
'''

import os

from flask import Flask, render_template, request, redirect, flash

from dotenv import load_dotenv

from flask_login import login_required, current_user, login_user, logout_user

from models import *

load_dotenv()

db_password = os.environ.get('DB_password')

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{db_password}@localhost/my_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = os.environ.get('Secret_key')

db.init_app(app)

login.init_app(app)
login.login_view = 'login'


first_answer = os.environ.get('First_answer')
second_answer = os.environ.get('Second_answer')

@app.before_first_request
def create_table():
    db.create_all()


def post_fact(template, page):
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        author = current_user
        person = request.form['person']



        facts_data = Facts(title=title,
                        text=text, author=author, person=person)

        try:
            db.session.add(facts_data)
            db.session.commit()
            redirect(page)
        except:
            return 'Failed to connect to the database :('
    return render_template(template)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
     
    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email=email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/')
     
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
     
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        repeat_password = request.form['repeat_password']
        question = request.form['question']

 
        if UserModel.query.filter_by(email=email).all():
            flash('A user with this email already exists')
            return redirect('/register')
        
        if password != repeat_password:
            flash('Passwords must match')
            return redirect('/register')
        
        if question != first_answer and question != second_answer:
            return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        
        user = UserModel(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template('register.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/donate')
def donate():
    return render_template('donate.html')

@app.route('/post/shavkoon', methods=['POST', 'GET'])
@login_required
def post_shavk():
    return post_fact('post_shavk.html', '/post/shavkoon')

@app.route('/post/vasyl', methods=['POST', 'GET'])
@login_required
def post_vasyl():
    return post_fact('post_vasyl.html','/post/vasyl')

@app.route('/resource')
def resource():
    return render_template('resource.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/read', methods=['POST', 'GET'])
def read():
    '''
    The user selects a person about whom 
    he wants to get facts.
    It connects to the database and 
    show all facts on the separate html page
    '''

    if request.method == 'GET':
        return render_template('read.html')
    elif request.method == 'POST':
        if request.form.get("person") == 'All':
            db_data = Facts.query.all()
            return render_template('result.html', db_data=db_data)
        else:
            person = request.form.get("person")
            db_data = Facts.query.filter_by(person = person).all()
            return render_template('result.html', db_data=db_data)

@app.route('/read/<int:id>')
def read_more(id):
    '''
    Return html page where url contains
    primary key for particular record 
    in the database. On that html page
    the user will see a full text of
    a certain fact
    '''

    db_data = Facts.query.filter_by(id=id).first()
    return render_template("read_more.html", db_data=db_data)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
