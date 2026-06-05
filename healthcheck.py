#!/usr/bin/env python3
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("HEALTHCHECK_URL")
    if not url:
        print("ERROR: HEALTHCHECK_URL not set", file=sys.stderr)
        return 1

    timeout = int(os.environ.get("HEALTHCHECK_TIMEOUT", 10))
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "chamado-health/1.0"})

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            status = response.getcode()
            if 200 <= status < 300:
                print(f"{datetime.now(timezone.utc).isoformat()} status={status} url={url}")
                return 0
            body = response.read(200).decode("utf-8", errors="replace")

        print(f"ERROR: HTTP {status}\n{body}", file=sys.stderr)
        return 2

    except urllib.error.HTTPError as exc:
        print(f"HTTPError {exc.code} {exc.reason} url={url}", file=sys.stderr)
        return 3
    except urllib.error.URLError as exc:
        print(f"URLError {exc.reason} url={url}", file=sys.stderr)
        return 4
    except Exception as exc:
        print(f"ERROR {exc} url={url}", file=sys.stderr)
        return 5


if __name__ == "__main__":
    sys.exit(main())
