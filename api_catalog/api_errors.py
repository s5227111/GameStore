class BaseError(Exception):
    """Base class for all errors in this module."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message


class MissingRequiredField(BaseError):
    """Missing required field in the request body"""


class InvalidField(BaseError):
    """Invalid field in the request body"""


class UnexpectedFieldError(BaseError):
    """Unexpected field in the request body"""


class DuplicateGameIdError(BaseError):
    """Duplicate game_id in the request body"""
