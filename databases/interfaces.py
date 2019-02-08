import typing
from types import TracebackType

from sqlalchemy.sql import ClauseElement


class DatabaseBackend:
    async def connect(self) -> None:
        raise NotImplementedError()  # pragma: no cover

    async def disconnect(self) -> None:
        raise NotImplementedError()  # pragma: no cover

    def session(self) -> "DatabaseSession":
        raise NotImplementedError()  # pragma: no cover


class DatabaseSession:
    async def fetch_all(self, query: ClauseElement) -> typing.Any:
        raise NotImplementedError()  # pragma: no cover

    async def fetch_one(self, query: ClauseElement) -> typing.Any:
        raise NotImplementedError()  # pragma: no cover

    async def execute(self, query: ClauseElement, values: dict = None) -> None:
        raise NotImplementedError()  # pragma: no cover

    async def execute_many(self, query: ClauseElement, values: list) -> None:
        raise NotImplementedError()  # pragma: no cover

    def transaction(self, force_rollback: bool = False) -> "DatabaseTransaction":
        raise NotImplementedError()  # pragma: no cover


class DatabaseTransaction:
    def __init__(self, force_rollback: bool = False):
        self.force_rollback = force_rollback

    async def __aenter__(self) -> None:
        await self.start()

    async def __aexit__(
        self,
        exc_type: typing.Type[BaseException] = None,
        exc_value: BaseException = None,
        traceback: TracebackType = None,
    ) -> None:
        if exc_type is not None or self.force_rollback:
            await self.rollback()
        else:
            await self.commit()

    async def start(self) -> None:
        raise NotImplementedError()  # pragma: no cover

    async def commit(self) -> None:
        raise NotImplementedError()  # pragma: no cover

    async def rollback(self) -> None:
        raise NotImplementedError()  # pragma: no cover
