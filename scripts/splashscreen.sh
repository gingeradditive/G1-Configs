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