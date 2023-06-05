from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TypeVar


T = TypeVar('T')


class RecordBase(ABC):
    @abstractmethod
    def __init__(self, values: Dict[str, str], context: Dict[str, Any]):
        pass

    @abstractmethod
    def __lt__(self: T, other: T) -> bool:
        pass


def get_id(id_map: Dict[str, int], original: str) -> int:
    return id_map.setdefault(original, len(id_map))


def get_opt_id(id_map: Dict[str, int], original: str) -> Optional[int]:
    return None if original == '' else get_id(id_map, original)
