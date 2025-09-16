class BaseBackendException(Exception):
    pass


class ObjectNotFound(BaseBackendException):
    pass


class RepositoryError(BaseBackendException):
    pass
