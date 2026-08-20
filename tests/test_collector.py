from datetime import datetime, timedelta, timezone

import pytest

from device_telemetry.collector import TelemetryCollector
from device_telemetry.common.types import DeviceType, TelemetryDataStatus


def valid_meter_payload():
    return {
        "device_type": DeviceType.METER.value,
        "telemetry": {
            "import_energy": 100,
            "export_energy": 50,
            "frequency": 50,
            "status": 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }


def test_missing_frequency():
    payload = valid_meter_payload()
    del payload["telemetry"]["frequency"]

    result = TelemetryCollector().validate_telemetry(payload)

    assert result == TelemetryDataStatus.MISSING


def test_frequency_none():
    payload = valid_meter_payload()
    payload["telemetry"]["frequency"] = None

    result = TelemetryCollector().validate_telemetry(payload)

    assert result == TelemetryDataStatus.MISSING


@pytest.mark.parametrize(
    "field,value",
    [
        ("frequency", "abc"),
        ("status", 9),
        ("timestamp", "invalid-date"),
    ],
)
def test_invalid_meter_data(field, value):
    payload = valid_meter_payload()
    payload["telemetry"][field] = value

    result = TelemetryCollector().validate_telemetry(payload)

    assert result == TelemetryDataStatus.INVALID


def test_stale_meter():
    payload = valid_meter_payload()
    payload["telemetry"]["timestamp"] = (
        datetime.now(timezone.utc) - timedelta(seconds=61)
    ).isoformat()

    result = TelemetryCollector().validate_telemetry(payload)

    assert result == TelemetryDataStatus.STALE


def test_valid_meter():
    payload = valid_meter_payload()

    result = TelemetryCollector().validate_telemetry(payload)

    assert result == TelemetryDataStatus.VALID