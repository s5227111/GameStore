# Flask packages
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
import pymysql

# Others packages
from werkzeug.security import generate_password_hash, check_password_hash
import os
from typing import Union

# Instantiate db manager
pymysql.install_as_MySQLdb()
db = SQLAlchemy()

# Configure login manager
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id: int) -> Union[db.Model, None]:
    return UserQuery.get_user_by_id(user_id)


def configure(app, test_mode=False):

    if test_mode:
        DB_URI = "mysql://root:newcicle23@127.0.0.1/unittest_gamestore"
    else:
        DB_URI = "mysql://root:newcicle23@127.0.0.1/gs_user_data"

    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI

    db.init_app(app)
    login_manager.init_app(app)

    app.db = db
    app.login_manager = login_manager


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    is_email_verified = db.Column(db.Boolean, default=False)
    # is_active = db.Column(db.Boolean, default=False)
    joined_at = db.Column(db.DateTime, default=db.func.now())

    # Relationships one-to-one PersonalData
    personal_data = db.relationship("PersonalData", backref="users", uselist=False)

    # Relationships one-to-one Contact
    contact = db.relationship("Contact", backref="users", uselist=False)

    # Relationships one-to-one Address
    address = db.relationship("Address", backref="users", uselist=False)

    # Relationships one-to-one PasswordReset
    password_reset = db.relationship("PasswordReset", backref="users", uselist=False)

    # Relationships one-to-many Games
    my_games = db.relationship("myGames", backref="users")

    # Relationships one-to-many userCart
    user_cart = db.relationship("userCart", backref="users")

    def hash_password(self) -> None:
        self.password = generate_password_hash(self.password)

    def check_password_hash(self, password) -> bool:
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_email_verified": self.is_email_verified,
            "is_active": self.is_active,
            "joined_at": self.joined_at,
            "personal_data": self.personal_data.to_dict(),
            "contact": self.contact.to_dict(),
            "address": self.address.to_dict(),
            "password_reset": self.password_reset.to_dict(),
            "my_games": [game.to_dict() for game in self.my_games],
            "user_cart": [cart.to_dict() for cart in self.user_cart],
        }

    def save(self) -> Union[db.Model, None]:
        """
        Save user to database
        """

        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f"<User> username={self.username}, email={self.email}"


class PersonalData(db.Model):
    __tablename__ = "personal_data"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    dob = db.Column(db.Date)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "dob": self.dob,
        }

    def __repr__(self):
        return f"<PersonalData> user_id={self.user_id}, first_name={self.first_name}, last_name={self.last_name}, dob={self.dob}"


class Address(db.Model):
    __tablename__ = "address"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    address_1 = db.Column(db.String(100))
    address_2 = db.Column(db.String(100))
    town_city = db.Column(db.String(100))
    county = db.Column(db.String(100))
    postcode = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "address_1": self.address_1,
            "address_2": self.address_2,
            "town_city": self.town_city,
            "county": self.county,
            "postcode": self.postcode,
        }


class Contact(db.Model):
    __tablename__ = "contact"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    phone = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "phone": self.phone,
            "email": self.email,
        }

    def __repr__(self):
        return f"<Contact> user_id={self.user_id}, phone={self.phone}"


class PasswordReset(db.Model):
    __tablename__ = "reset_password"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    token = db.Column(db.String(100))
    expires_at = db.Column(db.DateTime)
    is_used = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "token": self.token,
            "expires_at": self.expires_at,
            "is_used": self.is_used,
        }

    def __repr__(self):
        return f"<ResetPassword> user_id={self.user_id}, token={self.token}, expires_at={self.expires_at}, is_used={self.is_used}"


class myGames(db.Model):
    __tablename__ = "my_games"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    game_id = db.Column(db.Integer, unique=True)
    added_at = db.Column(db.DateTime, default=db.func.now())
    is_downloaded = db.Column(db.Boolean, default=False)  # if the game is downloaded

    def to_dict(self) -> dict:
        my_games_dict = {
            "id": self.id,
            "user_id": self.user_id,
            "game_id": self.game_id,
            "added_at": self.added_at,
            "is_downloaded": self.is_downloaded,
        }
        return my_games_dict

    def __repr__(self):
        return f"<myGames> user_id={self.user_id}, game_id={self.game_id}"


class userCart(db.Model):
    """
    User cart
    """

    __tablename__ = "user_cart"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    game_id = db.Column(
        db.Integer, unique=True
    )  # game id is an id that refers to collection of games
    added_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self) -> dict:
        user_cart_dict = {
            "id": self.id,
            "user_id": self.user_id,
            "game_id": self.game_id,
            "added_at": self.added_at,
        }
        return user_cart_dict

    def __repr__(self):
        return f"<userCart> user_id={self.user_id}, game_id={self.game_id}"


class UserQuery:

    """
    Abstract class for search on the database
    """

    @staticmethod
    def get_user_by_email(email: str) -> Union[User, None]:
        query = (
            db.session.execute(db.select(User).where(User.email == email))
            .scalars()
            .first()
        )

        return query

    @staticmethod
    def get_user_by_username(username: str) -> Union[User, None]:
        query = (
            db.session.execute(db.select(User).where(User.username == username))
            .scalars()
            .first()
        )

        return query

    @staticmethod
    def get_user_by_username_or_email(username_or_email: str) -> Union[User, None]:
        query = (
            db.session.execute(
                db.select(User).where(
                    (User.username == username_or_email)
                    | (User.email == username_or_email)
                )
            )
            .scalars()
            .first()
        )

        return query

    @staticmethod
    def get_user_by_id(user_id: int) -> Union[User, None]:
        query = (
            db.session.execute(db.select(User).where(User.id == user_id))
            .scalars()
            .first()
        )

        return query
