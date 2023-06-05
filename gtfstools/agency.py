from dataclasses import dataclass
from typing import Any, Dict

from gtfstools.helpers import RecordBase, get_id


@dataclass
class Agency(RecordBase):
    agency_id: int
    agency_name: str
    agency_url: str
    agency_timezone: str

    def __init__(self, values: Dict[str, str], context: Dict[str, Any]):
        agency_id_map = context.setdefault('agency_id_map', {})
        # TODO: `agency_id` is only conditionally required
        self.agency_id = get_id(agency_id_map, values['agency_id'])
        self.agency_name = values['agency_name']
        self.agency_url = values['agency_url']
        self.agency_timezone = values['agency_timezone']

    def __lt__(self, other: 'Agency') -> bool:
        return self.agency_id < other.agency_id
