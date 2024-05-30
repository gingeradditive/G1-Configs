#!/bin/bash

# Banner
echo "                                                        
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
  !P#######GJ:                        ~5B######BY^                              "
echo
echo "G1-Config"
echo "Version 0.0.2 - By: Giacomo Guaresi"
echo; echo

# Check if the script is run as root and exit if true
if [ "$EUID" -eq 0 ]; then
  echo "Please do NOT run this script as root or with sudo."
  exit 1
fi

# Function to install a package if not already installed
install_if_missing() {
    if ! dpkg -l | grep -q "^ii  $1 "; then
        echo "Installing $1..."
        sudo apt-get install -y "$1"
    else
        echo "$1 is already installed."
    fi
}

# UPGRADE SYSTEM
echo ">>>>>> UPGRADE SYSTEM <<<<<<"
sudo apt update && sudo apt full-upgrade -y
echo

# INSTALLING KIAUH
echo ">>>>>> INSTALLING KIAUH <<<<<<"
install_if_missing git
cd ~ 
if [ ! -d "kiauh" ]; then
    git clone https://github.com/dw-0/kiauh.git
else
    echo "KIAUH is already cloned."
fi
echo

# INSTALLING MOONRAKER-OBICO
echo ">>>>>> INSTALLING MOONRAKER-OBICO <<<<<<"
cd ~
if [ ! -d "moonraker-obico" ]; then
    git clone https://github.com/TheSpaghettiDetective/moonraker-obico.git
    cd moonraker-obico
    ./install.sh
else
    echo "Moonraker-Obico is already cloned."
fi
echo

# INSTALLING KLIPPAIN SHAKETUNE
echo ">>>>>> INSTALLING KLIPPAIN SHAKETUNE <<<<<<"
wget -O - https://raw.githubusercontent.com/Frix-x/klippain-shaketune/main/install.sh | bash
echo

# INSTALLING KAMP
echo ">>>>>> INSTALLING KAMP <<<<<<"
cd ~
if [ ! -d "Klipper-Adaptive-Meshing-Purging" ]; then
    git clone https://github.com/kyleisah/Klipper-Adaptive-Meshing-Purging.git
    ln -s ~/Klipper-Adaptive-Meshing-Purging/Configuration printer_data/config/KAMP
    cp ~/Klipper-Adaptive-Meshing-Purging/Configuration/KAMP_Settings.cfg ~/printer_data/config/KAMP_Settings.cfg
else
    echo "KAMP is already cloned."
fi
echo

# ENABLE USB
echo ">>>>>> ENABLE USB <<<<<<"
ln -s /media /home/pi/printer_data/gcodes/
RULES_FILE="/etc/udev/rules.d/usbstick.rules"
RULE='ACTION=="add", KERNEL=="sd[a-z][0-9]", TAG+="systemd", ENV{SYSTEMD_WANTS}="usbstick-handler@%k"'
if ! grep -Fxq "$RULE" "$RULES_FILE"; then
    echo "$RULE" | sudo tee -a "$RULES_FILE"
    echo "USB rule added to $RULES_FILE"
else
    echo "USB rule already exists in $RULES_FILE"
fi
sudo udevadm control --reload-rules && sudo udevadm trigger
echo "udev rules reloaded"

SERVICE_FILE="/lib/systemd/system/usbstick-handler@.service"
SERVICE_CONTENT="[Unit]
Description=Mount USB sticks
BindsTo=dev-%i.device
After=dev-%i.device

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/bin/pmount --umask 000 --noatime -r --sync %I .
ExecStop=/usr/bin/pumount /dev/%I
"
if [ ! -f "$SERVICE_FILE" ]; then
    echo "$SERVICE_CONTENT" | sudo tee "$SERVICE_FILE" > /dev/null
    sudo chmod 644 "$SERVICE_FILE"
    sudo systemctl daemon-reload
    echo "USB handler service created and systemd daemons reloaded"
else
    echo "USB handler service already exists"
fi
echo

# INSTALL POWERBUTTON
echo ">>>>>> INSTALL POWERBUTTON <<<<<<"
cd ~/
install_if_missing pmount
if [ ! -d "pi-power-button" ]; then
    git clone https://github.com/Howchoo/pi-power-button.git
    ./pi-power-button/script/install
else
    echo "Power button is already cloned."
fi
echo

# INSTALL SPLASHSCREEN
echo ">>>>>> INSTALL SPLASHSCREEN <<<<<<"
install_if_missing fbi

BOOT_CONFIG="/boot/config.txt"
CMDLINE_CONFIG="/boot/cmdline.txt"
if ! grep -q "disable_splash=1" "$BOOT_CONFIG"; then
    echo "disable_splash=1" | sudo tee -a "$BOOT_CONFIG"
fi

if ! grep -q "logo.nologo consoleblank=0 loglevel=1 quiet" "$CMDLINE_CONFIG"; then
    sudo sed -i '1s/$/ logo.nologo consoleblank=0 loglevel=1 quiet/' "$CMDLINE_CONFIG"
fi
echo "Boot configuration files modified successfully."

SPLASH_SERVICE_FILE="/etc/systemd/system/splashscreen.service"
SPLASH_SERVICE_CONTENT="[Unit]
Description=Splash screen
DefaultDependencies=no
After=local-fs.target

[Service]
ExecStart=/usr/bin/fbi -d /dev/fb0 --noverbose -a /home/pi/printer_data/config/splash.png
StandardInput=tty
StandardOutput=tty

[Install]
WantedBy=sysinit.target"
if [ ! -f "$SPLASH_SERVICE_FILE" ]; then
    echo "$SPLASH_SERVICE_CONTENT" | sudo tee "$SPLASH_SERVICE_FILE" > /dev/null
    sudo chmod 644 "$SPLASH_SERVICE_FILE"
    sudo systemctl daemon-reload
    sudo systemctl enable splashscreen.service
    echo "Splashscreen service created and enabled"
else
    echo "Splashscreen service already exists"
fi
sudo systemctl enable splashscreen
echo

# INSTALLING KLIPPERSCREEN
echo ">>>>>> INSTALLING KLIPPERSCREEN <<<<<<"
cd ~/
if [ ! -d "KlipperScreen" ]; then
    git clone https://github.com/KlipperScreen/KlipperScreen.git
    ./KlipperScreen/scripts/KlipperScreen-install.sh
else
    echo "KlipperScreen is already cloned."
fi
echo

echo ">>>>>> MOVE GINGER CONFIGS <<<<<<"
SYMBOLIC_LINK_DESTINATION="$HOME/printer_data/config/gingersConfigs" 
if [ -L "$SYMBOLIC_LINK_DESTINATION" ]; then
    sudo rm "$SYMBOLIC_LINK_DESTINATION"
    echo "Symbolic link removed"
fi

echo "Copying G1-Configs to printer_data/config"
G1_CONFIGS_DIR="$HOME/G1-Configs/Configs"
if [ -d "$G1_CONFIGS_DIR" ]; then
    cp -r "$G1_CONFIGS_DIR"/* "$HOME/printer_data/config/"
    sudo rm "$SYMBOLIC_LINK_DESTINATION"
else
    echo "G1-Configs directory does not exist."
fi

MOONRAKER_CONF="$HOME/printer_data/config/moonraker.conf"
MOONRAKER_CONF_CONTENT="
## Ginger Configs
[update_manager GingerConfigs]
type: git_repo
origin: https://github.com/gingeradditive/G1-Configs.git
path: $HOME/G1-Configs
primary_branch: main
managed_services: klipper"
if ! sudo grep -q "Ginger Configs" "$MOONRAKER_CONF"; then
    echo "$MOONRAKER_CONF_CONTENT" | sudo tee -a "$MOONRAKER_CONF" > /dev/null
    echo "Ginger Configs added to $MOONRAKER_CONF"
else
    echo "Ginger Configs already present in $MOONRAKER_CONF"
fi

sudo ln -s "$HOME/G1-Configs" "$SYMBOLIC_LINK_DESTINATION"
echo "Symbolic link recreated for Ginger Configs"
echo

# User interaction for final action
echo ">>>>>> FINAL ACTION <<<<<<"
echo "Choose an action:"
echo "R - Reboot"
echo "S - Shutdown"
echo "X - Exit"

read -rp "Enter your choice (R/S/X): " choice

case "$choice" in
    [Rr]* )
        echo "Rebooting..."
        sudo reboot
        ;;
    [Ss]* )
        echo "Shutting down..."
        sudo shutdown now
        ;;
    [Xx]* )
        echo "Exiting installation."
        exit 0
        ;;
    * )
        echo "Invalid choice. Exiting installation."
        exit 1
        ;;
esac
