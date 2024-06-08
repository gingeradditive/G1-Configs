# INSTALLING MOONRAKER-OBICO
echo ">>>>>> INSTALLING MOONRAKER-OBICO <<<<<<"
cd ~
if [ ! -d "moonraker-obico" ]; then
    git clone https://github.com/TheSpaghettiDetective/moonraker-obico.git
    cd moonraker-obico
    ./install.sh
else
    echo "Moonraker-Obico is already cloned."
fi
echo