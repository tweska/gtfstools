from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict

from gtfstools.helpers import DATE_FORMAT, RecordBase, get_id


@dataclass(eq=False)
class Service(RecordBase):
    service_id: int
    start_date: date
    end_date: date

    monday: bool
    tuesday: bool
    wednesday: bool
    thursday: bool
    friday: bool
    saturday: bool
    sunday: bool

    def __init__(self, values: Dict[str, str], context: Dict[str, Any]):
        service_id_map = context.setdefault('service_id_map', {})
        self.service_id = get_id(service_id_map, values['service_id'])
        self.start_date = datetime.strptime(
            values['start_date'], DATE_FORMAT).date()
        self.end_date = datetime.strptime(
            values['end_date'], DATE_FORMAT).date()

        self.monday = values['monday'] == '1'
        self.tuesday = values['tuesday'] == '1'
        self.wednesday = values['tuesday'] == '1'
        self.thursday = values['thursday'] == '1'
        self.friday = values['friday'] == '1'
        self.saturday = values['saturday'] == '1'
        self.sunday = values['sunday'] == '1'

    def primary(self) -> int:
        return self.service_id

    def asdict(self) -> Dict[str, Any]:
        return {
            'service_id': self.service_id,
            'start_date': self.start_date.strftime(DATE_FORMAT),
            'end_date': self.end_date.strftime(DATE_FORMAT),
            'monday': [0, 1][self.monday],
            'tuesday': [0, 1][self.tuesday],
            'wednesday': [0, 1][self.wednesday],
            'thursday': [0, 1][self.thursday],
            'friday': [0, 1][self.friday],
            'saturday': [0, 1][self.saturday],
            'sunday': [0, 1][self.sunday],
        }
