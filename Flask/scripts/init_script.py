import os
import json
import subprocess

def run(serial_number: str, timezone: str):
    print(f"[Init Script] Serial: {serial_number}, Timezone: {timezone}")

    # Path setup
    if os.name == "nt":
        basePath = os.getcwd()
        databasePath = os.path.normpath(os.path.join(basePath, "..", "out", "database"))
    else:
        databasePath = os.path.normpath(os.path.join("/home", "pi", "printer_data", "database"))

    # Assicurati che la cartella esista
    os.makedirs(databasePath, exist_ok=True)

    # Percorso del file G1.Conf
    g1_conf_path = os.path.join(databasePath, "G1.Conf")

    # Se esiste, rimuovilo
    if os.path.exists(g1_conf_path):
        os.remove(g1_conf_path)

    # Crea il JSON con serial_number
    data = {
        "serial_number": serial_number
    }

    with open(g1_conf_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"[Init Script] Created {g1_conf_path} with serial {serial_number}")

    # Gestione timezone
    if os.name == "nt":
        print(f"[Init Script] (Windows) Would set timezone to: {timezone}")
    else:
        try:
            # su Raspberry/Linux
            subprocess.run(["sudo", "timedatectl", "set-timezone", timezone], check=True)
            print(f"[Init Script] Timezone set to {timezone}")
        except Exception as e:
            print(f"[Init Script] Failed to set timezone: {e}")
