from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()

def connect_db(app):
	db.app = app
	db.init_app(app)

bcrypt = Bcrypt()

class User(db.Model):
    """This is the class model for user"""

    __tablename__ = 'users'

    def __repr__(self):
        p = self
        return f"<User username={p.username} password={p.password}>"

    username =  db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text,  nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    feedback = db.relationship('Feedback', backref='users', passive_deletes=True)
    
    def serialize(self):
        return {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name
        }
    
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Create User instance with a hashed password and return the instance"""
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode('utf8')
        
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """Validate that the user exist and the password is correct
        Return user if valid, else return false
        """
        current_user = User.query.filter_by(username=username).first()
        if current_user and bcrypt.check_password_hash(current_user.password, password):
            return current_user
        else:
            return False

class Feedback(db.Model):
    """This is the class model for feedback"""

    __tablename__ = 'feedback'

    def __repr__(self):
        p = self
        return f"<User username={p.username} title={p.title}>"

    id =  db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100),  nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(30), db.ForeignKey('users.username', ondelete='CASCADE'), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'username': self.username
        }
        
    @classmethod
    def add(cls, title, content, username):
        return cls(title=title, content=content, username=username)





