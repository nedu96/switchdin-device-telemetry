from datetime import datetime

from device_telemetry.battery.model import (
    BatteryConnectionStatus,
    BatteryTelemetry,
)
from device_telemetry.battery.service import BatteryTelemetryService


def create_battery(
    state_of_charge=50,
    battery_voltage=0.5,
    battery_current=0,
    status=BatteryConnectionStatus.OFF,
):
    return BatteryTelemetry(
        state_of_charge=state_of_charge,
        battery_voltage=battery_voltage,
        battery_current=battery_current,
        status=status,
        timestamp=datetime.now(),
    )


def test_state_of_charge():
    assert BatteryTelemetryService(
        create_battery(state_of_charge=0)
    ).validate_state_of_charge()

    assert BatteryTelemetryService(
        create_battery(state_of_charge=100)
    ).validate_state_of_charge()

    assert not BatteryTelemetryService(
        create_battery(state_of_charge=-1)
    ).validate_state_of_charge()

    assert not BatteryTelemetryService(
        create_battery(state_of_charge=101)
    ).validate_state_of_charge()


def test_battery_voltage():
    assert BatteryTelemetryService(
        create_battery(battery_voltage=0)
    ).validate_battery_voltage()

    assert BatteryTelemetryService(
        create_battery(battery_voltage=1)
    ).validate_battery_voltage()

    assert not BatteryTelemetryService(
        create_battery(battery_voltage=-0.1)
    ).validate_battery_voltage()

    assert not BatteryTelemetryService(
        create_battery(battery_voltage=1.1)
    ).validate_battery_voltage()


def test_battery_current():
    assert BatteryTelemetryService(
        create_battery(battery_current=-10000)
    ).validate_battery_current()

    assert BatteryTelemetryService(
        create_battery(battery_current=10000)
    ).validate_battery_current()

    assert not BatteryTelemetryService(
        create_battery(battery_current=-10001)
    ).validate_battery_current()

    assert not BatteryTelemetryService(
        create_battery(battery_current=10001)
    ).validate_battery_current()


def test_battery_status():
    for status in BatteryConnectionStatus:
        assert BatteryTelemetryService(
            create_battery(status=status)
        ).validate_battery_status()


def test_valid_battery_telemetry():
    service = BatteryTelemetryService(create_battery())

    assert service.battery_telemetry_data_validation()