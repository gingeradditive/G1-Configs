#!/bin/bash

# INSTALLING GINGER CONFIGS
echo ">>>>>> MOVE GINGER CONFIGS <<<<<<"

# Ask the user if they want to create a symbolic link or copy the files
read -p "Do you want to create a symbolic link (L) or copy the files (C)? [L/C]: " user_choice

SYMBOLIC_LINK_DESTINATION="$HOME/printer_data/config/gingersConfigs"
G1_CONFIGS_DIR="$HOME/G1-Configs/Configs"
MOONRAKER_CONF="$HOME/printer_data/config/moonraker.conf"

MOONRAKER_CONF_CONTENT="
## Ginger Configs
[update_manager GingerConfigs]
type: git_repo
origin: https://github.com/gingeradditive/G1-Configs.git
path: $HOME/G1-Configs
primary_branch: main
managed_services: klipper"

case $user_choice in
    [Ll]* )
        # Copy the files
        echo "Copying G1-Configs to printer_data/config"
        if [ -d "$G1_CONFIGS_DIR" ]; then
            cp -r "$G1_CONFIGS_DIR"/* "$HOME/printer_data/config/"
            echo "G1-Configs copied to printer_data/config"
        else
            echo "G1-Configs directory does not exist."
            exit 1
        fi
        
        # Remove the existing gingersConfigs folder or link if it exists
        if [ -e "$SYMBOLIC_LINK_DESTINATION" ]; then
            sudo rm -rf "$SYMBOLIC_LINK_DESTINATION"
            echo "Existing gingersConfigs removed"
        fi
        
        # Create the symbolic link
        sudo ln -s "$HOME/G1-Configs/Configs/gingersConfigs" "$SYMBOLIC_LINK_DESTINATION"
        sudo chown -h pi:pi "$SYMBOLIC_LINK_DESTINATION"
        echo "Symbolic link created for Ginger Configs"

        # Add the configuration to moonraker.conf if not already present
        if ! sudo grep -q "Ginger Configs" "$MOONRAKER_CONF"; then
            echo "$MOONRAKER_CONF_CONTENT" | sudo tee -a "$MOONRAKER_CONF" > /dev/null
            echo "Ginger Configs added to $MOONRAKER_CONF"
        else
            echo "Ginger Configs already present in $MOONRAKER_CONF"
        fi
        ;;
    [Cc]* )
        # Copy the files
        echo "Copying G1-Configs to printer_data/config"
        if [ -d "$G1_CONFIGS_DIR" ]; then
            cp -r "$G1_CONFIGS_DIR"/* "$HOME/printer_data/config/"
            echo "G1-Configs copied to printer_data/config"
        else
            echo "G1-Configs directory does not exist."
            exit 1
        fi
        ;;
    * )
        echo "Invalid choice. Please run the script again and choose either L or C."
        exit 1
        ;;
esac
echo
