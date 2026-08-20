from datetime import datetime

from device_telemetry.meter.model import (
    MeterConnectionStatus,
    MeterTelemetry,
)
from device_telemetry.meter.service import MeterTelemetryService


def create_telemetry(
    import_energy=100,
    export_energy=50,
    frequency=50,
    status=MeterConnectionStatus.CONNECTED,
    timestamp=None,
):
    return MeterTelemetry(
        import_energy=import_energy,
        export_energy=export_energy,
        frequency=frequency,
        status=status,
        timestamp=timestamp or datetime.now(),
    )


def test_valid_import_energy():
    assert MeterTelemetryService(
        create_telemetry(import_energy=10)
    ).validate_import_energy()


def test_negative_import_energy():
    assert not MeterTelemetryService(
        create_telemetry(import_energy=-1)
    ).validate_import_energy()


def test_valid_export_energy():
    assert MeterTelemetryService(
        create_telemetry(export_energy=10)
    ).validate_export_energy()


def test_negative_export_energy():
    assert not MeterTelemetryService(
        create_telemetry(export_energy=-1)
    ).validate_export_energy()


def test_valid_frequency_boundaries():
    assert MeterTelemetryService(
        create_telemetry(frequency=40)
    ).validate_frequency()

    assert MeterTelemetryService(
        create_telemetry(frequency=70)
    ).validate_frequency()


def test_invalid_frequency():
    assert not MeterTelemetryService(
        create_telemetry(frequency=39.9)
    ).validate_frequency()

    assert not MeterTelemetryService(
        create_telemetry(frequency=70.1)
    ).validate_frequency()


def test_connection_status():
    assert MeterTelemetryService(
        create_telemetry(status=MeterConnectionStatus.CONNECTED)
    ).validate_connection_status()

    assert MeterTelemetryService(
        create_telemetry(status=MeterConnectionStatus.DISCONNECTED)
    ).validate_connection_status()


def test_valid_telemetry():
    assert MeterTelemetryService(
        create_telemetry()
    ).telemetry_data_validation()