# Chamado Health

Simple health check script for Healthchecks.io, designed to run every minute using a systemd timer.

## Installation

Run the setup script:

```bash
bash setup.sh
```

The script will:
1. Ask for your `HEALTHCHECK_URL` (Healthchecks.io ping endpoint) and validate it.
2. Ask for a `DEVICE_NAME` to identify this machine.
3. Clone the repository to `~/src/health-monitor`.
4. Save the configuration to `~/.config/health-monitor`.
5. Install and enable the systemd timer via `install_systemd.sh`.
6. Run a test ping to confirm everything works.

> Both `HEALTHCHECK_URL` and `DEVICE_NAME` can be pre-set as environment variables to skip the interactive prompts.

## Configuration

The configuration file is `~/.config/health-monitor`:

```
HEALTHCHECK_URL=https://hc-ping.com/<your-uuid>
DEVICE_NAME=my-machine
```

You can also pass the URL as a command-line argument to the script:

```bash
./healthcheck.py https://hc-ping.com/<your-uuid>
```

## Systemd units

The unit files installed to `~/.config/systemd/user/` are:

- `health-check.service`
- `health-check.timer`

To reload and restart after changes:

```bash
systemctl --user daemon-reload
systemctl --user restart health-check.timer
systemctl --user list-timers --all | grep health-check
journalctl --user -u health-check.service -n 10 --no-pager
```

## Script behavior

- Sends an HTTP GET to the configured Healthchecks.io URL.
- Exits with code `0` when the request succeeds with `2xx`.
- Logs diagnostic errors to journal if the request fails.
