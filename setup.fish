#!/usr/bin/env fish

set REPO_URL "https://github.com/SantosFC/health-check.git"
set INSTALL_DIR "$HOME/src/health-monitor"
set CONFIG_FILE "$HOME/.config/health-monitor"

# 1. Verificar pré-requisitos
for cmd in git python3 systemctl loginctl
    if not command -q $cmd
        echo "ERRO: '$cmd' não encontrado. Instale e tente novamente."
        exit 1
    end
end

# 2. Capturar URL
if not set -q HEALTHCHECK_URL
    read -P "HEALTHCHECK_URL: " HEALTHCHECK_URL
end

# 3. Validar URL antes de prosseguir
echo "Validando URL..."
if not python3 -c "
import urllib.request, sys
try:
    urllib.request.urlopen('$HEALTHCHECK_URL', timeout=10)
    print('URL acessível.')
except Exception as e:
    print(f'AVISO: não foi possível alcançar a URL: {e}', file=sys.stderr)
    sys.exit(1)
" 2>/dev/null
    echo "AVISO: não foi possível alcançar a URL informada."
    read -P "Continuar mesmo assim? [s/N] " confirm
    if not string match -qi 's' $confirm
        echo "Instalação cancelada."
        exit 1
    end
end

# 4. Capturar nome do device
if not set -q DEVICE_NAME
    read -P "Nome do device: " DEVICE_NAME
end

# 5. Clonar ou atualizar repositório
if test -d "$INSTALL_DIR/.git"
    git -C $INSTALL_DIR pull --ff-only
else
    git clone $REPO_URL $INSTALL_DIR
end

# 6. Salvar configuração (confirmando antes de sobrescrever)
if test -f $CONFIG_FILE
    echo "Configuração existente encontrada em $CONFIG_FILE."
    read -P "Deseja substituir? [s/N] " confirm
    if string match -qi 's' $confirm
        printf "HEALTHCHECK_URL=%s\nDEVICE_NAME=%s\n" $HEALTHCHECK_URL $DEVICE_NAME > $CONFIG_FILE
        echo "Configuração salva em $CONFIG_FILE."
    else
        echo "Configuração mantida. Prosseguindo com valor existente."
    end
else
    printf "HEALTHCHECK_URL=%s\nDEVICE_NAME=%s\n" $HEALTHCHECK_URL $DEVICE_NAME > $CONFIG_FILE
    echo "Configuração salva em $CONFIG_FILE."
end

fish "$INSTALL_DIR/install_systemd.fish"

loginctl enable-linger
echo "Linger habilitado — o timer executa mesmo sem sessão ativa."
