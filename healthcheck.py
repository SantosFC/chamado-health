#!/usr/bin/env python3
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path


def load_url_from_config():
    config_file = Path.home() / ".config" / "health-monitor"
    if config_file.exists():
        for line in config_file.read_text().splitlines():
            if line.startswith("HEALTHCHECK_URL="):
                return line.split("=", 1)[1].strip()
    return None


def ping(url: str, timeout: int) -> int:
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "health-monitor/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.getcode()


def ping_fail(url: str, timeout: int) -> None:
    fail_url = url.rstrip("/") + "/fail"
    try:
        req = urllib.request.Request(fail_url, method="GET", headers={"User-Agent": "health-monitor/1.0"})
        urllib.request.urlopen(req, timeout=timeout)
    except Exception:
        pass


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("HEALTHCHECK_URL") or load_url_from_config()
    if not url:
        print("ERROR: HEALTHCHECK_URL not set", file=sys.stderr)
        return 1

    timeout = int(os.environ.get("HEALTHCHECK_TIMEOUT", 10))

    try:
        status = ping(url, timeout)
        if 200 <= status < 300:
            print(f"{datetime.now(timezone.utc).isoformat()} status={status} url={url}")
            return 0

        print(f"ERROR: HTTP {status} url={url}", file=sys.stderr)
        ping_fail(url, timeout)
        return 2

    except urllib.error.HTTPError as exc:
        print(f"HTTPError {exc.code} {exc.reason} url={url}", file=sys.stderr)
        ping_fail(url, timeout)
        return 3
    except urllib.error.URLError as exc:
        print(f"URLError {exc.reason} url={url}", file=sys.stderr)
        ping_fail(url, timeout)
        return 4
    except Exception as exc:
        print(f"ERROR {exc} url={url}", file=sys.stderr)
        ping_fail(url, timeout)
        return 5


if __name__ == "__main__":
    sys.exit(main())
