from datetime import datetime
import enum
from dataclasses import dataclass


class PVConnectionStatus(enum.IntEnum):
    OFF = 1
    GENERATING = 2
    FAULT = 3

@dataclass  
class PVTelemetry:
    active_power: float
    frequency: float
    dc_voltage: float
    dc_current: float
    status: PVConnectionStatus
    timestamp: datetime