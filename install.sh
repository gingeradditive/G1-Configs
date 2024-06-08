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
./scripts/upgrade.sh

# INSTALLING KIAUH
./scripts/kiauh.sh

# INSTALLING MOONRAKER-OBICO
./scripts/moonraker-obico.sh

# INSTALLING KLIPPAIN SHAKETUNE
./scripts/shaketune.sh

# INSTALLING KAMP
./scripts/kamp.sh

# ENABLE USB
./scripts/usb.sh

# INSTALL POWERBUTTON
./scripts/powerbutton.sh

# INSTALL SPLASHSCREEN
./scripts/splashscreen.sh

# INSTALLING KLIPPERSCREEN
./scripts/klipperscreen.sh

# INSTALLING GINGER CONFIGS
./scripts/gingerconfig.sh

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
