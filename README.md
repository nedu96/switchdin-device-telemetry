## DEVICE TELEMETRY COLLECTION

## OVERVIEW

- This project is a component for handling telemetry from electricity meters, PV inverters, and batteries.
- It accepts incoming telemetry, converts it into device-specific models, and applies validation rules.
- It distinguishes telemetry as VALID, INVALID, MISSING, or STALE.
- Device-specific validation is separated into individual services, while the collector handles routing, parsing, and stale data checks.
- Valid and stale telemetry can be exposed to downstream consumers.

## ASSUMPTIONS

- incoming telemetry is an already-decoded Python dictionary
- each message contains device_type and telemetry
- timestamps are ISO-8601 strings
- timestamps without timezone information are treated as UTC
- telemetry older than 60 seconds is considered stale
- stale threshold time could be configurable in a production system

## ARCHITECTURE

raw payload
↓
TelemetryCollector
↓
parse / missing checks
↓
device model
↓
device-specific service
↓
stale check
↓
VALID / INVALID / MISSING / STALE

## VALIDATION RULES

| Device  | Field           | Valid range/status |
| ------- | --------------- | ------------------ |
| Meter   | Import energy   | `>= 0`             |
| Meter   | Export energy   | `>= 0`             |
| Meter   | Frequency       | `40–70`            |
| PV      | Active power    | `0–5`              |
| PV      | Frequency       | `40–70`            |
| PV      | DC voltage      | `0–1`              |
| PV      | DC current      | `0–20`             |
| Battery | State of charge | `0–100`            |
| Battery | Battery voltage | `0–1`              |
| Battery | Battery current | `-10000–10000`     |

## INPUT FORMAT

### Meter Payload

    ```json
    {
    "device_type": "meter",
    "telemetry": {
        "import_energy": 100.0,
        "export_energy": 50.0,
        "frequency": 50.0,
        "status": 1,
        "timestamp": "2026-08-21T01:20:00+10:00"
    }
    }
    ```

### PV inverter Payload

````json
 {
 "device_type": "pv_inverter",
 "telemetry": {
     "active_power": 3.5,
     "frequency": 50.0,
     "dc_voltage": 0.7,
     "dc_current": 10.0,
     "status": 2,
     "timestamp": "2026-08-21T01:20:00+10:00"
 }
 }
 ```

### Battery Payload

 ```json
 {
 "device_type": "battery",
 "telemetry": {
     "state_of_charge": 75.0,
     "battery_voltage": 0.8,
     "battery_current": -250.0,
     "status": 3,
     "timestamp": "2026-08-21T01:20:00+10:00"
 }
 }
````

## TELEMETRY STATES

VALID

- all required fields are present
- values can be parsed
- all business validation rules pass
- timestamp is fresh

MISSING

- required field is absent
- or required field has a None value

INVALID

- malformed value
- unsupported status
- value outside allowed range
- invalid timestamp format
- malformed telemetry structure

STALE

- telemetry is valid
- timestamp is more than 60 seconds old

## DESIGN

TelemetryCollector (src/device_telemetry/collector.py)

- receives raw payloads
- identifies device type
- checks missing/malformed data
- converts raw values
- delegates validation
- checks staleness

Meter/PV/Battery models (src/device_telemetry/meter/ , src/device_telemetry/pv/ , src/device_telemetry/Meter/battery/)

- represent parsed telemetry

Device services

- contain device specific validation rules

common/types.py

- common enums such as device type and telemetry status

## FILE STRUCTURE

src/
└── device_telemetry/
├── collector.py
├── common/
├── meter/
├── pv/
└── battery/

## EXPOSING TELEMETRY

- VALID telemetry can be exposed
- STALE telemetry can also be exposed but is clearly marked stale
- INVALID/MISSING telemetry is not treated as usable telemetry

### Sample data

```json
{
  "device_type": "meter",
  "telemetry_status": "Valid Telemetry Data",
  "telemetry": {
    "import_energy": 100.0,
    "export_energy": 50.0,
    "frequency": 50.0,
    "status": 1,
    "timestamp": "2026-08-21T01:30:00+10:00"
  }
}
```

## TEST CASES

![Test results](image-1.png)

- boundary conditions
- invalid ranges
- statuses
- missing fields
- malformed values
- stale telemetry

## RUNNING TESTS

Install the package in editable mode:

```bash
python -m pip install -e .
```

## FUTURE IMPROVEMENTS

- stale timeout could be configuration-driven
- common parsing could be extracted if many more device types are added
- transport/protocol integration is intentionally not implemented
- production system could add logging/metrics
