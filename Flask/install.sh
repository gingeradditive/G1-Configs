#!/bin/bash

echo "Installing Flask..."
pip3 install flask

# Avvia il server Flask
# echo "Starting Flask server..."
# python3 /home/pi/G1-Configs/Flask/server.py &

# Configura Nginx
echo "Configuring Nginx..."
NGINX_CONF="/etc/nginx/sites-available/mainsail"
if [ ! -f "$NGINX_CONF" ]; then
    sudo bash -c "cat > $NGINX_CONF" <<EOF
server {
    listen 80;
    server_name localhost;

    location /g1config {
        proxy_pass http://127.0.0.1:5000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF
    # Abilita la configurazione di Nginx
    sudo ln -s /etc/nginx/sites-available/mainsail /etc/nginx/sites-enabled/
    sudo systemctl reload nginx
    echo "Nginx configured and reloaded."
else
    echo "Nginx configuration already exists."
fi

# Crea un servizio systemd per avviare automaticamente Flask all'avvio
echo "Creating systemd service for Flask..."
SERVICE_FILE="/etc/systemd/system/g1-flask.service"
sudo bash -c "cat > $SERVICE_FILE" <<EOF
[Unit]
Description=Flask server for G1-Configs
After=network.target

[Service]
User=$USER
WorkingDirectory=/home/pi/G1-Configs/Flask
ExecStart=/usr/bin/python3 /home/pi/G1-Configs/Flask/server.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Abilita e avvia il servizio Flask
sudo systemctl daemon-reload
sudo systemctl enable g1-flask.service
sudo systemctl start g1-flask.service

echo "Flask service created and started successfully."

# Verifica lo stato del servizio
sudo systemctl status g1-flask.service
