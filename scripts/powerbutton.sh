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