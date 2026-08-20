from device_telemetry.battery.model import BatteryConnectionStatus, BatteryTelemetry

class BatteryTelemetryService:
    def __init__(self, battery_telemetry: BatteryTelemetry):
        # Store the battery telemetry to validate.
        self.battery_telemetry = battery_telemetry

    def validate_state_of_charge(self):
        # State of charge must be between 0 and 100 percent.
        if self.battery_telemetry.state_of_charge >= 0 and self.battery_telemetry.state_of_charge <= 100:
            return True
        else:
            return False

    def validate_battery_voltage(self):
        # Battery voltage must be within the supported range.
        if self.battery_telemetry.battery_voltage >= 0 and self.battery_telemetry.battery_voltage <= 1:
            return True
        else:
            return False

    def validate_battery_current(self):
        # Battery current must be within the supported limits.
        if self.battery_telemetry.battery_current >= -10000 and self.battery_telemetry.battery_current <= 10000:
            return True
        else:
            return False

    def validate_battery_status(self):
        # Check that the status is a recognised connection state.
        if self.battery_telemetry.status == BatteryConnectionStatus.OFF:
            return True
        if self.battery_telemetry.status == BatteryConnectionStatus.CHARGING:
            return True
        if self.battery_telemetry.status == BatteryConnectionStatus.DISCHARGING:
            return True
        if self.battery_telemetry.status == BatteryConnectionStatus.FAULT:
            return True
        return False

    def battery_telemetry_data_validation(self):
        # Validate all battery telemetry fields.
        if (
            self.validate_state_of_charge()
            and self.validate_battery_voltage()
            and self.validate_battery_current()
            and self.validate_battery_status()
        ):
            return True
        else:
            return False

        