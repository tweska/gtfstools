from dataclasses import dataclass
from typing import Any, Dict, Optional

from gtfstools.helpers import RecordBase, get_id, get_opt_id


@dataclass
class Stop(RecordBase):
    stop_id: int
    stop_name: str
    stop_lat: float
    stop_lon: float
    parent_station: Optional[int]

    def __init__(self, values: Dict[str, str], context: Dict[str, Any]):
        stop_id_map = context.setdefault('stop_id_map', {})
        self.parent_station = get_opt_id(stop_id_map, values['parent_station'])
        self.stop_id = get_id(stop_id_map, values['stop_id'])
        self.stop_name = values['stop_name']
        self.stop_lat = float(values['stop_lat'])
        self.stop_lon = float(values['stop_lon'])

    def __lt__(self, other: 'Stop') -> bool:
        return self.stop_id < other.stop_id
