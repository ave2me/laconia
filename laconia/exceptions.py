class LaconiaError(Exception):
    """
    Base class for any custom exceptions.
    """


class KeyExistsError(LaconiaError):
    """
    Error raised when trying to overwrite an existing key.
    """
