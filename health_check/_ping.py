import json
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

_USER_AGENT = "health-check/1.0.2"


def _build_body(agent: str, device: str) -> bytes:
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

    return json.dumps({"user": agent, "device": device, "ips": ips, "uptime": uptime}).encode()


def ping(url: str, agent: str, device: str, timeout: int = 10) -> int:
    """Send a success ping to Healthchecks.io. Returns the HTTP status code."""
    body = _build_body(agent, device)
    req = urllib.request.Request(
        url, data=body, method="POST",
        headers={"User-Agent": _USER_AGENT, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.getcode()


def ping_fail(url: str, agent: str, device: str, timeout: int = 10) -> None:
    """Send a failure ping to Healthchecks.io (<uuid>/fail)."""
    body = _build_body(agent, device)
    fail_url = url.rstrip("/") + "/fail"
    try:
        req = urllib.request.Request(
            fail_url, data=body, method="POST",
            headers={"User-Agent": _USER_AGENT, "Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=timeout)
    except Exception:
        pass
