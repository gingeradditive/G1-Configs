#!/bin/bash

echo "Installing Flask..."
pip3 install flask

# Avvia il server Flask
# echo "Starting Flask server..."
# python3 /home/pi/G1-Configs/Flask/server.py &

# Configura Nginx
echo "Configuring Nginx..."
NGINX_CONF="/etc/nginx/sites-available/mainsail"

if grep -q "location /g1config" "$NGINX_CONF"; then
    echo "The 'location /g1config' block already exists in $NGINX_CONF."
else
    echo "Adding 'location /g1config' block to $NGINX_CONF..."
    sudo sed -i '/^}$/i \ \ \ \ location /g1config {\n\ \ \ \ \ \ proxy_pass http://127.0.0.1:5000/;\n\ \ \ \ \ \ proxy_http_version 1.1;\n\ \ \ \ \ \ proxy_set_header Upgrade $http_upgrade;\n\ \ \ \ \ \ proxy_set_header Connection "upgrade";\n\ \ \ \ \ \ proxy_set_header Host $host;\n\ \ \ \ \ \ proxy_cache_bypass $http_upgrade;\n\ \ \ \ }' "$NGINX_CONF"
    sudo systemctl reload nginx
    echo "Nginx configuration updated and reloaded."
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