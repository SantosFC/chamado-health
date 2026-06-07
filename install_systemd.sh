#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${HOME}/.config/health-check"

mkdir -p "${HOME}/.config/systemd/user"
cp "${SCRIPT_DIR}/systemd/health-check.service" "${HOME}/.config/systemd/user/"
cp "${SCRIPT_DIR}/systemd/health-check.timer" "${HOME}/.config/systemd/user/"

echo "Arquivos de unit systemd copiados para ~/.config/systemd/user/."

systemctl --user daemon-reload
systemctl --user enable --now health-check.timer
systemctl --user status --no-pager health-check.timer

# Ping de teste imediato para confirmar que tudo funciona
echo ""
echo "Executando ping de teste..."
if python3 "${SCRIPT_DIR}/healthcheck.py"; then
    echo "Ping OK — instalação concluída com sucesso."
else
    echo "AVISO: o ping de teste falhou. Verifique a URL em ${CONFIG_FILE}."
fi
