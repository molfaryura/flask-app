'''
WebApp on Flask and SQLAlchemy.
In this app the user can store and get 
data from the database about two
people, who are widely known in
narrow circles
'''

import os

from flask import Flask, render_template, request, redirect

from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv


load_dotenv()

password = os.environ.get('DB_password')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{password}@localhost/my_db'

db = SQLAlchemy(app)

class Facts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable = False)
    text = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    person = db.Column(db.String, nullable=False)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    fact = db.relationship('Facts', backref='author')


def post_fact(template, page):
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        author = request.form['author']
        person = request.form['person']

        author_data = Author(name=author)

        facts_data = Facts(title=title,
                        text=text, author=author_data, person=person)

        try:
            db.session.add_all([facts_data, author_data])
            db.session.commit()
            redirect(page)
        except:
            return 'Failed to connect to the database :('
    return render_template(template)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/shavkoon')
def shavk():
    return render_template('post_shavk.html')

@app.route('/vasyl')
def vasyl():
    return render_template('post_vasyl.html')

@app.route('/donate')
def donate():
    return render_template('donate.html')

@app.route('/post/shavkoon', methods=['POST', 'GET'])
def post_shavk():
    return post_fact('post_shavk.html', '/shavkoon')

@app.route('/post/vasyl', methods=['POST', 'GET'])
def post_vasyl():
    return post_fact('post_vasyl.html','/vasyl')



@app.route('/read', methods=['POST', 'GET'])
def read():
    '''
    The user selects a person about whom he wants to get facts
    It connects to the database and show all facts on the separate html page
    '''

    if request.method == 'GET':
        return render_template('read.html')
    elif request.method == 'POST':
        if request.form.get("person") != 'all':
            person = request.form.get("person")
            db_data = Facts.query.filter_by(person = person).all()
            return render_template('result.html', db_data=db_data)
        else:
            db_data = Facts.query.all()
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


if __name__ == '__main__':
    app.run(debug=True)
