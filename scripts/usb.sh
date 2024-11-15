# ENABLE USB
echo ">>>>>> ENABLE USB <<<<<<"
sudo apt install pmount

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