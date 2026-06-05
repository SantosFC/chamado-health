#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "${HOME}/.config/systemd/user"
cp "${SCRIPT_DIR}/systemd/chamado-health.service" "${HOME}/.config/systemd/user/"
cp "${SCRIPT_DIR}/systemd/chamado-health.timer" "${HOME}/.config/systemd/user/"

echo "Copied systemd unit files to ~/.config/systemd/user/."

systemctl --user daemon-reload
systemctl --user enable --now chamado-health.timer
systemctl --user status --no-pager chamado-health.timer
