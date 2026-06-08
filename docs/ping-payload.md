# Ping Payload Standard

This document defines the standard payload for all health check pings sent to Healthchecks.io across all agents (scripts, bots, services).

## HTTP Request

- **Method:** `POST`
- **URL:** `https://hc-ping.com/<uuid>`

## Headers

| Header | Value |
|---|---|
| `User-Agent` | `<service-name>/<version>` |
| `Content-Type` | `application/json` |

The `User-Agent` must identify the agent and its version. Examples:

```
health-check/1.0.2
telegram-bot-alerts/2.1.0
```

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

On error, agents must send a POST to `<uuid>/fail` with the same body.
