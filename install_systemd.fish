#!/usr/bin/env fish

set SCRIPT_DIR (dirname (realpath (status filename)))
set CONFIG_FILE "$HOME/.config/chamado-health"

mkdir -p "$HOME/.config/systemd/user"
cp "$SCRIPT_DIR/systemd/chamado-health.service" "$HOME/.config/systemd/user/"
cp "$SCRIPT_DIR/systemd/chamado-health.timer" "$HOME/.config/systemd/user/"

echo "Arquivos de unit systemd copiados para ~/.config/systemd/user/."

systemctl --user daemon-reload
systemctl --user enable --now chamado-health.timer
systemctl --user status --no-pager chamado-health.timer

# Ping de teste imediato para confirmar que tudo funciona
echo ""
echo "Executando ping de teste..."
if python3 "$SCRIPT_DIR/healthcheck.py"
    echo "Ping OK — instalação concluída com sucesso."
else
    echo "AVISO: o ping de teste falhou. Verifique a URL em $CONFIG_FILE."
end
