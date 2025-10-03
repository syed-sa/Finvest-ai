class BaseBackendException(Exception):
    status_code: int = 500
    message: str = "An error occurred"
    detail: str = "An unexpected error occured. Please contact support."
    status: bool = False

    def __init__(self, message: str | None = None, detail: str | None = None):
        super().__init__(message or self.message)
        self.message = message or self.message
        self.detail = detail or self.detail


class ObjectNotFound(BaseBackendException):
    status_code = 404
    message = "Resource not found"

class RepositoryError(BaseBackendException):
    status_code = 500
    message = "Database error"
    
class UnAuthorized(BaseBackendException):
    status_code = 401
    message = "Unauthorized access"


class Forbidden(BaseBackendException):
    status_code = 403
    message = "Forbidden access"

class BadRequest(BaseBackendException):
    status_code = 400
    message = "Bad request"
    detail = "Invalid input provided."

class Conflict(BaseBackendException):
    status_code = 409
    message = "Conflict"
    detail = "The resource already exists or has a conflict."
