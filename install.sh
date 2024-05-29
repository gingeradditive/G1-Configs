#!/bin/bash
echo "                                                        
          .-.                                           
  .--.   ( __)  ___ .-.     .--.     .--.    ___ .-.    
 /    \  (''') (   )   \   /    \   /    \  (   )   \   
;  ,-. '  | |   |  .-. .  ;  ,-. ' |  .-. ;  | ' .-. ;  
| |  | |  | |   | |  | |  | |  | | |  | | |  |  / (___) 
| |  | |  | |   | |  | |  | |  | | |  |/  |  | |        
| |  | |  | |   | |  | |  | |  | | |  ' _.'  | |        
| '  | |  | |   | |  | |  | '  | | |  .'.-.  | |        
'  '-' |  | |   | |  | |  '  '-' | '  '-' /  | |        
 '.__. | (___) (___)(___)  '.__. |  '.__.'  (___)       
 ( '-' ;                   ( '-' ;                      
  '.__.                     '.__.'                       "

echo "Script for fast G1 installation"
echo "Version 0.0.1 - By: Giacomo Guaresi"
#-------------------------------------------------------------------------------

echo; echo ">>>>>> UPGRADE SYSTEM <<<<<<"
sudo apt update
sudo apt full-upgrade -y
echo
#-------------------------------------------------------------------------------
echo; echo ">>>>>> INSTALLING KIAUH <<<<<<"
sudo apt-get update 
sudo apt-get install git -y
cd ~ 
git clone https://github.com/dw-0/kiauh.git
echo
#-------------------------------------------------------------------------------
echo; echo ">>>>>> INSTALLING MOONRAKER-OBICO <<<<<<"
cd ~
git clone https://github.com/TheSpaghettiDetective/moonraker-obico.git
cd moonraker-obico
./install.sh
echo
#-------------------------------------------------------------------------------
echo; echo ">>>>>> INSTALLING KLIPPAIN SHAKETUNE <<<<<<"
wget -O - https://raw.githubusercontent.com/Frix-x/klippain-shaketune/main/install.sh | bash
echo
#-------------------------------------------------------------------------------
echo; echo ">>>>>> INSTALLING KAMP <<<<<<"
cd ~
git clone https://github.com/kyleisah/Klipper-Adaptive-Meshing-Purging.git
ln -s ~/Klipper-Adaptive-Meshing-Purging/Configuration printer_data/config/KAMP
cp ~/Klipper-Adaptive-Meshing-Purging/Configuration/KAMP_Settings.cfg ~/printer_data/config/KAMP_Settings.cfg
echo
#-------------------------------------------------------------------------------
echo; echo ">>>>>> ENABLE USB <<<<<<"
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
sudo echo "$SERVICE_CONTENT" | sudo tee "$SERVICE_FILE"
sudo systemctl daemon-reload
echo "Il file di servizio è stato creato e i daemon di systemd sono stati ricaricati"
echo
#-------------------------------------------------------------------------------
echo; echo ">>>>>> INSTALL POWERBUTTON <<<<<<"
cd ~/
sudo apt-get install pmount -y
git clone https://github.com/Howchoo/pi-power-button.git
./pi-power-button/script/install
echo
#-------------------------------------------------------------------------------
echo; echo ">>>>>> INSTALL SPLASHSCREEN <<<<<<"
cd ~/

if ! grep -q "disable_splash=1" /boot/config.txt; then
    sudo echo "disable_splash=1" >> /boot/config.txt
fi
if ! grep -q "logo.nologo consoleblank=0 loglevel=1 quiet" /boot/cmdline.txt; then
    sudo sed -i '1s/$/ logo.nologo consoleblank=0 loglevel=1 quiet/' /boot/cmdline.txt
fi

echo "Modifiche ai file di configurazione effettuate con successo."

SERVICE_FILE="/etc/systemd/system/splashscreen.service"
SERVICE_CONTENT="[Unit]
Description=Splash screen
DefaultDependencies=no
After=local-fs.target

[Service]
ExecStart=/usr/bin/fbi -d /dev/fb0 --noverbose -a /home/pi/printer_data/config/splash.png
StandardInput=tty
StandardOutput=tty

[Install]
WantedBy=sysinit.target"

if [ ! -f "$SERVICE_FILE" ]; then
    sudo echo "$SERVICE_CONTENT" > "$SERVICE_FILE"
    sudo chmod 644 "$SERVICE_FILE"
    sudo systemctl daemon-reload
    sudo systemctl enable splashscreen.service
    echo "Il servizio splashscreen è stato creato e abilitato con successo."
else
    echo "Il file $SERVICE_FILE esiste già. Nessuna modifica effettuata."
fi

sudo apt-get update
sudo systemctl enable splashscreen
echo
#-------------------------------------------------------------------------------
echo; echo ">>>>>> INSTALLING KLIPPERSCREEN <<<<<<"
cd ~/
git clone https://github.com/KlipperScreen/KlipperScreen.git
./KlipperScreen/scripts/KlipperScreen-install.sh
echo
#-------------------------------------------------------------------------------
echo; echo ">>>>>> MOVE GINGER CONFIGS <<<<<<"
echo "Moving G1-Configs to printer_data/config"
cp -r ./G1-Configs/Configs/* ./printer_data/config/
echo
#-------------------------------------------------------------------------------
echo; echo ">>>>>> REBOOT <<<<<<"
echo "bye bye!"
sudo reboot