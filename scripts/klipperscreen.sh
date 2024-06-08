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