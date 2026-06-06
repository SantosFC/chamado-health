#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/SantosFC/health-monitor.git"
INSTALL_DIR="${HOME}/src/health-monitor"
CONFIG_FILE="${HOME}/.config/health-monitor"

# 1. Verificar pré-requisitos
for cmd in git python3 systemctl loginctl; do
    command -v "$cmd" &>/dev/null || { echo "ERRO: '$cmd' não encontrado. Instale e tente novamente."; exit 1; }
done

# 2. Capturar URL
if [[ -z "${HEALTHCHECK_URL:-}" ]]; then
    read -rp "HEALTHCHECK_URL: " HEALTHCHECK_URL </dev/tty
fi

# 3. Validar URL antes de prosseguir
echo "Validando URL..."
if ! python3 -c "
import urllib.request, sys
try:
    urllib.request.urlopen('${HEALTHCHECK_URL}', timeout=10)
    print('URL acessível.')
except Exception as e:
    print(f'AVISO: não foi possível alcançar a URL: {e}', file=sys.stderr)
    sys.exit(1)
" 2>/dev/null; then
    echo "AVISO: não foi possível alcançar a URL informada."
    read -rp "Continuar mesmo assim? [s/N] " confirm </dev/tty
    [[ "$confirm" =~ ^[sS]$ ]] || { echo "Instalação cancelada."; exit 1; }
fi

# 4. Clonar ou atualizar repositório
if [[ -d "${INSTALL_DIR}/.git" ]]; then
    git -C "${INSTALL_DIR}" pull --ff-only
else
    git clone "${REPO_URL}" "${INSTALL_DIR}"
fi

# 5. Salvar configuração (confirmando antes de sobrescrever)
if [[ -f "${CONFIG_FILE}" ]]; then
    echo "Configuração existente encontrada em ${CONFIG_FILE}."
    read -rp "Deseja substituir? [s/N] " confirm </dev/tty
    if [[ ! "$confirm" =~ ^[sS]$ ]]; then
        echo "Configuração mantida. Prosseguindo com valor existente."
    else
        echo "HEALTHCHECK_URL=${HEALTHCHECK_URL}" > "${CONFIG_FILE}"
        echo "Configuração salva em ${CONFIG_FILE}."
    fi
else
    echo "HEALTHCHECK_URL=${HEALTHCHECK_URL}" > "${CONFIG_FILE}"
    echo "Configuração salva em ${CONFIG_FILE}."
fi

bash "${INSTALL_DIR}/install_systemd.sh"

loginctl enable-linger
echo "Linger habilitado — o timer executa mesmo sem sessão ativa."
