#!/bin/bash

# INSTALLING GINGER STYLES
echo ">>>>>> INSTALLING GINGER STYLES <<<<<<"
cd ~

echo "Install klipperscreen styles"
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

echo "Install mainsail styles"
mkdir /home/pi/printer_data/config/.theme
ln -sf $HOME/G1-Configs/Styles/mainsail-ginger/*.* "/home/pi/printer_data/config/.theme/"

echo "Activate light mode default"
# sed  "defaultMode": "dark" to "defaultMode": "light",
sed -i 's/"defaultMode": "dark"/"defaultMode": "light"/' /home/pi/mainsail/config.json
