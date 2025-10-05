# pragma: no cover start
from enum import Enum


class BaseEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)


class SortOrder(BaseEnum):
    ASC = "asc"
    DESC = "desc"


class Environment(BaseEnum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class MessageState(str, Enum):
    FAILED = "FAILED"
    FULFILLED = "FULFILLED"
    PENDING = "PENDING"


# pragma: no cover stop
