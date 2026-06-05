# Chamado Health

Simple health check script for Healthchecks.io, designed to run every minute using a systemd timer.

## Installation

1. Copy the systemd unit files to your user systemd directory:

   ```bash
   mkdir -p ~/.config/systemd/user
   cp systemd/chamado-health.service ~/.config/systemd/user/
   cp systemd/chamado-health.timer ~/.config/systemd/user/
   ```

2. Update the `HEALTHCHECK_URL` in the service unit or set it in `~/.config/chamado-health`.

3. Reload the user daemon and enable the timer:

   ```bash
   systemctl --user daemon-reload
   systemctl --user enable --now chamado-health.timer
   systemctl --user status chamado-health.timer
   ```

4. If you change the service or timer unit later, reload the user daemon and restart the timer using the unit name (not the file path):

   ```bash
   systemctl --user daemon-reload
   systemctl --user restart --now chamado-health.timer
   systemctl --user list-timers --all | grep chamado-health
   journalctl --user -u chamado-health.service -n 10 --no-pager
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
