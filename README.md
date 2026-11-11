# Cyclistic bike-share case study

Google Data Analytics Capstone, Track A. Analysis in **DuckDB (SQL) + Python (pandas)**, dashboard in **Tableau Public**.

**Business task:** How do annual members and casual riders use Cyclistic bikes differently, and how can marketing convert casual riders into annual members?

## Elevator pitch
> (2–3 sentences, written in the Act phase)

## Process
| Phase | Where |
| --- | --- |
| Ask | [notebook §1](notebooks/cyclistic_analysis.ipynb) |
| Prepare | [docs/data_sources.md](docs/data_sources.md), `scripts/download_data.py` |
| Process | notebook §3, [docs/changelog.md](docs/changelog.md) |
| Analyze | notebook §4 |
| Share | notebook §5, `figures/`, Tableau dashboard (link) |
| Act | notebook §6 — top 3 recommendations |

## Key findings
1. …
2. …
3. …

## Run it
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/download_data.py          # 2025-11 → 2026-10, ~238 MB zip, not committed
jupyter lab notebooks/cyclistic_analysis.ipynb
```
