#!/usr/bin/env python3
"""CLI entry point for health-check."""

import os
import sys
from datetime import datetime, timezone

import urllib.error
from health_check import ping, ping_fail, load_config

AGENT = "Ronaldo Freitas Dias"


def main() -> int:
    config = load_config()
    url = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("HEALTHCHECK_URL") or config.get("HEALTHCHECK_URL")
    if not url:
        print("ERROR: HEALTHCHECK_URL not set", file=sys.stderr)
        return 1

    device = os.environ.get("DEVICE_NAME") or config.get("DEVICE_NAME", "unknown")
    timeout = int(os.environ.get("HEALTHCHECK_TIMEOUT", 10))

    try:
        status = ping(url, agent=AGENT, device=device, timeout=timeout)
        if 200 <= status < 300:
            print(f"{datetime.now(timezone.utc).isoformat()} status={status} device={device} url={url}")
            return 0

        print(f"ERROR: HTTP {status} url={url}", file=sys.stderr)
        ping_fail(url, agent=AGENT, device=device, timeout=timeout)
        return 2

    except urllib.error.HTTPError as exc:
        print(f"HTTPError {exc.code} {exc.reason} url={url}", file=sys.stderr)
        ping_fail(url, agent=AGENT, device=device, timeout=timeout)
        return 3
    except urllib.error.URLError as exc:
        print(f"URLError {exc.reason} url={url}", file=sys.stderr)
        ping_fail(url, agent=AGENT, device=device, timeout=timeout)
        return 4
    except Exception as exc:
        print(f"ERROR {exc} url={url}", file=sys.stderr)
        ping_fail(url, agent=AGENT, device=device, timeout=timeout)
        return 5


if __name__ == "__main__":
    sys.exit(main())
