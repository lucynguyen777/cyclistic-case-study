# Data sources (Prepare)

| Item | Detail |
| --- | --- |
| Dataset | Divvy trip data, used as "Cyclistic" in the case study |
| Publisher | Motivate International Inc. (Lyft) – https://divvy-tripdata.s3.amazonaws.com/index.html |
| License | Divvy Data License Agreement – https://divvybikes.com/data-license-agreement |
| Period used | 2025-11 → 2026-10 (12 monthly files; the newest was published 2026-11-05) |
| Format | 1 CSV per month, one row per trip, 13 columns, 6,294,451 rows in total (~1.4 GB) |
| Columns | ride_id, rideable_type, started_at, ended_at, start/end station name & id, start/end lat & lng, member_casual |
| Values seen | rideable_type: classic_bike, electric_bike · member_casual: member, casual |

## ROCCC
- **Reliable**: recorded automatically by the bike-share system, not self-reported; consistent schema across all 12 files.
- **Original**: first-party data from the operator (Divvy/Lyft), used here in place of the fictional Cyclistic.
- **Comprehensive**: covers time, bike type, stations, coordinates and rider type for every trip; does **not** include rider IDs, prices, revenue or demographics.
- **Current**: the latest 12 complete months at the time of analysis (Nov 2025 – Oct 2026).
- **Cited**: public source with a published license (link above).

## Data quality checks
| Check | Result |
| --- | --- |
| Duplicate ride_id | 35 rows (6,294,451 rows vs 6,294,416 distinct ids) |
| Missing start station name | 19.8% of rides (mostly e-bikes parked off-dock) |
| Missing end coordinates | 5,303 rides (0.08%) |
| Trips starting before the window | 108 rides started on 2025-10-31 but appear in the November file |
| Mislabelled archive | the January 2026 archive contains a file named 202501; renamed to 202601 on extraction |

## Limitations
- No rider IDs: we count **rides, not people**, and cannot see who converted from casual to member.
- No prices or revenue: cannot compare profitability; savings messages need current pricing.
- Station-level results use only rides with a known station name.
- Single city and a single year; weather and events (festivals, tourism) are not in the data.
