# Chamado Health

Simple health check script for Healthchecks.io, designed to run every minute using a systemd timer.

## Installation

### 1. Install Git

```bash
# Debian/Ubuntu
sudo apt update && sudo apt install -y git python3

# RHEL/CentOS/Fedora
sudo dnf install -y git python3
```

### 2. Configure Git identity

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### 3. Clone the repository

```bash
mkdir -p ~/src
git clone https://github.com/SantosFC/health-check.git ~/src/health-check
cd ~/src/health-check
```

### 4. Run the setup script

```bash
bash setup.sh
```

The script will:
1. Ask for your `HEALTHCHECK_URL` (Healthchecks.io ping endpoint) and validate it.
2. Ask for a `DEVICE_NAME` to identify this machine.
3. Save the configuration to `~/.config/health-check`.
4. Install and enable the systemd timer.
5. Run a test ping to confirm everything works.

> Both `HEALTHCHECK_URL` and `DEVICE_NAME` can be pre-set as environment variables to skip the interactive prompts:
> ```bash
> HEALTHCHECK_URL=https://hc-ping.com/<your-uuid> DEVICE_NAME=my-machine bash setup.sh
> ```

## Configuration

The configuration file is `~/.config/health-check`:

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
