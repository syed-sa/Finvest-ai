from typing import Optional

import pytest
from fastapi_pagination import Params, set_params
from sqlmodel import Field, SQLModel

from src.core.exceptions import ObjectNotFound
from src.repositories.sqlalchemy import BaseSQLAlchemyRepository


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    is_active: bool = True


class UserCreate(SQLModel):
    name: str
    email: str
    is_active: bool = True


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None


# Concrete Class for testing
class UserRepository(BaseSQLAlchemyRepository[User, UserCreate, UserUpdate]):
    _model = User


@pytest.mark.asyncio
async def test_create_user(db_session, setup_test_db):
    """Test creating a user"""
    user_repo = UserRepository(db_session)

    user_data = UserCreate(name="John Doe", email="john@example.com")
    created_user = await user_repo.create(user_data)

    assert created_user.id is not None
    assert created_user.name == "John Doe"
    assert created_user.email == "john@example.com"
    assert created_user.is_active is True


@pytest.mark.asyncio
async def test_get_user(db_session, setup_test_db):
    """Test getting a user by criteria"""
    user_repo = UserRepository(db_session)

    user_data = UserCreate(name="Jane Doe", email="jane@example.com")
    created_user = await user_repo.create(user_data)

    found_user = await user_repo.get(email="jane@example.com")
    assert found_user.id == created_user.id
    assert found_user.name == "Jane Doe"


@pytest.mark.asyncio
async def test_update_user(db_session, setup_test_db):
    """Test updating a user"""
    user_repo = UserRepository(db_session)

    user_data = UserCreate(name="Bob Smith", email="bob@example.com")
    created_user = await user_repo.create(user_data)

    update_data = UserUpdate(name="Robert Smith")
    updated_user = await user_repo.update(created_user, update_data)

    assert updated_user.name == "Robert Smith"
    assert updated_user.email == "bob@example.com"  # Should remain unchanged


@pytest.mark.asyncio
async def test_delete_user(db_session, setup_test_db):
    """Test deleting a user"""
    user_repo = UserRepository(db_session)

    user_data = UserCreate(name="Delete Me", email="delete@example.com")
    created_user = await user_repo.create(user_data)

    await user_repo.delete(id=created_user.id)

    with pytest.raises(ObjectNotFound):
        await user_repo.get(id=created_user.id)


@pytest.mark.asyncio
async def test_paginate(db_session, setup_test_db):
    """Test pagination functionality"""
    user_repo = UserRepository(db_session)
    set_params(Params(size=10, page=1))

    for i in range(10):
        user_data = UserCreate(name=f"User {i}", email=f"user{i}@example.com")
        await user_repo.create(user_data)

    page_result = await user_repo.paginate(sort_field="name", sort_order="asc")

    assert len(page_result.items) == 10
    assert page_result.total == 10
    assert page_result.items[0].name == "User 0"


@pytest.mark.asyncio
async def test_all_users(db_session, setup_test_db):
    """Test getting all users with pagination"""
    user_repo = UserRepository(db_session)

    for i in range(3):
        user_data = UserCreate(name=f"User {i}", email=f"user{i}@example.com")
        await user_repo.create(user_data)

    all_users = await user_repo.all(limit=10, sort_field="name", sort_order="asc")

    assert len(all_users) == 3
    assert all_users[0].name == "User 0"


@pytest.mark.asyncio
async def test_filter_users(db_session, setup_test_db):
    """Test filtering users with the f() method"""
    user_repo = UserRepository(db_session)

    active_user = UserCreate(name="Active User", email="active@example.com", is_active=True)
    inactive_user = UserCreate(name="Inactive User", email="inactive@example.com", is_active=False)

    await user_repo.create(active_user)
    await user_repo.create(inactive_user)

    active_users = await user_repo.f(is_active=True)
    assert len(active_users) == 1
    assert active_users[0].name == "Active User"


@pytest.mark.asyncio
async def test_get_or_create(db_session, setup_test_db):
    """Test get_or_create functionality"""
    user_repo = UserRepository(db_session)

    user_data = UserCreate(name="Get Or Create", email="getorcreate@example.com")

    user1 = await user_repo.get_or_create(user_data, email="getorcreate@example.com")
    assert user1.id is not None

    user2 = await user_repo.get_or_create(user_data, email="getorcreate@example.com")
    assert user1.id == user2.id


def test_repository_initialization(db_session):
    """Test that repository can be initialized properly"""
    user_repo = UserRepository(db_session)

    assert user_repo.db == db_session
    assert user_repo._model == User