#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

USER_NAME = "Ronaldo Freitas Dias"


def load_config():
    config_file = Path.home() / ".config" / "health-check"
    config = {}
    if config_file.exists():
        for line in config_file.read_text().splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
    return config


def ping(url: str, body: bytes, timeout: int) -> int:
    req = urllib.request.Request(
        url, data=body, method="POST",
        headers={"User-Agent": "health-check/1.0.2", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.getcode()


def ping_fail(url: str, body: bytes, timeout: int) -> None:
    fail_url = url.rstrip("/") + "/fail"
    try:
        req = urllib.request.Request(
            fail_url, data=body, method="POST",
            headers={"User-Agent": "health-check/1.0.2", "Content-Type": "application/json"}
        )
        urllib.request.urlopen(req, timeout=timeout)
    except Exception:
        pass


def main():
    config = load_config()
    url = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("HEALTHCHECK_URL") or config.get("HEALTHCHECK_URL")
    if not url:
        print("ERROR: HEALTHCHECK_URL not set", file=sys.stderr)
        return 1

    device = os.environ.get("DEVICE_NAME") or config.get("DEVICE_NAME", "unknown")
    timeout = int(os.environ.get("HEALTHCHECK_TIMEOUT", 10))
    try:
        ips = subprocess.check_output(["hostname", "-I"], timeout=5).decode().split()
    except Exception:
        ips = []

    try:
        seconds = int(float(Path("/proc/uptime").read_text().split()[0]))
        d, rem = divmod(seconds, 86400)
        h, rem = divmod(rem, 3600)
        m = rem // 60
        uptime = f"{d}d {h}h {m}m"
    except Exception:
        uptime = "unknown"

    body = json.dumps({"user": USER_NAME, "device": device, "ips": ips, "uptime": uptime}).encode()

    try:
        status = ping(url, body, timeout)
        if 200 <= status < 300:
            print(f"{datetime.now(timezone.utc).isoformat()} status={status} device={device} url={url}")
            return 0

        print(f"ERROR: HTTP {status} url={url}", file=sys.stderr)
        ping_fail(url, body, timeout)
        return 2

    except urllib.error.HTTPError as exc:
        print(f"HTTPError {exc.code} {exc.reason} url={url}", file=sys.stderr)
        ping_fail(url, body, timeout)
        return 3
    except urllib.error.URLError as exc:
        print(f"URLError {exc.reason} url={url}", file=sys.stderr)
        ping_fail(url, body, timeout)
        return 4
    except Exception as exc:
        print(f"ERROR {exc} url={url}", file=sys.stderr)
        ping_fail(url, body, timeout)
        return 5


if __name__ == "__main__":
    sys.exit(main())
