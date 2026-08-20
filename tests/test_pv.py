from datetime import datetime

from device_telemetry.pv.model import (
    PVConnectionStatus,
    PVTelemetry,
)
from device_telemetry.pv.service import PVTelemetryService


def create_pv(
    active_power=2.5,
    frequency=50,
    dc_voltage=0.5,
    dc_current=10,
    status=PVConnectionStatus.GENERATING,
):
    return PVTelemetry(
        active_power=active_power,
        frequency=frequency,
        dc_voltage=dc_voltage,
        dc_current=dc_current,
        status=status,
        timestamp=datetime.now(),
    )


def test_active_power():
    assert PVTelemetryService(
        create_pv(active_power=0)
    ).validate_active_power()

    assert PVTelemetryService(
        create_pv(active_power=5)
    ).validate_active_power()

    assert not PVTelemetryService(
        create_pv(active_power=-0.1)
    ).validate_active_power()

    assert not PVTelemetryService(
        create_pv(active_power=5.1)
    ).validate_active_power()


def test_frequency():
    assert PVTelemetryService(
        create_pv(frequency=40)
    ).validate_frequency()

    assert PVTelemetryService(
        create_pv(frequency=70)
    ).validate_frequency()

    assert not PVTelemetryService(
        create_pv(frequency=39.9)
    ).validate_frequency()

    assert not PVTelemetryService(
        create_pv(frequency=70.1)
    ).validate_frequency()


def test_dc_voltage():
    assert PVTelemetryService(
        create_pv(dc_voltage=0)
    ).validate_dc_voltage()

    assert PVTelemetryService(
        create_pv(dc_voltage=1)
    ).validate_dc_voltage()

    assert not PVTelemetryService(
        create_pv(dc_voltage=-0.1)
    ).validate_dc_voltage()

    assert not PVTelemetryService(
        create_pv(dc_voltage=1.1)
    ).validate_dc_voltage()


def test_dc_current():
    assert PVTelemetryService(
        create_pv(dc_current=0)
    ).validate_dc_current()

    assert PVTelemetryService(
        create_pv(dc_current=20)
    ).validate_dc_current()

    assert not PVTelemetryService(
        create_pv(dc_current=-0.1)
    ).validate_dc_current()

    assert not PVTelemetryService(
        create_pv(dc_current=20.1)
    ).validate_dc_current()


def test_status():
    for status in PVConnectionStatus:
        assert PVTelemetryService(
            create_pv(status=status)
        ).validate_status()


def test_valid_pv_telemetry():
    service = PVTelemetryService(create_pv())

    assert service.pv_telemetry_data_validation()