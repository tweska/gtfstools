from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional, Tuple, TypeVar, Union

T = TypeVar('T', bound='RecordBase')

DATE_FORMAT = '%Y%m%d'


@dataclass(eq=False)
class RecordBase(ABC):
    @abstractmethod
    def __init__(self, values: Dict[str, str], context: Dict[str, Any]):
        pass

    def __hash__(self) -> int:
        return hash(self.primary())

    def __lt__(self: T, other: T) -> bool:
        if type(self) != type(other):
            raise TypeError(f"Type mismatch: {type(self)} and {type(other)}")
        return self.primary() < other.primary()  # type: ignore

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, type(self)) \
               and self.primary() == other.primary()

    @abstractmethod
    def primary(self) -> Union[int, Tuple[int, int]]:
        pass

    def asdict(self) -> Dict[str, Any]:
        return asdict(self)


def get_id(id_map: Dict[str, int], original: str) -> int:
    return id_map.setdefault(original, len(id_map))


def get_opt_id(id_map: Dict[str, int], original: str) -> Optional[int]:
    return None if original == '' else get_id(id_map, original)
