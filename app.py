import os

from flask import Flask, render_template

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

class Author(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    fact = db.relationship('Facts', backref='author')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/donate')
def donate():
    return render_template('donate.html')

@app.route('/post/shavk', methods=['POST', 'GET'])
def post_shavk():
    return render_template('post_shavk.html')

@app.route('/post/vasyl', methods=['POST', 'GET'])
def post_vasyl():
    return render_template('post_vasyl.html')

if __name__ == '__main__':
    app.run(debug=True)
