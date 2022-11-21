from flask_sqlalchemy import SQLAlchemy
import pymysql 

from werkzeug.security import generate_password_hash, check_password_hash

import os

pymysql.install_as_MySQLdb()
db = SQLAlchemy()

def configure(app):

    DB_URI = os.getenv('DB_URI')
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

    db.init_app(app)
    app.db = db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    is_email_verified = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, default=True)
    joined_at = db.Column(db.DateTime, default=db.func.now())

    def hash_password(self, password) -> None:
        self.password = generate_password_hash(password)

    def check_password_hash(self, password) -> bool:
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_email_verified': self.is_email_verified,
            'is_active': self.is_active,
            'joined_at': self.joined_at
        }

    def __repr__(self):
        return f"<User> username={self.username}, email={self.email}"

    class PersonalData(db.Model):
        __tablename__ = 'personal_data'

        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        first_name = db.Column(db.String(100), nullable=False)
        last_name = db.Column(db.String(100), nullable=False)
        dob = db.Column(db.Date, nullable=False)

        def __repr__(self):
            return f"<PersonalData> user_id={self.user_id}, first_name={self.first_name}, last_name={self.last_name}, dob={self.dob}"
    
    class Address(db.Model):
        __tablename__ = 'address'

        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        street = db.Column(db.String(100), nullable=False)
        city = db.Column(db.String(100), nullable=False)
        state = db.Column(db.String(100), nullable=False)
        country = db.Column(db.String(100), nullable=False)
        postcode = db.Column(db.String(100), nullable=False)

    class Contact(db.Model):
        __tablename__ = 'contact'

        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        phone = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(100), nullable=False)

        def __repr__(self):
            return f"<Contact> user_id={self.user_id}, phone={self.phone}"
    
    class ResetPassword(db.Model):
        __tablename__ = 'reset_password'

        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        token = db.Column(db.String(100), nullable=False)
        expires_at = db.Column(db.DateTime, nullable=False)
        is_used = db.Column(db.Boolean, nullable=False, default=False)
        
        def __repr__(self):
            return f"<ResetPassword> user_id={self.user_id}, token={self.token}, expires_at={self.expires_at}, is_used={self.is_used}"
    

