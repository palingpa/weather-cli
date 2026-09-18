#!/usr/bin/env python3
"""Fetch a simple weather summary (Open-Meteo) or use --mock."""
import argparse
import json
import urllib.parse
import urllib.request


MOCK = {
    "latitude": 35.68,
    "longitude": 139.69,
    "current": {
        "temperature_2m": 22.5,
        "wind_speed_10m": 8.2,
        "weather_code": 1,
    },
}


def fetch(lat: float, lon: float) -> dict:
    qs = urllib.parse.urlencode(
        {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,wind_speed_10m,weather_code",
        }
    )
    url = f"https://api.open-meteo.com/v1/forecast?{qs}"
    with urllib.request.urlopen(url, timeout=15) as resp:
        return json.load(resp)


def format_report(data: dict) -> str:
    cur = data.get("current") or {}
    lines = [
        f"lat={data.get('latitude')} lon={data.get('longitude')}",
        f"temp_c={cur.get('temperature_2m')}",
        f"wind_kmh={cur.get('wind_speed_10m')}",
        f"code={cur.get('weather_code')}",
    ]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--lat", type=float, default=35.68)
    p.add_argument("--lon", type=float, default=139.69)
    p.add_argument("--mock", action="store_true", help="Use canned data")
    p.add_argument("--city", choices=["tokyo", "nyc", "london"], help="Preset coords")
    args = p.parse_args()
    presets = {
        "tokyo": (35.68, 139.69),
        "nyc": (40.71, -74.01),
        "london": (51.51, -0.13),
    }
    if args.city:
        args.lat, args.lon = presets[args.city]
    data = MOCK if args.mock else fetch(args.lat, args.lon)
    print(format_report(data))


if __name__ == "__main__":
    main()
