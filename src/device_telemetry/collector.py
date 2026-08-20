from datetime import datetime, timezone
from device_telemetry.common.types import DeviceType, TelemetryDataStatus
from device_telemetry.meter.service import MeterTelemetryService
from device_telemetry.meter.model import MeterConnectionStatus, MeterTelemetry

class TelemetryCollector:
        #def __init__(self, telemetry):
        #self.telemetry = telemetry

    def validate_telemetry(self, raw_payload: dict) -> TelemetryDataStatus:
        if raw_payload.get("device_type") == DeviceType.METER.value:
            telemetry = raw_payload.get("telemetry", {})
            required_fields = ["import_energy", "export_energy", "frequency", "status", "timestamp"]
            null_check = any(telemetry.get(field) is None for field in required_fields)
            if null_check:
                return TelemetryDataStatus.MISSING

            try:
                telemetry = {
                    "import_energy": float(telemetry["import_energy"]),
                    "export_energy": float(telemetry["export_energy"]),
                    "frequency": float(telemetry["frequency"]),
                    "status": MeterConnectionStatus(telemetry["status"]),
                    "timestamp": datetime.fromisoformat(telemetry["timestamp"]),
                }
            except (ValueError, TypeError):
                return TelemetryDataStatus.INVALID
            
            meter_telemetry = MeterTelemetryService(MeterTelemetry(**telemetry))
            if meter_telemetry.telemetry_data_validation():
                if self.is_telemetry_stale(telemetry["timestamp"]):
                    return TelemetryDataStatus.STALE
                return TelemetryDataStatus.VALID
            else:                       
                return TelemetryDataStatus.INVALID

        return TelemetryDataStatus.INVALID

    def is_telemetry_stale(self, timestamp: datetime) -> bool:
        current_time = datetime.now(timezone.utc)
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        time_difference = current_time - timestamp
        return time_difference.total_seconds() > 60  # 1 minute in seconds