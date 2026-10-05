"""Fetch Sentinel-2/3 TLEs from CelesTrak and write sentinel-overhead/tle.json.

Run once a day by .github/workflows/update-tle.yml. The page reads this file
instead of calling CelesTrak from every visitor's browser.
"""
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=resource&FORMAT=tle"
OUT = Path(__file__).resolve().parents[2] / "sentinel-overhead" / "tle.json"
PREFIXES = ("SENTINEL-2", "SENTINEL-3")


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "world-space-week-tle-updater (GitHub Actions)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")


def parse(text: str) -> list[dict]:
    lines = [l.rstrip() for l in text.splitlines() if l.strip()]
    sats = []
    for i in range(len(lines) - 2):
        name, l1, l2 = lines[i].strip(), lines[i + 1], lines[i + 2]
        if l1.startswith("1 ") and l2.startswith("2 ") and not name.startswith(("1 ", "2 ")):
            sats.append({"name": name, "line1": l1, "line2": l2})
    return sats


def main() -> int:
    sats = [s for s in parse(fetch(URL)) if s["name"].upper().startswith(PREFIXES)]
    if not sats:
        print("No Sentinel TLEs found; keeping the previous file.", file=sys.stderr)
        return 1
    payload = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": URL,
        "satellites": sorted(sats, key=lambda s: s["name"]),
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(sats)} satellites: {', '.join(s['name'] for s in payload['satellites'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
