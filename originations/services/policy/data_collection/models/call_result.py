from dataclasses import dataclass
from enum import Enum
from typing import Generic, Optional, TypeVar


class ServiceCallResult(str, Enum):
    OK = "ok"
    FAIL = "fail"


T = TypeVar("T")  # Define a type variable


@dataclass
class ServiceCall(Generic[T]):
    result: ServiceCallResult
    data: T
    message: Optional[str] = ""
