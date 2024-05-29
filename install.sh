#!/bin/bash

echo ">>>>>> UPGRADE SYSTEM <<<<<<"
sudo apt update
sudo apt full-upgrade

#-------------------------------------------------------------------------------

echo ">>>>>> INSTALLING KIAUH <<<<<<"
sudo apt-get update 
sudo apt-get install git -y
cd ~ 
git clone https://github.com/dw-0/kiauh.git

#-------------------------------------------------------------------------------

echo ">>>>>> INSTALLING MOONRAKER-OBICO <<<<<<"
cd ~
git clone https://github.com/TheSpaghettiDetective/moonraker-obico.git
cd moonraker-obico
./install.sh

#-------------------------------------------------------------------------------

echo ">>>>>> INSTALLING KLIPPAIN SHAKETUNE <<<<<<"
wget -O - https://raw.githubusercontent.com/Frix-x/klippain-shaketune/main/install.sh | bash

echo ">>>>>> INSTALLING KAMP <<<<<<"
cd ~
git clone https://github.com/kyleisah/Klipper-Adaptive-Meshing-Purging.git
ln -s ~/Klipper-Adaptive-Meshing-Purging/Configuration printer_data/config/KAMP
cp ~/Klipper-Adaptive-Meshing-Purging/Configuration/KAMP_Settings.cfg ~/printer_data/config/KAMP_Settings.cfg

#-------------------------------------------------------------------------------

echo ">>>>>> MOVE GINGER CONFIGS <<<<<<"
echo "TODO"

#-------------------------------------------------------------------------------

echo ">>>>>> ENABLE USB <<<<<<"
ln -s /usb /home/pi/printer_data/gcodes/
RULES_FILE="/etc/udev/rules.d/usbstick.rules"
RULE='ACTION=="add", KERNEL=="sd[a-z][0-9]", TAG+="systemd", ENV{SYSTEMD_WANTS}="usbstick-handler@%k"'

if grep -Fxq "$RULE" "$RULES_FILE"; then
    echo "La regola esiste già nel file $RULES_FILE"
else
    # Aggiungi la regola al file
    echo "$RULE" | sudo tee -a "$RULES_FILE"
    echo "La regola è stata aggiunta al file $RULES_FILE"
fi
sudo udevadm control --reload-rules
sudo udevadm trigger
echo "Regole udev ricaricate"

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
echo "$SERVICE_CONTENT" | sudo tee "$SERVICE_FILE"
sudo systemctl daemon-reload
echo "Il file di servizio è stato creato e i daemon di systemd sono stati ricaricati"

#-------------------------------------------------------------------------------

echo ">>>>>> INSTALL POWERBUTTON <<<<<<"
cd ~/
git clone https://github.com/Howchoo/pi-power-button.git
./pi-power-button/script/install

#-------------------------------------------------------------------------------

echo ">>>>>> INSTALLING KLIPPERSCREEN <<<<<<"
cd ~/
git clone https://github.com/KlipperScreen/KlipperScreen.git
./KlipperScreen/scripts/KlipperScreen-install.sh