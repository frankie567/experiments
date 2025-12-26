from typing import Any, List, Literal, NotRequired, Optional, Protocol, TypedDict

"""A user in the system"""
class User(TypedDict):
    id: int
    username: str
    email: str
    full_name: NotRequired[str]
    is_active: NotRequired[bool]
    role: NotRequired[UserRole]

"""Schema for creating a new user"""
class UserCreate(TypedDict):
    username: str
    email: str
    full_name: NotRequired[str]
    role: NotRequired[UserRole]

"""Schema for updating a user"""
class UserUpdate(TypedDict):
    username: NotRequired[str]
    email: NotRequired[str]
    full_name: NotRequired[str]
    is_active: NotRequired[bool]
    role: NotRequired[UserRole]

UserRole = Literal["admin", "user", "guest"]

"""List all users"""
class ListusersProtocol(Protocol):
    """GET /users"""

    def __call__(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[User]: ...

"""Create a new user"""
class CreateuserProtocol(Protocol):
    """POST /users"""

    def __call__(
        self,
        body: UserCreate,
    ) -> User: ...

"""Get a user by ID"""
class GetuserProtocol(Protocol):
    """GET /users/{userId}"""

    def __call__(
        self,
        userId: int,
    ) -> User: ...

"""Update a user"""
class UpdateuserProtocol(Protocol):
    """PUT /users/{userId}"""

    def __call__(
        self,
        userId: int,
        body: UserUpdate,
    ) -> User: ...

"""Delete a user"""
class DeleteuserProtocol(Protocol):
    """DELETE /users/{userId}"""

    def __call__(
        self,
        userId: int,
    ) -> Any: ...

