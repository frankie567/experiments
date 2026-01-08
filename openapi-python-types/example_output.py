from typing import Any, Literal, NotRequired, TypedDict, overload
from dataclasses import dataclass, field

class UserDict(TypedDict):
    """A user in the system"""
    id: int
    username: str
    email: str
    full_name: NotRequired[str]
    is_active: NotRequired[bool]
    role: NotRequired[UserRole]

@dataclass
class User:
    """A user in the system"""
    id: int
    username: str
    email: str
    full_name: str | None = field(default=None)
    is_active: bool | None = field(default=None)
    role: UserRole | None = field(default=None)

class UserCreateDict(TypedDict):
    """Schema for creating a new user"""
    username: str
    email: str
    full_name: NotRequired[str]
    role: NotRequired[UserRole]

@dataclass
class UserCreate:
    """Schema for creating a new user"""
    username: str
    email: str
    full_name: str | None = field(default=None)
    role: UserRole | None = field(default=None)

class UserUpdateDict(TypedDict):
    """Schema for updating a user"""
    username: NotRequired[str]
    email: NotRequired[str]
    full_name: NotRequired[str]
    is_active: NotRequired[bool]
    role: NotRequired[UserRole]

@dataclass
class UserUpdate:
    """Schema for updating a user"""
    username: str | None = field(default=None)
    email: str | None = field(default=None)
    full_name: str | None = field(default=None)
    is_active: bool | None = field(default=None)
    role: UserRole | None = field(default=None)
UserRole = Literal['admin', 'user', 'guest']

class ListusersQueryParamsDict(TypedDict):
    limit: NotRequired[int]
    offset: NotRequired[int]

@dataclass
class ListusersQueryParams:
    limit: int | None = field(default=None)
    offset: int | None = field(default=None)

class GetuserPathParamsDict(TypedDict):
    userId: int

@dataclass
class GetuserPathParams:
    userId: int

class UpdateuserPathParamsDict(TypedDict):
    userId: int

@dataclass
class UpdateuserPathParams:
    userId: int

class DeleteuserPathParamsDict(TypedDict):
    userId: int

@dataclass
class DeleteuserPathParams:
    userId: int

class BaseClient:

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/users'], *, query_params: ListusersQueryParamsDict | ListusersQueryParams=..., response_model: type[list[User]]) -> list[User]:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/users'], *, body: UserCreateDict | UserCreate, response_model: type[User]) -> User:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/users/{userId}'], *, path_params: GetuserPathParamsDict | GetuserPathParams, response_model: type[User]) -> User:
        ...

    @overload
    def __call__(self, method: Literal['PUT'], path: Literal['/users/{userId}'], *, path_params: UpdateuserPathParamsDict | UpdateuserPathParams, body: UserUpdateDict | UserUpdate, response_model: type[User]) -> User:
        ...

    @overload
    def __call__(self, method: Literal['DELETE'], path: Literal['/users/{userId}'], *, path_params: DeleteuserPathParamsDict | DeleteuserPathParams) -> None:
        ...

    def __call__(self, method: str, path: str, *, path_params: Any | None=None, query_params: Any | None=None, body: Any | None=None, response_model: type[Any] | None=None) -> Any:
        return self.make_request(method, path, path_params=path_params, query_params=query_params, body=body, response_model=response_model)

    def make_request(self, method: str, path: str, *, path_params: Any | None=None, query_params: Any | None=None, body: Any | None=None, response_model: type[Any] | None=None) -> Any:
        raise NotImplementedError()

class AsyncBaseClient:

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/users'], *, query_params: ListusersQueryParamsDict | ListusersQueryParams=..., response_model: type[list[User]]) -> list[User]:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/users'], *, body: UserCreateDict | UserCreate, response_model: type[User]) -> User:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/users/{userId}'], *, path_params: GetuserPathParamsDict | GetuserPathParams, response_model: type[User]) -> User:
        ...

    @overload
    async def __call__(self, method: Literal['PUT'], path: Literal['/users/{userId}'], *, path_params: UpdateuserPathParamsDict | UpdateuserPathParams, body: UserUpdateDict | UserUpdate, response_model: type[User]) -> User:
        ...

    @overload
    async def __call__(self, method: Literal['DELETE'], path: Literal['/users/{userId}'], *, path_params: DeleteuserPathParamsDict | DeleteuserPathParams) -> None:
        ...

    async def __call__(self, method: str, path: str, *, path_params: Any | None=None, query_params: Any | None=None, body: Any | None=None, response_model: type[Any] | None=None) -> Any:
        return await self.make_request(method, path, path_params=path_params, query_params=query_params, body=body, response_model=response_model)

    async def make_request(self, method: str, path: str, *, path_params: Any | None=None, query_params: Any | None=None, body: Any | None=None, response_model: type[Any] | None=None) -> Any:
        raise NotImplementedError()
