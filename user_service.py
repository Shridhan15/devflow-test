# -*- coding: utf-8 -*-
"""Service layer for user‑related operations.

This module provides a `UserService` class that encapsulates the business logic
for creating, retrieving, updating, and deleting user entities. It interacts
with a repository layer (`UserRepository`) which abstracts the underlying data
store. The service returns plain data‑transfer objects (`UserDTO`) to keep the
domain model decoupled from external representations.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import List, Optional

# ---------------------------------------------------------------------------
# Import handling
# ---------------------------------------------------------------------------
# Attempt an absolute import first (useful when the package is installed).
# If that fails, fall back to a relative import for development environments.
try:
    from user_repository import UserRepository  # type: ignore
except ImportError:  # pragma: no cover
    try:
        from .user_repository import UserRepository  # type: ignore
    except ImportError:  # pragma: no cover
        UserRepository = None  # type: ignore

try:
    from models import User  # type: ignore
except ImportError:  # pragma: no cover
    try:
        from .models import User  # type: ignore
    except ImportError:  # pragma: no cover
        User = None  # type: ignore

# Configure a module‑level logger.
logger = logging.getLogger(__name__)


@dataclass
class UserDTO:
    """Data transfer object representing a user.

    Attributes
    ----------
    id: int
        Unique identifier of the user.
    username: str
        Human‑readable login name.
    email: str
        Contact e‑mail address.
    is_active: bool, default True
        Flag indicating whether the user account is active.
    """

    id: int
    username: str
    email: str
    is_active: bool = True


class UserService:
    """Service class handling user‑related business logic.

    The service delegates persistence to a `UserRepository` instance and works
    with `UserDTO` objects to keep the API stable.
    """

    def __init__(self, repository: "UserRepository") -> None:
        """Create a new ``UserService``.

        Parameters
        ----------
        repository: UserRepository
            An instance of the repository that provides low‑level data access.
        """
        self._repo = repository
        logger.debug("UserService initialized with repository %s", repository)

    # ---------------------------------------------------------------------
    # CRUD operations
    # ---------------------------------------------------------------------
    def create_user(self, username: str, email: str) -> UserDTO:
        """Create a new user and persist it via the repository.

        Args
        ----
        username: str
            Desired username; must be non‑empty.
        email: str
            User's e‑mail address; basic validation is performed.

        Returns
        -------
        UserDTO
            The newly created user represented as a DTO.
        """
        if not username:
            raise ValueError("username must not be empty")
        if not email or "@" not in email:
            raise ValueError("invalid email address")

        logger.debug("Creating user with username=%s, email=%s", username, email)
        user: "User" = self._repo.add(username=username, email=email)
        dto = self._to_dto(user)
        logger.info("User created with id=%s", dto.id)
        return dto

    def get_user(self, user_id: int) -> Optional[UserDTO]:
        """Retrieve a single user by its identifier.

        Parameters
        ----------
        user_id: int
            Primary key of the user to fetch.

        Returns
        -------
        Optional[UserDTO]
            ``UserDTO`` if found, otherwise ``None``.
        """
        logger.debug("Fetching user with id=%s", user_id)
        user: Optional["User"] = self._repo.get(user_id)
        if user is None:
            logger.warning("User with id=%s not found", user_id)
            return None
        dto = self._to_dto(user)
        logger.info("User fetched: %s", dto)
        return dto

    def list_users(self) -> List[UserDTO]:
        """Return a list of all users.

        Returns
        -------
        List[UserDTO]
            A list containing a DTO for each user in the repository.
        """
        logger.debug("Listing all users")
        users: List["User"] = self._repo.list()
        dtos = [self._to_dto(u) for u in users]
        logger.info("Retrieved %d users", len(dtos))
        return dtos

    def update_user(self, user_id: int, **kwargs) -> Optional[UserDTO]:
        """Update mutable fields of a user.

        Parameters
        ----------
        user_id: int
            Identifier of the user to update.
        **kwargs:
            Fields to update; only ``username``, ``email`` and ``is_active`` are
            allowed.

        Returns
        -------
        Optional[UserDTO]
            Updated DTO if the user existed, otherwise ``None``.
        """
        logger.debug("Updating user id=%s with %s", user_id, kwargs)
        user: Optional["User"] = self._repo.get(user_id)
        if user is None:
            logger.warning("Cannot update non‑existent user id=%s", user_id)
            return None

        allowed_fields = {"username", "email", "is_active"}
        for key, value in kwargs.items():
            if key not in allowed_fields:
                logger.error("Attempted to update disallowed field '%s'", key)
                raise ValueError(f"Field '{key}' cannot be updated")
            setattr(user, key, value)
            logger.debug("Set %s to %s on user id=%s", key, value, user_id)

        updated_user: "User" = self._repo.update(user)
        dto = self._to_dto(updated_user)
        logger.info("User id=%s updated", user_id)
        return dto

    def delete_user(self, user_id: int) -> bool:
        """Delete a user by its identifier.

        Parameters
        ----------
        user_id: int
            Identifier of the user to delete.

        Returns
        -------
        bool
            ``True`` if deletion succeeded, ``False`` otherwise.
        """
        logger.debug("Attempting to delete user id=%s", user_id)
        try:
            self._repo.delete(user_id)
        except Exception as exc:  # pragma: no cover – repository‑specific
            logger.error("Failed to delete user id=%s: %s", user_id, exc)
            return False
        logger.info("User id=%s deleted", user_id)
        return True

    # ---------------------------------------------------------------------
    # Helper methods
    # ---------------------------------------------------------------------
    def _to_dto(self, user: "User") -> UserDTO:
        """Convert a ``User`` model instance to a ``UserDTO``.

        This isolates conversion logic, making it easier to adapt if the model
        changes.
        """
        return UserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=getattr(user, "is_active", True),
        )


# -------------------------------------------------------------------------
# Demo / simple manual test (executed only when run directly)
# -------------------------------------------------------------------------
if __name__ == "__main__":
    # Provide fallback definitions if imports failed.
    from dataclasses import dataclass
    from typing import List, Optional

    if User is None:
        @dataclass
        class User:  # type: ignore
            id: int
            username: str
            email: str
            is_active: bool = True

    if UserRepository is None:
        from abc import ABC, abstractmethod

        class UserRepository(ABC):  # type: ignore
            @abstractmethod
            def add(self, username: str, email: str) -> User:
                pass

            @abstractmethod
            def get(self, user_id: int) -> Optional[User]:
                pass

            @abstractmethod
            def list(self) -> List[User]:
                pass

            @abstractmethod
            def update(self, user: User) -> User:
                pass

            @abstractmethod
            def delete(self, user_id: int) -> None:
                pass

    # Simple in‑memory repository for demonstration purposes.
    class InMemoryUserRepository(UserRepository):
        """A minimal in‑memory repository for demonstration purposes."""

        def __init__(self) -> None:
            self._store: dict[int, User] = {}
            self._next_id = 1

        def add(self, username: str, email: str) -> User:
            user = User(
                id=self._next_id,
                username=username,
                email=email,
                is_active=True,
            )
            self._store[self._next_id] = user
            self._next_id += 1
            return user

        def get(self, user_id: int) -> Optional[User]:
            return self._store.get(user_id)

        def list(self) -> List[User]:
            return list(self._store.values())

        def update(self, user: User) -> User:
            if user.id not in self._store:
                raise KeyError(f"User {user.id} does not exist")
            self._store[user.id] = user
            return user

        def delete(self, user_id: int) -> None:
            self._store.pop(user_id, None)

    # Initialise service with the demo repository.
    repo = InMemoryUserRepository()
    service = UserService(repo)

    # Demonstrate CRUD operations.
    alice = service.create_user("alice", "alice@example.com")
    print("Created:", alice)

    fetched = service.get_user(alice.id)
    print("Fetched:", fetched)

    service.update_user(alice.id, username="alice2")
    print("After update:", service.get_user(alice.id))

    print("All users:", service.list_users())

    service.delete_user(alice.id)
    print("After deletion, all users:", service.list_users())
