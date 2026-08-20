from device_telemetry.meter.model import MeterConnectionStatus
from device_telemetry.meter.model import MeterTelemetry


class MeterTelemetryService:
    def __init__(self, telemetry: MeterTelemetry):
        self._telemetry = telemetry

    def validate_import_energy(self):
        if self._telemetry.import_energy >= 0:
            return True
        else:
            return False

    def validate_export_energy(self):
        if self._telemetry.export_energy >= 0:
            return True
        else:
            return False

    def validate_frequency(self):
        if self._telemetry.frequency >= 40 and self._telemetry.frequency <= 70:
            return True
        else:
            return False

    def validate_connection_status(self):
        if self._telemetry.status == MeterConnectionStatus.CONNECTED:
            return True
        if self._telemetry.status == MeterConnectionStatus.DISCONNECTED:
            return True
        return False

    def validate_timestamp(self):
        if self._telemetry.timestamp is not None:
            return True
        else:
            return False    

    def telemetry_data_validation(self):
        if (
            self.validate_import_energy()
            and self.validate_export_energy()
            and self.validate_frequency()
            and self.validate_connection_status()
            and self.validate_timestamp()
        ):
            return True
        else:
            return False
    