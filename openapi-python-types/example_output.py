from typing import Any, List, Literal, NotRequired, Protocol, TypedDict, overload

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
UserRole = Literal['admin', 'user', 'guest']

class ListusersQueryParams(TypedDict):
    limit: NotRequired[int]
    offset: NotRequired[int]

class GetuserPathParams(TypedDict):
    userId: int

class UpdateuserPathParams(TypedDict):
    userId: int

class DeleteuserPathParams(TypedDict):
    userId: int

class Client(Protocol):

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/users'], *, path_params: None, query_params: ListusersQueryParams, body: None) -> List[User]:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/users'], *, path_params: None, query_params: None, body: UserCreate) -> User:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/users/{userId}'], *, path_params: GetuserPathParams, query_params: None, body: None) -> User:
        ...

    @overload
    def __call__(self, method: Literal['PUT'], path: Literal['/users/{userId}'], *, path_params: UpdateuserPathParams, query_params: None, body: UserUpdate) -> User:
        ...

    @overload
    def __call__(self, method: Literal['DELETE'], path: Literal['/users/{userId}'], *, path_params: DeleteuserPathParams, query_params: None, body: None) -> None:
        ...

    def __call__(self, method: str, path: str, *, path_params: Any, query_params: Any, body: Any) -> Any:
        ...
