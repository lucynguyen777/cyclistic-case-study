# Cleaning & transformation change log (Process)

Tool: DuckDB 2.0 (SQL) inside `notebooks/cyclistic_analysis.ipynb`, run on 2026-11-11. Raw files are never modified; the cleaned table is written to `data/clean/trips_clean.parquet`.

| # | Step | Rows after | Removed | Reason |
| ---: | --- | ---: | ---: | --- |
| 1 | Load 12 monthly CSVs into `trips_raw` (`union_by_name`, timestamps parsed) | 6,294,451 | – | one table for the whole year |
| 2 | Keep the first row per `ride_id` | 6,294,416 | 35 | duplicate trip records |
| 3 | Keep `member_casual` in {member, casual} | 6,294,416 | 0 | no invalid values found |
| 4 | Keep rides between 1 minute and 24 hours | 6,130,233 | 164,183 | < 1 min (159,035) = false starts/re-docks; > 24 h (5,148) = lost or faulty bikes |
| 5 | Drop stations named like `%TEST%` / `%REPAIR%` | 6,130,220 | 13 | internal test and repair stations |
| 6 | Keep rides starting 2025-11-01 00:00 to 2026-10-31 23:59 | **6,130,112** | 108 | 108 rides from 2025-10-31 were in the November file |
| 7 | Add `ride_length_min`, `day_of_week`, `dow` (1 = Mon … 7 = Sun), `hour`, `month`, `round_trip` | 6,130,112 | – | fields needed for the analysis |

Total removed: 164,339 rows (2.6% of the raw data).

Kept on purpose: rides without a station name (19.8%). They still have times, bike type and rider type, so they count in every analysis except station rankings.
