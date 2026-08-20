
from dataclasses import dataclass
import enum

class TelemetryDataStatus(enum.Enum):
    VALID = "Valid Telemetry Data"
    INVALID = "Invalid Telemetry Data"
    MISSING = "Missing Telemetry Data"
    STALE = "Stale Telemetry Data"

class DeviceType(enum.Enum):
    PV = "pv_inverter"
    METER = "meter"
    BATTERY = "battery"

@dataclass
class DeviceTelemetryType:
    telemetry_status: TelemetryDataStatus
    device_type: DeviceType