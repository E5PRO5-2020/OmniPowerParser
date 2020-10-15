"""Generic class for measurements and measurement frames.

:platform: Python 3.5.10 on Linux, OS X
:synopsis: This module implements classes for generic measurements taken from a meter.
:authors: Janus Bo Andersen, Jakob Aaboe Vestergaard
:date: 13 October 2020
"""

import os
from collections import OrderedDict
import json
from datetime import datetime
from typing import Any


class Measurement:
    """Single physical measurement.
    A single measurement of a physical quantity pair, consisting of a value and a unit.
    """
    def __init__(self, value: float, unit: str):

        # A numeric value (float)
        self.value = value

        # A string SI unit
        self.unit = unit

    def __repr__(self):
        return str(self.value) + " " + self.unit

    def __iter__(self):
        return self.value, self.unit


class MeterMeasurement:
    """
    A single measurement collection based on one frame from the meter.
    Will contain multiple measurements of physical quantities taken at the same time.
    """

    def __init__(self, meter_id: str, timestamp: datetime):
        """
        Make a new measurement collection.
        Takes meter ID of the meter taking the measurement.
        Add the time when the measurement was received as a datetime obj.
        """

        self.meter_id = meter_id
        self.timestamp = timestamp
        self.Measurements = OrderedDict()   # type: OrderedDict[Any, Any]

    def add_measurement(self, name: str, measurement: Measurement) -> None:
        """
        Store a new measurement in the collection.
        """

        # Insert new pair into ordered dict. The name is human readable
        self.Measurements.update({name: measurement})

    def __repr__(self):
        """
        Human readable representation of a measurement collection.
        """
        # Build the header
        header = "Meter ID: " + str(self.meter_id) + os.linesep
        header = header + "Timestamp: " + str(self.timestamp) + os.linesep

        # Iterate over the measurements in the collection, making a combined string
        text = [k + ": " + str(v.value) + " " + str(v.unit) for k, v in self.Measurements.items()]
        text = os.linesep.join(text)

        # Return human readable combined string
        return header + text

    def as_dict(self) -> dict:
        """Serializes and dumps the Measurement frame as a dict.
        Make an object similar to
        {
            "Meter ID: ": "3232323",
            "Timestamp:": "2020-10-13T17:36:53",
            "Measurements": {
                "A+": {
                    "unit": "kWh",
                    "value": 7
                },
                "A-": {
                    "unit": "kWh",
                    "value": 8
                },
                "P+": {
                    "unit": "kW",
                    "value": 9
                },
                "P-": {
                    "unit": "kW",
                    "value": 10
                }
            }
        }
        """

        # Build object, and dump timestamp using ISO8601, https://en.wikipedia.org/wiki/ISO_8601
        obj = dict({
            'Meter ID: ': str(self.meter_id),
            'Timestamp:': datetime.strftime(self.timestamp, '%Y-%m-%dT%H:%M:%S'),
            'Measurements': dict()
        })
        # Insert all the measurements
        [obj['Measurements'].update({key: {'value': val.value, 'unit': val.unit}})
         for key, val in self.Measurements.items()]     # type:

        return obj

    def json_dump(self) -> str:
        """Returns a JSON formatted string of all data in frame.
        """
        obj = self.as_dict()
        return json.dumps(obj)
