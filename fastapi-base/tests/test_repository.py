from typing import Optional

import pytest
from fastapi_pagination import Params, set_params
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Field, SQLModel

from src.core.exceptions import ObjectNotFound
from src.models.base import BaseModel
from src.repositories.sqlalchemy import BaseSQLAlchemyRepository


class BaseTest(BaseModel, table=True):
    __tablename__ = "test"

    email: str = Field(unique=True, index=True, max_length=255)
    name: str = Field(max_length=100)
    is_active: bool = Field(default=True)


# For creating users (input validation)
class BaseTestCreate(SQLModel):
    email: str = Field(max_length=255)
    name: str = Field(max_length=100)
    is_active: bool = Field(default=True)


class BaseTestUpdate(SQLModel):
    email: Optional[str] = Field(default=None, max_length=255)
    name: Optional[str] = Field(default=None, max_length=100)
    is_active: Optional[bool] = Field(default=None)


# Concrete Class for testing
class BaseTestRepository(BaseSQLAlchemyRepository[BaseTest, BaseTestCreate, BaseTestUpdate]):
    _model = BaseTest


@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession) -> None:
    """Test creating a user"""
    user_repo = BaseTestRepository(db_session)

    user_data = BaseTestCreate(name="John Doe", email="john@example.com")
    created_user = await user_repo.create(user_data)

    assert created_user.id is not None
    assert created_user.name == "John Doe"
    assert created_user.email == "john@example.com"
    assert created_user.is_active is True


@pytest.mark.asyncio
async def test_get_user(db_session: AsyncSession) -> None:
    """Test getting a user by criteria"""
    user_repo = BaseTestRepository(db_session)

    user_data = BaseTestCreate(name="Jane Doe", email="jane@example.com")
    created_user = await user_repo.create(user_data)

    found_user = await user_repo.get(email="jane@example.com")
    if not found_user:
        raise AssertionError("User not found")

    assert found_user.id == created_user.id
    assert found_user.name == "Jane Doe"


@pytest.mark.asyncio
async def test_update_user(db_session: AsyncSession) -> None:
    """Test updating a user"""
    user_repo = BaseTestRepository(db_session)

    user_data = BaseTestCreate(name="Bob Smith", email="bob@example.com")
    created_user = await user_repo.create(user_data)

    update_data = BaseTestUpdate(name="Robert Smith")
    updated_user = await user_repo.update(created_user, update_data)

    assert updated_user.name == "Robert Smith"
    assert updated_user.email == "bob@example.com"  # Should remain unchanged


@pytest.mark.asyncio
async def test_delete_user(db_session: AsyncSession) -> None:
    """Test deleting a user"""
    user_repo = BaseTestRepository(db_session)

    user_data = BaseTestCreate(name="Delete Me", email="delete@example.com")
    created_user = await user_repo.create(user_data)

    await user_repo.delete(id=created_user.id)

    with pytest.raises(ObjectNotFound):
        await user_repo.get(id=created_user.id)


@pytest.mark.asyncio
async def test_paginate(db_session: AsyncSession) -> None:
    """Test pagination functionality"""
    user_repo = BaseTestRepository(db_session)
    set_params(Params(size=10, page=1))

    for i in range(10):
        user_data = BaseTestCreate(name=f"User {i}", email=f"user{i}@example.com")
        await user_repo.create(user_data)

    page_result = await user_repo.paginate(sort_field="name", sort_order="asc")

    assert len(page_result.items) == 10
    assert page_result.total == 10
    assert page_result.items[0].name == "User 0"


@pytest.mark.asyncio
async def test_all_users(db_session: AsyncSession) -> None:
    """Test getting all users with pagination"""
    user_repo = BaseTestRepository(db_session)

    for i in range(3):
        user_data = BaseTestCreate(name=f"User {i}", email=f"user{i}@example.com")
        await user_repo.create(user_data)

    all_users = await user_repo.all(limit=10, sort_field="name", sort_order="asc")

    assert len(all_users) == 3
    assert all_users[0].name == "User 0"


@pytest.mark.asyncio
async def test_filter_users(db_session: AsyncSession) -> None:
    """Test filtering users with the f() method"""
    user_repo = BaseTestRepository(db_session)

    active_user = BaseTestCreate(name="Active User", email="active@example.com", is_active=True)
    inactive_user = BaseTestCreate(
        name="Inactive User", email="inactive@example.com", is_active=False
    )

    await user_repo.create(active_user)
    await user_repo.create(inactive_user)

    active_users = await user_repo.f(is_active=True)
    assert len(active_users) == 1
    assert active_users[0].name == "Active User"


@pytest.mark.asyncio
async def test_get_or_create(db_session: AsyncSession) -> None:
    """Test get_or_create functionality"""
    user_repo = BaseTestRepository(db_session)

    user_data = BaseTestCreate(name="Get Or Create", email="getorcreate@example.com")

    user1 = await user_repo.get_or_create(user_data, email="getorcreate@example.com")
    assert user1.id is not None

    user2 = await user_repo.get_or_create(user_data, email="getorcreate@example.com")
    assert user1.id == user2.id


def test_repository_initialization(db_session: AsyncSession) -> None:
    """Test that repository can be initialized properly"""
    user_repo = BaseTestRepository(db_session)

    assert user_repo.db == db_session
    assert user_repo._model == BaseTest
