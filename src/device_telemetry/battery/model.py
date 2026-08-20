
from dataclasses import dataclass
from datetime import datetime
import enum


class BatteryConnectionStatus(enum.IntEnum):
    OFF = 1
    CHARGING = 2
    DISCHARGING = 3
    FAULT = 4

@dataclass
class BatteryTelemetry:
    state_of_charge: float
    battery_voltage: float
    battery_current: float
    status: BatteryConnectionStatus
    timestamp: datetime