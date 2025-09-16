# how to create a model


# import the model from this dir
# EXAMPLE
# from .user import User

# where user is something like
# from sqlmodel import Field, SQLModel
# from src.models.base import BaseMode
# class User(BaseModel, table=True):
#     __tablename__ = "users
#     username: str = Field(max_length=50, unique=True)
#     email: str = Field(max_length=100, unique=True)
#     is_active: bool = Field(default=True)


# then Generate migration: make alembic-make-migrations
# Apply migration: make alembic-migrate

# from .test import Test
# from .user import User

from .base import BaseModel  # noqa
from .user import User  # noqa
