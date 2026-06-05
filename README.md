# Chamado Health

Simple health check script for Healthchecks.io, designed to run every minute using a systemd timer.

## Installation

1. Copy the systemd unit files to `/etc/systemd/system/`:

   ```bash
   sudo cp systemd/chamado-health.service /etc/systemd/system/
   sudo cp systemd/chamado-health.timer /etc/systemd/system/
   ```

2. Update the `HEALTHCHECK_URL` in the service unit or set it in `/etc/default/chamado-health`.

3. Reload systemd and enable the timer:

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now chamado-health.timer
   sudo systemctl status chamado-health.timer
   ```

## Configuration

- `HEALTHCHECK_URL` must be set to your Healthchecks.io ping endpoint.
- You can also pass the URL as a command-line argument to the script:

  ```bash
  ./healthcheck.py https://hc-ping.com/<your-uuid>
  ```

## Script behavior

- Sends an HTTP GET to the configured Healthchecks.io URL.
- Exits with code `0` when the request succeeds with `2xx`.
- Logs diagnostic errors to journal if the request fails.
