from flask_sqlalchemy import SQLAlchemy
import pymysql 

from werkzeug.security import generate_password_hash, check_password_hash

import os

from typing import Union

pymysql.install_as_MySQLdb()
db = SQLAlchemy()

def configure(app, test_mode=False):

    if test_mode:
        DB_URI = "mysql://root:newcicle23@127.0.0.1/unittest_gamestore"
    else:
        DB_URI = "mysql://root:newcicle23@127.0.0.1/gs_user_data"

    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

    db.init_app(app)
    app.db = db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    is_email_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    joined_at = db.Column(db.DateTime, default=db.func.now())
    

    # Relationships one-to-one PersonalData
    personal_data = db.relationship('PersonalData', backref='users', uselist=False)

    # Relationships one-to-one Contact
    contact = db.relationship('Contact', backref='users', uselist=False)

    # Relationships one-to-one Address
    address = db.relationship('Address', backref='users', uselist=False)

    # Relationships one-to-one PasswordReset
    password_reset = db.relationship('PasswordReset', backref='users', uselist=False)


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

class PasswordReset(db.Model):
    __tablename__ = 'reset_password'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(100), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, nullable=False, default=False)
    
    def __repr__(self):
        return f"<ResetPassword> user_id={self.user_id}, token={self.token}, expires_at={self.expires_at}, is_used={self.is_used}"

class UserQuery():

    """
    Abstract class for search on the database
    """

    @staticmethod
    def get_user_by_email(email: str) -> Union[User, None]:
        query = (db.session.execute(db.select(User).where(User.email == email))
        .scalars()
        .first()
        )

        return query
    
    @staticmethod
    def get_user_by_username(username: str) -> Union[User, None]:
        query = (db.session.execute(db.select(User).where(User.username == username))
        .scalars()
        .first()
        )

        return query
    
    @staticmethod
    def get_user_by_username_or_email(username_or_email: str) -> Union[User, None]:
        query = (db.session.execute(db.select(User).where(username_or_email in (User.username, User.email)))
        .scalars()
        .first()
        )

        return query
