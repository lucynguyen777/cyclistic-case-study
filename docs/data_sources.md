# Data sources (Prepare)

| Item | Detail |
| --- | --- |
| Dataset | Divvy trip data (used as "Cyclistic" in the case study) |
| Publisher | Motivate International Inc. — https://divvy-tripdata.s3.amazonaws.com/index.html |
| License | https://divvybikes.com/data-license-agreement |
| Period used | 2025-11 → 2026-10 (12 months, files published up to 2026-11-05) |
| Format | 1 CSV per month, one row per trip |
| Columns | ride_id, rideable_type, started_at, ended_at, start/end station name & id, start/end lat & lng, member_casual |

## ROCCC
- **Reliable**: …
- **Original**: first-party data from the operator
- **Comprehensive**: …
- **Current**: …
- **Cited**: …

## Limitations
- No rider IDs or payment data (privacy) → cannot link trips to people or count unique riders
- Missing station names for some e-bike trips
- …
