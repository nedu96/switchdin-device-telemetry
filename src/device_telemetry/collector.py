from datetime import datetime, timezone
from device_telemetry.common.types import DeviceType, TelemetryDataStatus
from device_telemetry.meter.service import MeterTelemetryService
from device_telemetry.meter.model import MeterConnectionStatus, MeterTelemetry
from device_telemetry.pv.model import PVConnectionStatus, PVTelemetry
from device_telemetry.pv.service import PVTelemetryService
from device_telemetry.battery.model import BatteryConnectionStatus, BatteryTelemetry
from device_telemetry.battery.service import BatteryTelemetryService

class TelemetryCollector:

    stale_time: int = 60  # Default stale time in seconds

    def validate_telemetry(self, raw_payload: dict) -> TelemetryDataStatus:
        # Reject payloads that are not dictionaries.
        if not isinstance(raw_payload, dict):
            return TelemetryDataStatus.INVALID

        # Validate meter telemetry.
        if raw_payload.get("device_type") == DeviceType.METER.value:
            telemetry = raw_payload.get("telemetry", {})
            required_fields = ["import_energy", "export_energy", "frequency", "status", "timestamp"]

            try:
                if isinstance(telemetry, dict):
                    if all(field in telemetry for field in required_fields):
                        if any(telemetry[field] is None for field in required_fields):
                            return TelemetryDataStatus.MISSING
                        telemetry = {
                            "import_energy": float(telemetry["import_energy"]),
                            "export_energy": float(telemetry["export_energy"]),
                            "frequency": float(telemetry["frequency"]),
                            "status": MeterConnectionStatus(telemetry["status"]),
                            "timestamp": datetime.fromisoformat(telemetry["timestamp"]),
                        }
                    else:
                        return TelemetryDataStatus.MISSING
                else:
                    return TelemetryDataStatus.INVALID
            except (ValueError, TypeError):
                return TelemetryDataStatus.INVALID

            meter_telemetry = MeterTelemetryService(MeterTelemetry(**telemetry))
            if meter_telemetry.telemetry_data_validation():
                if self.is_telemetry_stale(telemetry["timestamp"]):
                    return TelemetryDataStatus.STALE
                return TelemetryDataStatus.VALID
            else:
                return TelemetryDataStatus.INVALID

        # Validate PV telemetry.
        elif raw_payload.get("device_type") == DeviceType.PV.value:
            telemetry = raw_payload.get("telemetry", {})
            required_fields = ["active_power", "frequency", "dc_voltage", "dc_current", "status", "timestamp"]
            try:
                if isinstance(telemetry, dict):
                    if all(field in telemetry for field in required_fields):
                        if any(telemetry[field] is None for field in required_fields):
                            return TelemetryDataStatus.MISSING
                        telemetry = {
                            "active_power": float(telemetry["active_power"]),
                            "frequency": float(telemetry["frequency"]),
                            "dc_voltage": float(telemetry["dc_voltage"]),
                            "dc_current": float(telemetry["dc_current"]),
                            "status": PVConnectionStatus(telemetry["status"]),
                            "timestamp": datetime.fromisoformat(telemetry["timestamp"]),
                        }
                    else:
                        return TelemetryDataStatus.MISSING
                else:
                    return TelemetryDataStatus.INVALID
            except (ValueError, TypeError):
                return TelemetryDataStatus.INVALID
            pv_telemetry_service = PVTelemetryService(PVTelemetry(**telemetry))
            if pv_telemetry_service.pv_telemetry_data_validation():
                if self.is_telemetry_stale(telemetry["timestamp"]):
                    return TelemetryDataStatus.STALE
                return TelemetryDataStatus.VALID
            else:
                return TelemetryDataStatus.INVALID

        # Validate battery telemetry.
        elif raw_payload.get("device_type") == DeviceType.BATTERY.value:
            telemetry = raw_payload.get("telemetry", {})
            required_fields = ["state_of_charge", "battery_voltage", "battery_current", "status", "timestamp"]
            try:
                if isinstance(telemetry, dict):
                    if all(field in telemetry for field in required_fields):
                        if any(telemetry[field] is None for field in required_fields):
                            return TelemetryDataStatus.MISSING
                        telemetry = {
                            "battery_voltage": float(telemetry["battery_voltage"]),
                            "battery_current": float(telemetry["battery_current"]),
                            "state_of_charge": float(telemetry["state_of_charge"]),
                            "status": BatteryConnectionStatus(telemetry["status"]),
                            "timestamp": datetime.fromisoformat(telemetry["timestamp"]),
                        }
                    else:
                        return TelemetryDataStatus.MISSING
                else:
                    return TelemetryDataStatus.INVALID
            except (ValueError, TypeError):
                return TelemetryDataStatus.INVALID

            battery_telemetry_service = BatteryTelemetryService(BatteryTelemetry(**telemetry))
            if battery_telemetry_service.battery_telemetry_data_validation():
                if self.is_telemetry_stale(telemetry["timestamp"]):
                    return TelemetryDataStatus.STALE
                return TelemetryDataStatus.VALID
            else:
                return TelemetryDataStatus.INVALID

        # Unknown device types are invalid.
        return TelemetryDataStatus.INVALID

    
    def is_telemetry_stale(self, timestamp: datetime) -> bool:
        # Compare the telemetry timestamp with the current UTC time.
        current_time = datetime.now(timezone.utc)
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        time_difference = current_time - timestamp
        return time_difference.total_seconds() > self.stale_time  # 1 minute in seconds

    def expose_valid_stale_telemetry(self, raw_payload: dict) -> dict | None:
        # Return telemetry only when it is valid or stale.
        telemetry_status = self.validate_telemetry(raw_payload)
        if telemetry_status == TelemetryDataStatus.VALID or telemetry_status == TelemetryDataStatus.STALE:
            return {
                "device_type": raw_payload.get("device_type"),
                "telemetry_status": telemetry_status.value,
                "telemetry": raw_payload.get("telemetry")
            }
        return None
        