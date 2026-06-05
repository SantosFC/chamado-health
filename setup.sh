#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/SantosFC/chamado-health.git"
INSTALL_DIR="${HOME}/src/chamado-health"
CONFIG_FILE="${HOME}/.config/chamado-health"

if [[ -z "${HEALTHCHECK_URL:-}" ]]; then
    read -rp "HEALTHCHECK_URL: " HEALTHCHECK_URL
fi

if [[ -d "${INSTALL_DIR}/.git" ]]; then
    git -C "${INSTALL_DIR}" pull --ff-only
else
    git clone "${REPO_URL}" "${INSTALL_DIR}"
fi

echo "HEALTHCHECK_URL=${HEALTHCHECK_URL}" > "${CONFIG_FILE}"
echo "Config saved to ${CONFIG_FILE}."

bash "${INSTALL_DIR}/install_systemd.sh"

loginctl enable-linger
echo "Linger enabled — timer runs even without active session."
