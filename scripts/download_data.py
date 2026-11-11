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
        if zpath.exists() and not zipfile.is_zipfile(zpath):
            zpath.unlink()  # incomplete or corrupt download
        if not zpath.exists():
            print(f"downloading {ym} …", flush=True)
            part = zpath.with_suffix(".zip.part")
            urllib.request.urlretrieve(BASE.format(ym=ym), part)
            part.rename(zpath)
        with zipfile.ZipFile(zpath) as z:
            csvs = [n for n in z.namelist() if n.endswith(".csv") and not n.startswith("__MACOSX")]
            for i, name in enumerate(csvs):
                # name the output after the archive month (some archives contain mislabelled inner files)
                target = RAW / (f"{ym}-divvy-tripdata.csv" if len(csvs) == 1 else f"{ym}-divvy-tripdata-{i + 1}.csv")
                if not target.exists():
                    target.write_bytes(z.read(name))
                    print(f"  extracted {name} -> {target.name}", flush=True)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main("2025-11", "2026-10")
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        sys.exit(__doc__)
