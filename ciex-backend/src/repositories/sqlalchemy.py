import logging
from typing import Any, Generic, List, Optional, Type, TypeVar

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select

from src.core.exceptions import ObjectNotFound
from src.interfaces.repository import IRepository


ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)
logger: logging.Logger = logging.getLogger(__name__)


class BaseSQLAlchemyRepository(IRepository, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    A generic async SQLAlchemy repository base class that provides common CRUD operations.

    This class serves as a foundation for all repository classes, providing standardized
    methods for database operations while maintaining type safety through generics.

    Type Parameters:
        ModelType: The SQLModel database model class
        CreateSchemaType: The Pydantic model for creating new objects
        UpdateSchemaType: The Pydantic model for updating existing objects

    Example:
        >>> from sqlmodel import SQLModel, Field
        >>> from pydantic import BaseModel
        >>>
        >>> class User(SQLModel, table=True):
        ...     id: int = Field(primary_key=True)
        ...     name: str
        ...     email: str
        ...
        >>> class UserCreate(BaseModel):
        ...     name: str
        ...     email: str
        ...
        >>> class UserUpdate(BaseModel):
        ...     name: Optional[str] = None
        ...     email: Optional[str] = None
        ...
        >>> class UserRepository(BaseSQLAlchemyRepository[User, UserCreate, UserUpdate]):
        ...     _model = User
        ...
        >>> # Usage
        >>> user_repo = UserRepository(async_db_session)
        >>> new_user = await user_repo.create(UserCreate(name="John", email="john@example.com"))
    """

    _model: Type[ModelType]

    def __init__(self, db: AsyncSession) -> None:
        """
        Initialize the repository with a database session.

        Args:
            db: SQLAlchemy async database session

        Example:
            >>> from sqlalchemy.ext.asyncio import AsyncSession
            >>> user_repo = UserRepository(async_db_session)
        """
        self.db = db

    async def create(self, obj_in: CreateSchemaType, **kwargs: Any) -> ModelType:
        """
        Create a new object in the database.

        Args:
            obj_in: The create schema containing the data for the new object
            **kwargs: Additional options:
                - add (bool): Whether to add the object to the session (default: True)
                - flush (bool): Whether to flush the session (default: True)
                - commit (bool): Whether to commit the transaction (default: True)

        Returns:
            The created database object

        Raises:
            Exception: If database operation fails, rolls back the transaction

        Example:
            >>> user_data = UserCreate(name="Alice", email="alice@example.com")
            >>> new_user = await user_repo.create(user_data)
            >>> print(new_user.id)  # Auto-generated ID

            >>> # Create without committing (useful for batch operations)
            >>> user = await user_repo.create(user_data, commit=False)
        """
        logger.info(f"Inserting new object[{obj_in.__class__.__name__}]")

        db_obj = self._model.model_validate(obj_in)
        add = kwargs.get("add", True)
        flush = kwargs.get("flush", True)
        commit = kwargs.get("commit", True)

        if add:
            self.db.add(db_obj)

        # Navigate these with caution
        if add and commit:
            try:
                await self.db.commit()
                await self.db.refresh(db_obj)
            except Exception as exc:
                logger.error(exc)
                await self.db.rollback()

        elif add and flush:
            await self.db.flush()

        return db_obj

    async def get(self, **kwargs: Any) -> Optional[ModelType]:
        """
        Get a single object by filter criteria.

        Args:
            **kwargs: Filter criteria as key-value pairs

        Returns:
            The found object or None

        Raises:
            ObjectNotFound: If no object matches the criteria

        Example:
            >>> # Get user by ID
            >>> user = await user_repo.get(id=1)

            >>> # Get user by email
            >>> user = await user_repo.get(email="john@example.com")

            >>> # Get user by multiple criteria
            >>> user = await user_repo.get(name="John", is_active=True)
        """
        logger.info(f"Fetching [{self._model.__class__.__name__}] object by [{kwargs}]")

        query = select(self._model).filter_by(**kwargs)  # type: ignore
        response = await self.db.execute(query)
        scalar: Optional[ModelType] = response.scalar_one_or_none()

        if not scalar:
            raise ObjectNotFound(f"Object with [{kwargs}] not found.")

        return scalar

    async def update(self, obj_current: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        """
        Update an existing object in the database.

        Only fields that are explicitly set in the update schema will be modified.
        Unset fields are ignored to support partial updates.

        Args:
            obj_current: The current database object to update
            obj_in: The update schema containing the new data

        Returns:
            The updated database object

        Example:
            >>> # Get existing user
            >>> user = await user_repo.get(id=1)

            >>> # Update only the name (email remains unchanged)
            >>> update_data = UserUpdate(name="John Smith")
            >>> updated_user = await user_repo.update(user, update_data)

            >>> # Update multiple fields
            >>> update_data = UserUpdate(name="Jane", email="jane@example.com")
            >>> updated_user = await user_repo.update(user, update_data)
        """
        logger.info(f"Updating [{self._model.__class__.__name__}] object with [{obj_in}]")

        update_data = obj_in.model_dump(
            exclude_unset=True
        )  # This tells Pydantic to not include the values that were not sent

        for field in update_data:
            setattr(obj_current, field, update_data[field])

        self.db.add(obj_current)
        await self.db.commit()
        await self.db.refresh(obj_current)

        return obj_current

    async def delete(self, **kwargs: Any) -> None:
        """
        Delete an object from the database by filter criteria.

        Args:
            **kwargs: Filter criteria to identify the object to delete

        Raises:
            ObjectNotFound: If no object matches the criteria

        Example:
            >>> # Delete user by ID
            >>> await user_repo.delete(id=1)

            >>> # Delete user by email
            >>> await user_repo.delete(email="user@example.com")
        """
        obj = await self.get(**kwargs)

        self.db.delete(obj)  # type: ignore
        await self.db.commit()

    def _get_order_by(
        self, sort_field: Optional[str] = None, sort_order: Optional[str] = None
    ) -> Any:
        """
        Get the order by clause for queries.

        Args:
            sort_field: Field name to sort by (defaults to 'created_at')
            sort_order: Sort direction, 'asc' or 'desc' (defaults to 'desc')

        Returns:
            SQLAlchemy order by clause

        Note:
            If sort_field doesn't exist in the model, defaults to 'created_at'.
            If sort_order is invalid, defaults to 'desc'.
        """
        columns = self._model.__table__.columns

        if sort_field and sort_field not in columns:
            sort_field = None

        if not sort_field:
            sort_field = "created_at"

        if sort_order not in ["asc", "desc"]:
            sort_order = "desc"

        column = columns[sort_field]
        return column.asc() if sort_order == "asc" else column.desc()

    async def all(
        self,
        skip: int = 0,
        limit: int = 100,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> List[ModelType]:
        """
        Get a list of all objects with optional pagination and sorting.

        Args:
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            sort_field: Field name to sort by (defaults to 'created_at')
            sort_order: Sort direction, 'asc' or 'desc' (defaults to 'desc')

        Returns:
            List of database objects

        Example:
            >>> # Get first 10 users
            >>> users = await user_repo.all(limit=10)

            >>> # Get users 20-30, sorted by name ascending
            >>> users = await user_repo.all(skip=20, limit=10, sort_field="name", sort_order="asc")

            >>> # Get all users (up to default limit of 100)
            >>> all_users = await user_repo.all()
        """
        order_by = self._get_order_by(sort_field, sort_order)
        query = select(self._model).offset(skip).limit(limit).order_by(order_by)  # type: ignore

        response = await self.db.execute(query)
        return response.scalars().all()  # type: ignore

    async def paginate(
        self,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> Page[ModelType]:
        """
        Get paginated results using fastapi-pagination.

        Args:
            sort_field: Field name to sort by (defaults to 'created_at')
            sort_order: Sort direction, 'asc' or 'desc' (defaults to 'desc')

        Returns:
            Page object containing paginated results and metadata

        Example:
            >>> # Get paginated users (page size determined by fastapi-pagination settings)
            >>> page = await user_repo.paginate()
            >>> print(f"Total: {page.total}, Page: {page.page}")
            >>> for user in page.items:
            ...     print(user.name)

            >>> # Paginate with custom sorting
            >>> page = await user_repo.paginate(sort_field="email", sort_order="asc")
        """
        order_by = self._get_order_by(sort_field, sort_order)
        query = select(self._model).order_by(order_by)  # type: ignore

        return await paginate(self.db, query)

    async def f(self, **kwargs: Any) -> List[ModelType]:
        """
        Find all objects matching the given filter criteria.

        This method returns all matching objects without pagination limits,
        unlike the 'all' method which has built-in pagination.

        Args:
            **kwargs: Filter criteria as key-value pairs

        Returns:
            List of all matching database objects

        Example:
            >>> # Find all active users
            >>> active_users = await user_repo.f(is_active=True)

            >>> # Find all users with specific role
            >>> admins = await user_repo.f(role="admin")

            >>> # Find users by multiple criteria
            >>> verified_users = await user_repo.f(is_verified=True, is_active=True)
        """
        logger.info(f"Fetching [{self._model.__class__.__name__}] object by [{kwargs}]")

        query = select(self._model).filter_by(**kwargs)  # type: ignore
        response = await self.db.execute(query)
        scalars: List[ModelType] = response.scalars().all()

        return scalars

    async def get_or_create(self, obj_in: CreateSchemaType, **kwargs: Any) -> ModelType:
        """
        Get an existing object or create it if it doesn't exist.

        This method first attempts to find an object matching the given criteria.
        If found, it returns the existing object. If not found, it creates a new
        object using the provided create schema.

        Args:
            obj_in: The create schema for the new object
            **kwargs: Filter criteria to search for existing object

        Returns:
            Either the existing object or the newly created object

        Example:
            >>> # Get or create user by email
            >>> user_data = UserCreate(name="Bob", email="bob@example.com")
            >>> user = await user_repo.get_or_create(user_data, email="bob@example.com")

            >>> # This will return the same user if called again
            >>> same_user = await user_repo.get_or_create(user_data, email="bob@example.com")
            >>> assert user.id == same_user.id
        """
        try:
            get_instance: Optional[ModelType] = await self.get(**kwargs)

            if get_instance:
                return get_instance
        except ObjectNotFound:
            instance: ModelType = await self.create(obj_in)

        return instance
