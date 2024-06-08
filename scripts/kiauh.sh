# INSTALLING KIAUH
echo ">>>>>> INSTALLING KIAUH <<<<<<"
install_if_missing git
cd ~ 
if [ ! -d "kiauh" ]; then
    git clone https://github.com/dw-0/kiauh.git
else
    echo "KIAUH is already cloned."
fi
echo