from device_telemetry.meter.model import MeterConnectionStatus
from device_telemetry.meter.model import MeterTelemetry


class MeterTelemetryService:
    def __init__(self, telemetry: MeterTelemetry):
        # Store the telemetry to validate.
        self._telemetry = telemetry

    def validate_import_energy(self):
        # Import energy cannot be negative.
        if self._telemetry.import_energy >= 0:
            return True
        else:
            return False

    def validate_export_energy(self):
        # Export energy cannot be negative.
        if self._telemetry.export_energy >= 0:
            return True
        else:
            return False

    def validate_frequency(self):
        # Frequency must be between 40 and 70.
        if self._telemetry.frequency >= 40 and self._telemetry.frequency <= 70:
            return True
        else:
            return False

    def validate_connection_status(self):
        # Only connected and disconnected statuses are valid.
        if self._telemetry.status == MeterConnectionStatus.CONNECTED:
            return True
        if self._telemetry.status == MeterConnectionStatus.DISCONNECTED:
            return True
        return False
   
    def telemetry_data_validation(self):
        # Validate all telemetry fields.
        if (
            self.validate_import_energy()
            and self.validate_export_energy()
            and self.validate_frequency()
            and self.validate_connection_status()
        ):
            return True
        else:
            return False
    