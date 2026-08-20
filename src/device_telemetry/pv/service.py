from device_telemetry.pv.model import PVConnectionStatus


class PVTelemetryService:
    def __init__(self, pv_telemetry):
        self.pv_telemetry = pv_telemetry

    def validate_active_power(self):
        if self.pv_telemetry.active_power >= 0 and self.pv_telemetry.active_power <= 5:
            return True
        else:
            return False

    def validate_frequency(self):
        if self.pv_telemetry.frequency >= 40 and self.pv_telemetry.frequency <= 70:
            return True
        else:
            return False

    def validate_dc_voltage(self):
        if self.pv_telemetry.dc_voltage >= 0 and self.pv_telemetry.dc_voltage <= 1:
            return True
        else:
            return False

    def validate_dc_current(self):
        if self.pv_telemetry.dc_current >= 0 and self.pv_telemetry.dc_current <= 20:
            return True
        else:
            return False
        
    def validate_status(self):
        if self.pv_telemetry.status == PVConnectionStatus.OFF:
            return True
        if self.pv_telemetry.status == PVConnectionStatus.GENERATING:
            return True
        if self.pv_telemetry.status == PVConnectionStatus.FAULT:
            return True
        return False

    def pv_telemetry_data_validation(self):
        if (
            self.validate_active_power()
            and self.validate_frequency()
            and self.validate_dc_voltage()
            and self.validate_dc_current()
            and self.validate_status()
        ):
            return True
        else:
            return False