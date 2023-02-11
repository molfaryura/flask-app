'''Database structure with two
    tables for facts and user's
    credentials with one to many
    relationship
'''

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin, LoginManager


login = LoginManager()


db = SQLAlchemy()

class Facts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable = False)
    text = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    person = db.Column(db.String, nullable=False)

class UserModel(UserMixin, db.Model):
    '''Create table for 
       the registration
    '''
    __tablename__ = 'users'
 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String())
    fact = db.relationship('Facts', backref='author')
 
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
     
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))
