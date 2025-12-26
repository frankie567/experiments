from typing import Any, List, Literal, NotRequired, Optional, Protocol, TypedDict

class User(TypedDict):
    """A user in the system"""
    id: int
    username: str
    email: str
    full_name: NotRequired[str]
    is_active: NotRequired[bool]
    role: NotRequired[UserRole]

class UserCreate(TypedDict):
    """Schema for creating a new user"""
    username: str
    email: str
    full_name: NotRequired[str]
    role: NotRequired[UserRole]

class UserUpdate(TypedDict):
    """Schema for updating a user"""
    username: NotRequired[str]
    email: NotRequired[str]
    full_name: NotRequired[str]
    is_active: NotRequired[bool]
    role: NotRequired[UserRole]

UserRole = Literal["admin", "user", "guest"]

class ListusersProtocol(Protocol):
    """List all users
    
    GET /users
    """

    def __call__(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[User]: ...

class CreateuserProtocol(Protocol):
    """Create a new user
    
    POST /users
    """

    def __call__(
        self,
        body: UserCreate,
    ) -> User: ...

class GetuserProtocol(Protocol):
    """Get a user by ID
    
    GET /users/{userId}
    """

    def __call__(
        self,
        userId: int,
    ) -> User: ...

class UpdateuserProtocol(Protocol):
    """Update a user
    
    PUT /users/{userId}
    """

    def __call__(
        self,
        userId: int,
        body: UserUpdate,
    ) -> User: ...

class DeleteuserProtocol(Protocol):
    """Delete a user
    
    DELETE /users/{userId}
    """

    def __call__(
        self,
        userId: int,
    ) -> Any: ...

