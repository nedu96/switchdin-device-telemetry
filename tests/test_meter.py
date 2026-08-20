from types import SimpleNamespace

from device_telemetry.meter.model import MeterConnectionStatus
from device_telemetry.meter.service import MeterTelemetryService


def test_valid_telemetry():
    telemetry = SimpleNamespace(
        import_energy=100,
        export_energy=50,
        frequency=50,
        status=MeterConnectionStatus.CONNECTED,
        timestamp="2026-08-21T10:00:00"
    )

    service = MeterTelemetryService(telemetry)

    assert service.validate_import_energy() is True
    assert service.validate_export_energy() is True
    assert service.validate_frequency() is True
    assert service.validate_connection_status() is True
    assert service.validate_timestamp() is True
    assert service.telemetry_data_validation() is True


def test_invalid_telemetry():
    telemetry = SimpleNamespace(
        import_energy=-1,
        export_energy=-1,
        frequency=30,
        status=None,
        timestamp=None
    )

    service = MeterTelemetryService(telemetry)

    assert service.validate_import_energy() is False
    assert service.validate_export_energy() is False
    assert service.validate_frequency() is False
    assert service.validate_connection_status() is False
    assert service.validate_timestamp() is False
    assert service.telemetry_data_validation() is False


def test_frequency_boundaries():
    telemetry = SimpleNamespace(frequency=40)
    service = MeterTelemetryService(telemetry)

    assert service.validate_frequency() is True

    telemetry.frequency = 70
    assert service.validate_frequency() is True

    telemetry.frequency = 39
    assert service.validate_frequency() is False

    telemetry.frequency = 71
    assert service.validate_frequency() is False