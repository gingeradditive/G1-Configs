#!/bin/bash

# Prendi i parametri in ingresso
PLR_MOVE_COUNT=$1
PLR_LAST_FILE=$2

# Percorso dello script Python (modifica se necessario)
PYTHON_SCRIPT=./generate_resumed_file.py

# Esegui lo script Python con i parametri
python3 "$PYTHON_SCRIPT" "$PLR_MOVE_COUNT" "$PLR_LAST_FILE"
