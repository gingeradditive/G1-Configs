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

# Checkpoint file
CHECKPOINT_FILE="$HOME/G1-Configs/scripts/checkpoint.txt"

# Function to set checkpoint
set_checkpoint() {
    echo "$1" > "$CHECKPOINT_FILE"
}

# Function to get checkpoint
get_checkpoint() {
    if [ -f "$CHECKPOINT_FILE" ]; then
        cat "$CHECKPOINT_FILE"
    else
        echo "0"
    fi
}

# Get the current checkpoint
checkpoint=$(get_checkpoint)

# Execute scripts based on checkpoint
if [ "$checkpoint" -le 1 ]; then
    # UPGRADE SYSTEM
    sh "$HOME/G1-Configs/scripts/upgrade.sh"
    set_checkpoint 2
fi

if [ "$checkpoint" -le 2 ]; then
    # INSTALLING KIAUH
    sh "$HOME/G1-Configs/scripts/kiauh.sh"
    set_checkpoint 3
fi

if [ "$checkpoint" -le 3 ]; then
    # INSTALLING MOONRAKER-OBICO
    sh "$HOME/G1-Configs/scripts/moonraker-obico.sh"
    set_checkpoint 4
fi

if [ "$checkpoint" -le 4 ]; then
    # INSTALLING KLIPPAIN SHAKETUNE
    sh "$HOME/G1-Configs/scripts/shaketune.sh"
    set_checkpoint 5
fi

if [ "$checkpoint" -le 5 ]; then
    # INSTALLING KAMP
    sh "$HOME/G1-Configs/scripts/kamp.sh"
    set_checkpoint 6
fi

if [ "$checkpoint" -le 6 ]; then
    # ENABLE USB
    sh "$HOME/G1-Configs/scripts/usb.sh"
    set_checkpoint 7
fi

if [ "$checkpoint" -le 7 ]; then
    # INSTALL POWERBUTTON
    sh "$HOME/G1-Configs/scripts/powerbutton.sh"
    set_checkpoint 8
fi

if [ "$checkpoint" -le 8 ]; then
    # INSTALL SPLASHSCREEN
    sh "$HOME/G1-Configs/scripts/splashscreen.sh"
    set_checkpoint 9
fi

if [ "$checkpoint" -le 9 ]; then
    # INSTALLING KLIPPERSCREEN
    sh "$HOME/G1-Configs/scripts/klipperscreen.sh"
    set_checkpoint 10
fi

if [ "$checkpoint" -le 10 ]; then
    # INSTALLING GINGER CONFIGS
    sh "$HOME/G1-Configs/scripts/gingerconfig.sh"
    set_checkpoint 11
fi

if [ "$checkpoint" -le 11 ]; then
    # INSTALLING GINGER STYLES
    sh "$HOME/G1-Configs/scripts/gingerstyles.sh"
    set_checkpoint 12
fi

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
