# verify data input 
from marshmallow import Schema, fields, validate, ValidationError
from typing import Union

from models import User

class UserSchema(Schema):

    """ User Schema """

    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(min=4, max=25))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6, max=25))
    is_email_verified = fields.Boolean(dump_only=True)
    is_active = fields.Boolean(dump_only=True)
    joined_at = fields.DateTime(dump_only=True)

    # class Meta:
    #     ordered = True

    # @staticmethod
    # def validate_username(username: str) -> Union[ValidationError, None]:
    #     if User.query.filter_by(username=username).first():
    #         raise ValidationError('Username already exists')

    # @staticmethod
    # def validate_email(email: str) -> Union[ValidationError, None]:
    #     if User.query.filter_by(email=email).first():
    #         raise ValidationError('Email already exists')

    # function that loads after all the data is validated
    @post_load
    def create_user(self, data, **kwargs) -> Union[User, ValidationError]:
        """ Create User """

        return User(**data)