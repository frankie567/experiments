from typing import Any, Literal, NotRequired, TypedDict, overload

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

class BaseClient:

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/users'], *, query_params: ListusersQueryParams) -> list[User]:
        ...

    @overload
    def __call__(self, method: Literal['POST'], path: Literal['/users'], *, body: UserCreate) -> User:
        ...

    @overload
    def __call__(self, method: Literal['GET'], path: Literal['/users/{userId}'], *, path_params: GetuserPathParams) -> User:
        ...

    @overload
    def __call__(self, method: Literal['PUT'], path: Literal['/users/{userId}'], *, path_params: UpdateuserPathParams, body: UserUpdate) -> User:
        ...

    @overload
    def __call__(self, method: Literal['DELETE'], path: Literal['/users/{userId}'], *, path_params: DeleteuserPathParams) -> None:
        ...

    def __call__(self, method: str, path: str, *, path_params: Any | None=None, query_params: Any | None=None, body: Any | None=None) -> Any:
        return self.make_request(method, path, path_params=path_params, query_params=query_params, body=body)

    def make_request(self, method: str, path: str, *, path_params: Any | None=None, query_params: Any | None=None, body: Any | None=None) -> Any:
        raise NotImplementedError()

class AsyncBaseClient:

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/users'], *, query_params: ListusersQueryParams) -> list[User]:
        ...

    @overload
    async def __call__(self, method: Literal['POST'], path: Literal['/users'], *, body: UserCreate) -> User:
        ...

    @overload
    async def __call__(self, method: Literal['GET'], path: Literal['/users/{userId}'], *, path_params: GetuserPathParams) -> User:
        ...

    @overload
    async def __call__(self, method: Literal['PUT'], path: Literal['/users/{userId}'], *, path_params: UpdateuserPathParams, body: UserUpdate) -> User:
        ...

    @overload
    async def __call__(self, method: Literal['DELETE'], path: Literal['/users/{userId}'], *, path_params: DeleteuserPathParams) -> None:
        ...

    async def __call__(self, method: str, path: str, *, path_params: Any | None=None, query_params: Any | None=None, body: Any | None=None) -> Any:
        return await self.make_request(method, path, path_params=path_params, query_params=query_params, body=body)

    async def make_request(self, method: str, path: str, *, path_params: Any | None=None, query_params: Any | None=None, body: Any | None=None) -> Any:
        raise NotImplementedError()
