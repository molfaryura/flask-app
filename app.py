"""WebApp on Flask and SQLAlchemy. In this app the user can store and get
data from the database about two people, who are widely known in narrow circles
"""

import os

from flask import Flask, render_template, request, redirect, flash

from dotenv import load_dotenv

from flask_login import login_required, current_user, login_user, logout_user

from models import Facts, Users, login, db

load_dotenv()

db_password = os.environ.get('DB_password')

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{db_password}@localhost/my_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = os.environ.get('Secret_key')

db.init_app(app)

login.init_app(app)
login.login_view = 'login_'


first_answer = os.environ.get('First_answer')
second_answer = os.environ.get('Second_answer')

@app.before_first_request
def create_table():
    """Creates table if not exists"""
    db.create_all()


def post_fact(template, page):
    """ Handle POST request to post a fact to the database.

    param template (str): The name of the template to render if the request method is not POST.
    param page (str): The URL path to redirect to after successfully posting a fact.

    returns:
             If the request method is not POST, render the specified template.
             If successfully posted a fact, redirect to the specified page.
             If failed to connect to the database, return an error message.
    """
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
            return redirect(page)
        except:
            return 'Failed to connect to the database :('
    return render_template(template)


@app.route('/')
def index():
    """Returns the main page"""
    return render_template('index.html')

@app.route('/login', methods = ['POST', 'GET'])
def login_():
    """ Handle user login.

    returns:
        redirect: If the user is already authenticated, redirect to the home page.
        redirect: Home page if the request method is POST and the email and password are correct.
        redirect: Login page with an error flash message if the email or password is incorrect.
        render_template: If the request method is not POST, render the login template.
    """
    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        email = request.form['email']
        user = Users.query.filter_by(email=email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/')

        flash('Email or Password is incorrect!')
        return redirect('/login')

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    """ Handle user registration.

    returns:
        redirect: If the user is already authenticated, redirect to the home page.
        redirect: Home page if the request method is POST and the registration is successful.
        redirect: Registration page with an error flash message if a user already exists.
        redirect: Registration page with an error flash message if the passwords do not match.
        redirect: If the security question answer is invalid, redirect to a YouTube link.
        render_template: If the request method is not POST, render the registration template.
    """
    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        repeat_password = request.form['repeat_password']
        question = request.form['question']


        if Users.query.filter_by(email=email).all():
            flash('A user with this email already exists')
            return redirect('/register')

        if password != repeat_password:
            flash('Passwords must match')
            return redirect('/register')

        if question not in (first_answer, second_answer):
            return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

        user = Users(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template('register.html')

@app.route('/about')
def about():
    """Return about page"""
    return render_template('about.html')

@app.route('/donate')
def donate():
    """Return donate page"""
    return render_template('donate.html')

@app.route('/post/shavkoon', methods=['POST', 'GET'])
@login_required
def post_shavk():
    """Return post_shavk.html page"""
    return post_fact('post_shavk.html', '/post/shavkoon')

@app.route('/post/vasyl', methods=['POST', 'GET'])
@login_required
def post_vasyl():
    """Return post_vasyl.html page"""
    return post_fact('post_vasyl.html','/post/vasyl')

@app.route('/resource')
def resource():
    """Return resource page"""
    return render_template('resource.html')

@app.route('/team')
def team():
    """Return team page"""
    return render_template('team.html')

@app.route('/contact')
def contact():
    """Return contact page"""
    return render_template('contact.html')

@app.route('/read', methods=['POST', 'GET'])
def read():
    """Handle GET and POST requests for the '/read' URL.

    returns:
        response:
            Rendered HTML template as response for GET requests,
            or filtered data rendered in result.html template for POST requests.
    """

    if request.method == 'GET':
        return render_template('read.html')
    if request.method == 'POST' and request.form.get("person") == 'All':
        db_data = Facts.query.all()
        return render_template('result.html', db_data=db_data)
    person = request.form.get("person")
    db_data = Facts.query.filter_by(person = person).all()
    return render_template('result.html', db_data=db_data)

@app.route('/read/<int:page_id>')
def read_more(page_id):
    """Handle GET requests for the '/read/<page_id>' URL.

    param page_id (int): The page ID to retrieve data from the database.

    returns:
        response: Rendered HTML template with data retrieved from the database.
    """

    db_data = Facts.query.filter_by(id=page_id).first()
    return render_template("read_more.html", db_data=db_data)

@app.route('/logout')
def logout():
    """Handle GET requests for the '/logout' URL.

    returns:
        response: Redirects to the home page ('/') after logging out the user.
    """
    logout_user()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
