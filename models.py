'''Database structure with two tables for facts and user's
credentials with one to many relationship
'''

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin, LoginManager

login = LoginManager()

db = SQLAlchemy()

class Facts(db.Model):
    """ Model for the 'facts' table in the database.

    Attributes:
        id (int): Unique identifier for a fact.
        title (str): Title of the fact.
        text (str): Text of the fact.
        author_id (int): Foreign key referencing the 'id' of the user who authored the fact.
        person (str): Name of the person to whom the fact pertains.
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable = False)
    text = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    person = db.Column(db.String(255), nullable=False)

class Users(UserMixin, db.Model):
    """ Model for the 'users' table in the database.

    Attributes:
        id (int): Unique identifier for a user.
        email (str): Email address of the user. Must be unique.
        username (str): Username of the user.
        password_hash (str): Hashed password of the user.
        fact (relationship): One-to-many relationship with the 'Facts' model.
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable = False)
    username = db.Column(db.String(100), nullable = False)
    password_hash = db.Column(db.String(128), nullable = False)
    fact = db.relationship('Facts', backref='author')

    def set_password(self,password):
        """Set the password for the user.

        param password (str): Plain text password.

        returns: None
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        """Check if the provided password matches the stored password hash.

        param password (str): Plain text password to check against the stored hash.

        returns: bool
        """
        return check_password_hash(self.password_hash,password)

@login.user_loader
def load_user(user_id):
    """ Load a user from the database based on the provided user ID.

    param user_id (int): The ID of the user to load.

    returns: The User object associated with the provided user ID, or None if not found.
    """
    return Users.query.get(int(user_id))
