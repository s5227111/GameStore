# Flask packages
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
import pymysql

# Others packages
from werkzeug.security import generate_password_hash, check_password_hash
import os
from typing import Union
from datetime import datetime

from marshmallow import ValidationError


# Instantiate db manager
pymysql.install_as_MySQLdb()
db = SQLAlchemy()

# Configure login manager
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id: int) -> Union[db.Model, None]:  # type: ignore
    return User.query.get(user_id)


def configure(app, test_mode=False):

    if test_mode:
        DB_URI = "mysql://root:1234@127.0.0.1/unittest"
    else:
        DB_URI = "mysql://root:1234@34.89.56.248/gamestore"

    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI

    db.init_app(app)
    login_manager.init_app(app)

    app.db = db
    app.login_manager = login_manager


class User(db.Model, UserMixin):  # type: ignore
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    joined_at = db.Column(db.DateTime, default=db.func.now())
    is_email_verified = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships one-to-one PersonalData
    personal_data = db.relationship("PersonalData", backref="users", uselist=False)

    # Relationships one-to-one Contact
    contact = db.relationship("Contact", backref="users", uselist=False)

    # Relationships one-to-one Address
    address = db.relationship("Address", backref="users", uselist=False)

    # Relationships one-to-many PasswordReset
    password_reset = db.relationship("PasswordReset", backref="users")

    # Relationships one-to-many Games
    my_games = db.relationship("myGames", backref="users")

    # Relationships one-to-many userCart
    user_cart = db.relationship("userCart", backref="users")

    # Relationships one-to-many starredGames
    upvotes = db.relationship("Upvotes", backref="users")

    # Relationships one-to-many productsHistory
    products_history = db.relationship("productsHistory", backref="users")

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
            "password_reset": [reset.to_dict() for reset in self.password_reset],
            "my_games": [game.to_dict() for game in self.my_games],
            "user_cart": [cart.to_dict() for cart in self.user_cart],
            "upvotes": [game.to_dict() for game in self.upvotes],
            "products_history": [
                history.to_dict() for history in self.products_history
            ],
        }

    def save(self) -> Union[db.Model, None]:  # type: ignore
        """
        Save user to database
        """

        db.session.add(self)
        db.session.commit()
        return self

    def add_products_history(self, product_id: int) -> None:
        """
        Add product to products history
        """

        # Check if product is already in history
        for history in self.products_history:
            if history.game_id == product_id:
                return None

        history = productsHistory(user_id=self.id, game_id=product_id)
        self.products_history.append(history)

        # history is limited to 5 products
        if len(self.products_history) >= 5:
            self.products_history.pop(0)

        db.session.add(history)
        db.session.commit()

    def __repr__(self):
        return f"<User> username={self.username}, email={self.email}"


class PersonalData(db.Model):  # type: ignore for some reason mypy is not happy with this
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
            "is_empty": self.check_if_empty(),
        }

    def check_if_empty(self) -> bool:

        """
        Check if all fields are empty
        This functions is used in profile page to check if user has filled in personal data
        """
        if not self.first_name or not self.last_name or not self.dob:
            return True
        return False

    def __repr__(self):
        return f"<PersonalData> user_id={self.user_id}, first_name={self.first_name}, last_name={self.last_name}, dob={self.dob}"


class Address(db.Model):  # type: ignore for some reason mypy is not happy with this
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


class Contact(db.Model):  # type: ignore for some reason mypy is not happy with this
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


class PasswordReset(db.Model):  # type: ignore for some reason mypy is not happy with this
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


class myGames(db.Model):  # type: ignore for some reason mypy is not happy with this
    __tablename__ = "my_games"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    game_id = db.Column(db.Integer)
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


class userCart(db.Model):  # type: ignore for some reason mypy is not happy with this
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


class Upvotes(db.Model):  # type: ignore for some reason mypy is not happy with this

    __tablename__ = "upvotes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    game_id = db.Column(db.Integer)
    added_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self) -> dict:
        starred_games_dict = {
            "id": self.id,
            "user_id": self.user_id,
            "game_id": self.game_id,
            "added_at": self.added_at,
        }
        return starred_games_dict

    def __repr__(self):
        return f"<starred_games> user_id={self.user_id}, game_id={self.game_id}"


class productsHistory(db.Model):  # type: ignore for some reason mypy is not happy with this

    __tablename__ = "products_history"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    game_id = db.Column(db.Integer)
    added_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self) -> dict:
        products_history_dict = {
            "id": self.id,
            "user_id": self.user_id,
            "game_id": self.game_id,
            "added_at": self.added_at,
        }
        return products_history_dict


class UserQuery:

    """
    Abstract class for search on the database
    """

    @staticmethod
    def update_login_data(user_id: int, data: dict) -> None:

        """
        Update user login data. The data is already validated, so we just need to check
        if the email or username is already in use and password is correct
        """

        user = User.query.filter_by(id=user_id).first()

        # check if password is the same that is registered and remove it from the data
        if "password" in data:
            if not user.check_password_hash(data["password"]):
                raise ValidationError("Password is not correct")
            del data["password"]

        for k, v in data.items():
            # check if email is the one to be updated
            if k == "email":
                # check if email is already in the database
                if User.query.filter_by(email=v).first():
                    raise ValidationError("Email already in use")

            elif k == "username":
                if User.query.filter_by(username=v).first():
                    raise ValidationError("Username already in use")

            # update the user data
            setattr(user, k, v)

        db.session.commit()

    @staticmethod
    def update_personal_data(user_id: int, data: dict) -> None:

        """
        Update the user personal data. The data is validated before, so we can just update the data
        """

        user = User.query.filter_by(id=user_id).first()
        personal_data = user.personal_data

        for k, v in data.items():
            # update the user data
            # if k is dob, we need to convert it to datetime
            if k == "dob":
                v = datetime.strptime(v, "%Y-%m-%d")

            setattr(personal_data, k, v)

        db.session.commit()

    @staticmethod
    def update_contact_data(user_id: int, data: dict) -> None:
        # Update the user contact data

        user = User.query.filter_by(id=user_id).first()

        for k, v in data.items():
            # update the user data
            setattr(user.contact, k, v)

        db.session.commit()

    @staticmethod
    def update_address_data(user_id: int, data: dict) -> None:
        # Update the user address data

        user = User.query.filter_by(id=user_id).first()

        for k, v in data.items():
            # update the user data
            setattr(user.address, k, v)

        db.session.commit()
