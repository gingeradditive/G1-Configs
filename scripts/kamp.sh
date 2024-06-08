# INSTALLING KAMP
echo ">>>>>> INSTALLING KAMP <<<<<<"
cd ~
if [ ! -d "Klipper-Adaptive-Meshing-Purging" ]; then
    git clone https://github.com/kyleisah/Klipper-Adaptive-Meshing-Purging.git
    ln -s ~/Klipper-Adaptive-Meshing-Purging/Configuration printer_data/config/KAMP
    cp ~/Klipper-Adaptive-Meshing-Purging/Configuration/KAMP_Settings.cfg ~/printer_data/config/KAMP_Settings.cfg
else
    echo "KAMP is already cloned."
fi
echo