from dataclasses import dataclass
from datetime import datetime
import enum

class MeterConnectionStatus(enum.IntEnum):
    CONNECTED = 1
    DISCONNECTED = 2

@dataclass
class MeterTelemetry:
    import_energy: float
    export_energy: float
    frequency: float
    status: MeterConnectionStatus
    timestamp: datetime
    