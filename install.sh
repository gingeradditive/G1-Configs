#!/bin/bash

# Banner
RED='\033[0;31m'
NC='\033[0m'
echo "${RED}                                                        
                 5@?                                                            
    :~!7!~:  :^. ~!^ .^^  ^!77!:        .^!77!^  :^:     :~!77!^.    ^^..!7~.   
 .?B&#GPPG#BJB@7 P@J 7@#JBBPPPB&G!    !G&#GPPGB#YP@5   7B&BGPPB##5^  #@B#BGY    
~#@5^     .!B@@7 P@J 7@@#!.    !@@~ :G@G~.    .~P@@5 :B@5:     .!#@? #@@!       
&@J         .#@7 P@J 7@&:       P@Y 5@P          P@5 G@&YJYYYYYJJP@@~B@Y        
@@!          B@7 P@J 7@#        5@5 P@Y          5@5 #@P7????????777^B@7        
7@&7       :P@@7 P@J 7@#        5@5 ^&@J.      .J@@5 ?@#:        !5~ #@7     :: 
 ^5&#PYJY5G#P#@7 G@J ?@#.       5@5  .J##G5JJ5G#GB@5  7#@P7~^^!JB@P^ #@?    G@@G
^~:.~7JJJ?~.:&@^ ?P! ~PY        7P7 :~^.^7JJJ?!. B@7    !YGGBBGP?^   YP~    ?GG?
~B@P!:. ..^J&&7                     :P@G7:.  .^7B@Y                             
  !P#######GJ:                        ~5B######BY^                              ${NC}"
echo
echo "G1-Config"
echo "Version 0.0.1 - By: Giacomo Guaresi"
echo; echo


SYMBOLIC_LINK_DESTINATION="$HOME/printer_data/config/G1-Configs"
G1_CONFIGS_DIR="$HOME/G1-Configs/Configs"
G1_DATABASE_DIR="$HOME/G1-Configs/Database"

MOONRAKER_CONF="$HOME/printer_data/config/moonraker.conf"
MOONRAKER_CONF_CONTENT="
## Ginger Configs
[update_manager GingerConfigs]
type: git_repo
origin: https://github.com/gingeradditive/G1-Configs.git
path: $HOME/G1-Configs
primary_branch: main
managed_services: klipper"


# Copy the files
echo "Copying G1-Configs to printer_data/config"
if [ -d "$G1_CONFIGS_DIR" ]; then
    cp -r "$G1_CONFIGS_DIR"/* "$HOME/printer_data/config/"
    echo "G1-Configs copied to printer_data/config"
else
    echo "G1-Configs directory does not exist."
    exit 1
fi

# Remove the existing G1-Configs folder or link if it exists
if [ -e "$SYMBOLIC_LINK_DESTINATION" ]; then
    sudo rm -rf "$SYMBOLIC_LINK_DESTINATION"
    echo "Existing G1-Configs removed"
fi

# Create the symbolic link
sudo ln -s "$HOME/G1-Configs/Configs/G1-Configs" "$SYMBOLIC_LINK_DESTINATION"
sudo chown -h pi:pi "$SYMBOLIC_LINK_DESTINATION"
echo "Symbolic link created for Ginger Configs"

# Add the configuration to moonraker.conf if not already present
if ! sudo grep -q "Ginger Configs" "$MOONRAKER_CONF"; then
    echo "$MOONRAKER_CONF_CONTENT" | sudo tee -a "$MOONRAKER_CONF" > /dev/null
    echo "Ginger Configs added to $MOONRAKER_CONF"
else
    echo "Ginger Configs already present in $MOONRAKER_CONF"
fi


echo "Installing klipperscreen style"
ORIGIN_DIR="$HOME/G1-Configs/Styles/klipperscreen-ginger/"
DESTINATION_DIR="$HOME/KlipperScreen/styles/klipperscreen-ginger"
if [ -L "$DESTINATION_DIR" ]; then
    echo "Symbolic link already exists, removing it."
    rm "$DESTINATION_DIR"
fi
ln -s "$ORIGIN_DIR" "$DESTINATION_DIR"

if [ $? -eq 0 ]; then
    echo "Symbolic link created successfully!"
else
    echo "Error creating symbolic link."
fi

echo "Install mainsail style"
mkdir /home/pi/printer_data/config/.theme
ln -sf $HOME/G1-Configs/Styles/mainsail-ginger/*.* "/home/pi/printer_data/config/.theme/"

# echo "Activate light mode default"
# sed -i 's/"defaultMode": "dark"/"defaultMode": "light"/' /home/pi/mainsail/config.json


echo "Installing Flask..."
sudo pip3 install flask

# Crea un servizio systemd per avviare automaticamente Flask all'avvio
echo "Creating systemd service for Flask..."
SERVICE_FILE="/etc/systemd/system/g1-flask.service"
sudo bash -c "cat > $SERVICE_FILE" <<EOF
[Unit]
Description=Flask server for G1-Configs
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/home/pi/G1-Configs/Flask
ExecStart=/usr/bin/python3 /home/pi/G1-Configs/Flask/server.py
Restart=always
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
EOF

# Abilita e avvia il servizio Flask
sudo systemctl daemon-reload
sudo systemctl enable g1-flask.service
sudo systemctl start g1-flask.service

echo "Flask service created and started successfully."

echo "Restoring Moonraker DB..."
cp -f "$G1_DATABASE_DIR"/moonraker-sql.db "$HOME/printer_data/database/"