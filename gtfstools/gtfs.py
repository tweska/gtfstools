from csv import DictReader, DictWriter
from dataclasses import dataclass, fields
from io import TextIOWrapper
from typing import Any, Dict, List
from zipfile import ZipFile

from gtfstools.agency import Agency
from gtfstools.calendar import Service
from gtfstools.calendar_dates import ServiceChange
from gtfstools.helpers import RecordBase
from gtfstools.routes import Route
from gtfstools.stops import Stop


GTFS_DATASET_MAPPINGS: List[Dict[str, Any]] = [
    {'filename': 'agency.txt', 'fieldname': 'agencies', 'class': Agency},
    {'filename': 'stops.txt', 'fieldname': 'stops', 'class': Stop},
    {'filename': 'routes.txt', 'fieldname': 'routes', 'class': Route},
    {'filename': 'calendar.txt', 'fieldname': 'services', 'class': Service},
    {'filename': 'calendar_dates.txt', 'fieldname': 'service_changes',
     'class': ServiceChange},
]


@dataclass
class GTFS:
    agencies: List[Agency]
    stops: List[Stop]
    routes: List[Route]
    services: List[Service]
    service_changes: List[ServiceChange]


def read(path: str) -> GTFS:
    context: Dict[str, Any] = {}
    gtfs_fields: Dict[str, List[RecordBase]] = {}
    with ZipFile(path, 'r') as gtfs_file:
        for mapping in GTFS_DATASET_MAPPINGS:
            data = []
            with gtfs_file.open(mapping['filename'], 'r') as data_file:
                data_file_wrapper = TextIOWrapper(data_file, encoding='utf-8')
                reader = DictReader(data_file_wrapper)
                for row in reader:
                    data.append(mapping['class'](row, context))
            gtfs_fields[mapping['fieldname']] = data
    return GTFS(**gtfs_fields)  # type: ignore


def write(path: str, gtfs: GTFS) -> None:
    with ZipFile(path, 'w') as gtfs_file:
        for mapping in GTFS_DATASET_MAPPINGS:
            with gtfs_file.open(mapping['filename'], 'w') as data_file:
                data_file_wrapper = TextIOWrapper(data_file, encoding='utf-8',
                                                  write_through=True)
                fieldnames = [field.name for field in fields(mapping['class'])]
                writer = DictWriter(data_file_wrapper, fieldnames=fieldnames)
                writer.writeheader()

                records = getattr(gtfs, mapping['fieldname'])
                records.sort()
                for record in records:
                    writer.writerow(record.asdict())
