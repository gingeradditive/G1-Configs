#!/bin/bash

# INSTALLING GINGER STYLES
echo ">>>>>> INSTALLING GINGER STYLES <<<<<<"
cd ~

ORIGIN_DIR="$HOME/G1-Configs/Styles/klipperscreen-ginger/"
DESTINATION_DIR="$HOME/KlipperScreen/styles/klipperscreen-ginger"

if [ -L "$DESTINATION_DIR" ]; then
    echo "Il link simbolico esiste già, verrà rimosso."
    rm "$DESTINATION_DIR"
fi

ln -s "$ORIGIN_DIR" "$DESTINATION_DIR"

if [ $? -eq 0 ]; then
    echo "Link simbolico creato con successo!"
else
    echo "Errore durante la creazione del link simbolico."
fi

echo