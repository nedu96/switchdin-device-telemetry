from datetime import datetime, timezone
from device_telemetry.common.types import DeviceType, TelemetryDataStatus
from device_telemetry.meter.service import MeterTelemetryService
from device_telemetry.meter.model import MeterConnectionStatus, MeterTelemetry
from device_telemetry.pv.model import PVConnectionStatus, PVTelemetry
from device_telemetry.pv.service import PVTelemetryService
from device_telemetry.battery.model import BatteryConnectionStatus, BatteryTelemetry
from device_telemetry.battery.service import BatteryTelemetryService

class TelemetryCollector:

    stale_time : int = 60  # Default stale time in seconds

    def validate_telemetry(self, raw_payload: dict) -> TelemetryDataStatus:
        if raw_payload.get("device_type") == DeviceType.METER.value:
            telemetry = raw_payload.get("telemetry", {})
            required_fields = ["import_energy", "export_energy", "frequency", "status", "timestamp"]
            
            try:
                if (isinstance(telemetry, dict)):

                    if ( all(field in telemetry for field in required_fields)):
                        if (telemetry["import_energy"] is None or telemetry["export_energy"] is None or telemetry["frequency"] is None or telemetry["status"] is None or telemetry["timestamp"] is None):
                            return TelemetryDataStatus.MISSING
                        telemetry = {
                            "import_energy": float(telemetry["import_energy"]),
                            "export_energy": float(telemetry["export_energy"]),
                            "frequency": float(telemetry["frequency"]),
                            "status": MeterConnectionStatus(telemetry["status"]),
                        "timestamp": datetime.fromisoformat(telemetry["timestamp"])}
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

        elif raw_payload.get("device_type") == DeviceType.PV.value:
            telemetry = raw_payload.get("telemetry", {})
            required_fields = ["active_power", "frequency", "dc_voltage", "dc_current", "status", "timestamp"]
            try:
                if (isinstance(telemetry, dict)):

                    if ( all(field in telemetry for field in required_fields)):
                        if (telemetry["active_power"] is None or telemetry["frequency"] is None or telemetry["dc_voltage"] is None or telemetry["dc_current"] is None or telemetry["status"] is None or telemetry["timestamp"] is None):
                            return TelemetryDataStatus.MISSING
                        telemetry = {
                            "active_power": float(telemetry["active_power"]),
                            "frequency": float(telemetry["frequency"]),
                            "dc_voltage": float(telemetry["dc_voltage"]),
                            "dc_current": float(telemetry["dc_current"]),
                            "status": PVConnectionStatus(telemetry["status"]),
                            "timestamp": datetime.fromisoformat(telemetry["timestamp"])
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

        elif raw_payload.get("device_type") == DeviceType.BATTERY.value:
            telemetry = raw_payload.get("telemetry", {})
            required_fields = ["state_of_charge", "battery_voltage","battery_current","status", "timestamp"]
            try:
                if (isinstance(telemetry, dict)):

                    if ( all(field in telemetry for field in required_fields)):
                        if (telemetry["battery_voltage"] is None or telemetry["battery_current"] is None or telemetry["state_of_charge"] is None or telemetry["status"] is None or telemetry["timestamp"] is None):
                            return TelemetryDataStatus.MISSING
                        telemetry = {
                            "battery_voltage": float(telemetry["battery_voltage"]),
                            "battery_current": float(telemetry["battery_current"]),
                            "state_of_charge": float(telemetry["state_of_charge"]),
                            "status": BatteryConnectionStatus(telemetry["status"]),
                            "timestamp": datetime.fromisoformat(telemetry["timestamp"])
                        }
                    else:
                        return TelemetryDataStatus.MISSING

                else:
                    return TelemetryDataStatus.INVALID
            except (ValueError, TypeError):
                return TelemetryDataStatus.INVALID
            
            # Assuming a BatteryTelemetryService exists similar to MeterTelemetryService and PVTelemetryService
            battery_telemetry_service = BatteryTelemetryService(BatteryTelemetry(**telemetry))
            if battery_telemetry_service.battery_telemetry_data_validation():
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
        return time_difference.total_seconds() > self.stale_time  # 1 minute in seconds