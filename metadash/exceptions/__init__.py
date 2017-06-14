"""
Some built in Exceptions
"""


class MetadashException(Exception):
    pass


class CriticalError(Exception):
    pass


class ConfigError(MetadashException):
    pass


class AuthError(MetadashException):
    pass


class RemoteServerError(MetadashException):
    pass


class DependencyError(MetadashException):
    pass
