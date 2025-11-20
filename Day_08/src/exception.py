

class BooklyException(Exception):
    """
        This is the base class for all bookly error
    """
    pass


class InvalidToken(BooklyException):
    """
        User has provided an invalid or expired token
    """
    pass


class RevokeToken(BooklyException):
    """
        User has provided an token which is revoked
    """
    pass


class AccessTokenRequired(BooklyException):
    """
        User has provied a refresh token when an access token is needed
    """
    pass


class RefreshTokenRequired(BooklyException):
    """
        User has provied an access token when an refresh token is need
    """
    pass


class UserAlreadyExists(BooklyException):
    """
        User has provided an email for a user who exists during sign up
    """
    pass


class InsufficientPermission(BooklyException):
    """
        User do not has the neccessary permissions to perform an action.
    """
    pass


class InvalidCredentials(BooklyException):
    """
        User has provided wrong email or password during login
    """
    pass


class BookNotFound(BooklyException):
    """
        Book Not Found
    """
    pass


class TagNotFound(BooklyException):
    """
        Tag Not Found
    """
    pass


class TagAlreadyExists(BooklyException):
    """
        Tag Already Exists
    """
    pass


class UserNotFound(BooklyException):
    """
        User not Found
    """
    pass


class AccountNotVerified(Exception):
    """
        Account not yet verified
    """
    pass
