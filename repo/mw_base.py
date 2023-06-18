from abc import abstractmethod, ABCMeta
from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True)
class MiddlewareResponse:
    name: str
    args: MappingProxyType
    valid: bool
    message: str


class MWBase(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    async def mwmain(cls):
        return MiddlewareResponse(
            name="MWBase",
            args=MappingProxyType({}),
            valid=True,
            message="Not Implemented",
        )
