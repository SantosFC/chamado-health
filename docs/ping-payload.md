# Ping Payload Standard

This document defines the standard payload for all health check pings sent to Healthchecks.io across all agents (scripts, bots, services).

## Why not use an existing library?

The [`healthchecks-io`](https://pypi.org/project/healthchecks-io/) package on PyPI focuses on the management API and does not send a custom body payload. This library fills that gap with an opinionated, consistent payload that identifies the agent, device, IPs, and uptime on every ping.

---

## Using as a Python module

Install directly from the repository:

```bash
pip install git+https://github.com/SantosFC/health-check.git
```

### Basic usage

```python
from health_check import ping, ping_fail

url = "https://hc-ping.com/<your-uuid>"

try:
    status = ping(url, agent="my-telegram-bot", device="my-server")
    if 200 <= status < 300:
        print("Ping OK")
    else:
        ping_fail(url, agent="my-telegram-bot", device="my-server")
except Exception as exc:
    ping_fail(url, agent="my-telegram-bot", device="my-server")
    raise
```

### Loading config from file

```python
from health_check import load_config, ping

config = load_config()  # reads ~/.config/health-check
ping(config["HEALTHCHECK_URL"], agent="my-bot", device=config["DEVICE_NAME"])
```

### Custom config path

```python
from pathlib import Path
from health_check import load_config

config = load_config(config_file=Path("/etc/my-bot/config"))
```

### Timeout

```python
ping(url, agent="my-bot", device="server", timeout=5)
```

---

## HTTP Request

- **Method:** `POST`
- **URL:** `https://hc-ping.com/<uuid>`

## Headers

| Header | Value |
|---|---|
| `User-Agent` | `health-check/<version>` |
| `Content-Type` | `application/json` |

## Body

```json
{
  "user": "<agent-name>",
  "device": "<device-name>",
  "ips": ["<ip1>", "<ip2>"],
  "uptime": "<Xd Yh Zm>"
}
```

| Field | Type | Description |
|---|---|---|
| `user` | `string` | Name of the agent sending the ping (script, bot, service) |
| `device` | `string` | Name of the device or host where the agent runs |
| `ips` | `array of strings` | List of IP addresses of the device |
| `uptime` | `string` | Device uptime formatted as `Xd Yh Zm` |

## Example

```json
{
  "user": "my-telegram-bot",
  "device": "my-server",
  "ips": ["192.168.1.10", "10.0.0.5"],
  "uptime": "3d 14h 22m"
}
```

## Failure Ping

On error, agents must send a POST to `<uuid>/fail` with the same body. The `ping_fail` function handles this automatically.

---

## Telegram Notifications

Healthchecks.io includes the ping body as **Last Ping Body** in Telegram notifications (UP, DOWN, and failure events). The body is displayed as raw JSON with syntax highlighting.

Example of what appears in the Telegram message:

```
🟢 The check mySoccer is now UP.

Project: FastAPI
Tags: Telegram, Soccer
Period: 2 minutes
Total Pings: 860
Last Ping: Success, a second ago
Last Ping Body:
{"user":"ronaldo","device":"sandbox","ips":["192.168.122.71","fe80::f9f:d854:2bed:e454","100.70.8.112"],"uptime":"0d 2h 47m"}
```

### Implications for payload design

- Keep field names short and meaningful — they appear directly in the notification
- `user` identifies who sent the ping (agent name)
- `device` and `uptime` give immediate context for diagnosing incidents without leaving Telegram
- Avoid sensitive data in the body (IPs are acceptable; avoid tokens or passwords)
