from datetime import datetime

from device_telemetry.meter.model import (
    MeterConnectionStatus,
    MeterTelemetry,
)
from device_telemetry.meter.service import MeterTelemetryService


def create_meter(
    import_energy=100,
    export_energy=50,
    frequency=50,
    status=MeterConnectionStatus.CONNECTED,
):
    return MeterTelemetry(
        import_energy=import_energy,
        export_energy=export_energy,
        frequency=frequency,
        status=status,
        timestamp=datetime.now(),
    )


def test_valid_import_energy():
    service = MeterTelemetryService(create_meter(import_energy=100))

    assert service.validate_import_energy() is True


def test_negative_import_energy():
    service = MeterTelemetryService(create_meter(import_energy=-1))

    assert service.validate_import_energy() is False


def test_valid_export_energy():
    service = MeterTelemetryService(create_meter(export_energy=100))

    assert service.validate_export_energy() is True


def test_negative_export_energy():
    service = MeterTelemetryService(create_meter(export_energy=-1))

    assert service.validate_export_energy() is False


def test_frequency_40():
    service = MeterTelemetryService(create_meter(frequency=40))

    assert service.validate_frequency() is True


def test_frequency_70():
    service = MeterTelemetryService(create_meter(frequency=70))

    assert service.validate_frequency() is True


def test_frequency_below_range():
    service = MeterTelemetryService(create_meter(frequency=39.9))

    assert service.validate_frequency() is False


def test_frequency_above_range():
    service = MeterTelemetryService(create_meter(frequency=70.1))

    assert service.validate_frequency() is False


def test_connected_status():
    service = MeterTelemetryService(
        create_meter(status=MeterConnectionStatus.CONNECTED)
    )

    assert service.validate_connection_status() is True


def test_disconnected_status():
    service = MeterTelemetryService(
        create_meter(status=MeterConnectionStatus.DISCONNECTED)
    )

    assert service.validate_connection_status() is True