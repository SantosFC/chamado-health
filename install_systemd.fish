#!/usr/bin/env fish

set SCRIPT_DIR (dirname (realpath (status filename)))
set CONFIG_FILE "$HOME/.config/health-monitor"

mkdir -p "$HOME/.config/systemd/user"
cp "$SCRIPT_DIR/systemd/health-monitor.service" "$HOME/.config/systemd/user/"
cp "$SCRIPT_DIR/systemd/health-monitor.timer" "$HOME/.config/systemd/user/"

echo "Arquivos de unit systemd copiados para ~/.config/systemd/user/."

systemctl --user daemon-reload
systemctl --user enable --now health-monitor.timer
systemctl --user status --no-pager health-monitor.timer

# Ping de teste imediato para confirmar que tudo funciona
echo ""
echo "Executando ping de teste..."
if python3 "$SCRIPT_DIR/healthcheck.py"
    echo "Ping OK — instalação concluída com sucesso."
else
    echo "AVISO: o ping de teste falhou. Verifique a URL em $CONFIG_FILE."
end
