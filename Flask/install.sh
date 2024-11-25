#!/bin/bash
echo "install falsk"
sudo apt update
sudo apt install python3 python3-pip
pip3 install flask

echo "run flask"
python3 /home/pi/G1-Configs/Flask/server.py

# TODO: Write 
# location /g1config {
#     proxy_pass http://127.0.0.1:5000/;
#     proxy_http_version 1.1;
#     proxy_set_header Upgrade $http_upgrade;
#     proxy_set_header Connection "upgrade";
#     proxy_set_header Host $host;
#     proxy_cache_bypass $http_upgrade;
# }
# INTO: /etc/nginx/sites-available/mainsail
# THEN RUN: sudo systemctl reload nginx
