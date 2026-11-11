"""Download the last 12 months of Divvy trip data (public, Motivate International Inc. license).

Usage:  python scripts/download_data.py            (default: 2025-11 → 2026-10, ~238 MB zip)
        python scripts/download_data.py 2025-11 2026-10
Files go to data/raw/ as YYYYMM-divvy-tripdata.csv. Original zips are kept untouched in data/raw/zip/.
Source index: https://divvy-tripdata.s3.amazonaws.com/index.html
License:      https://divvybikes.com/data-license-agreement
"""
import sys
import urllib.request
import zipfile
from pathlib import Path

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
BASE = "https://divvy-tripdata.s3.amazonaws.com/{ym}-divvy-tripdata.zip"


def months(start: str, end: str):
    y, m = map(int, start.split("-"))
    ey, em = map(int, end.split("-"))
    while (y, m) <= (ey, em):
        yield f"{y}{m:02d}"
        m += 1
        if m == 13:
            y, m = y + 1, 1


def main(start: str, end: str):
    (RAW / "zip").mkdir(parents=True, exist_ok=True)
    for ym in months(start, end):
        zpath = RAW / "zip" / f"{ym}-divvy-tripdata.zip"
        if not zpath.exists():
            print(f"downloading {ym} …")
            urllib.request.urlretrieve(BASE.format(ym=ym), zpath)
        with zipfile.ZipFile(zpath) as z:
            for name in z.namelist():
                if name.endswith(".csv") and not name.startswith("__MACOSX"):
                    target = RAW / Path(name).name
                    if not target.exists():
                        target.write_bytes(z.read(name))
                        print(f"  extracted {target.name}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main("2025-11", "2026-10")
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        sys.exit(__doc__)
