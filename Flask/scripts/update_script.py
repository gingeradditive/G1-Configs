import os
import json
import requests
import re
import subprocess
import time


def get_mainboard_serial():
    """Legge il serial della mainboard Klipper."""
    if os.name == "nt":
        return "/dev/serial/by-id/usb-Klipper_stm32h723xx_XXXXXXXXXXXXXXXXXXXXXXXX-XXXX"
    try:
        serials = os.listdir("/dev/serial/by-id/")
        serial = next((s for s in serials if "usb-Klipper" in s), None)
        if serial:
            return f"/dev/serial/by-id/{serial}"
        return "Nessun dispositivo trovato"
    except FileNotFoundError:
        return "Directory /dev/serial/by-id/ non trovata"


def get_extruder_board_serial():
    """Legge il serial della scheda estrusore."""
    if os.name == "nt":
        return "/dev/serial/by-id/usb-1a86_USB2.0-XXXX-XXXX-XXXXX"
    try:
        serials = os.listdir("/dev/serial/by-id/")
        serial = next((s for s in serials if "usb-1a86_USB" in s), None)
        if serial:
            return f"/dev/serial/by-id/{serial}"
        return "Nessun dispositivo trovato"
    except FileNotFoundError:
        return "Directory /dev/serial/by-id/ non trovata"


def update_printer_cfg_serials(printer_cfg_path):
    """Aggiorna i seriali nel file printer.cfg."""
    if not os.path.exists(printer_cfg_path):
        print(f"[Update Script] printer.cfg non trovato: {printer_cfg_path}")
        return

    try:
        with open(printer_cfg_path, "r", encoding="utf-8") as f:
            content = f.read()

        main_serial = get_mainboard_serial()
        extruder_serial = get_extruder_board_serial()

        # Aggiorna le righe con regex
        content = re.sub(
            r"(serial:\s*/dev/serial/by-id/usb-Klipper[^\n]*)",
            f"serial: {main_serial}",
            content
        )
        content = re.sub(
            r"(serial:\s*/dev/serial/by-id/usb-1a86_USB[^\n]*)",
            f"serial: {extruder_serial}",
            content
        )

        with open(printer_cfg_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"[Update Script] Seriali aggiornati in printer.cfg")
    except Exception as e:
        print(f"[Update Script] Errore durante l'aggiornamento dei seriali: {e}")


def update_moonraker(moonraker_url="http://localhost:7125"):
    """Controlla e aggiorna Moonraker/Klipper/Mainsail se necessario."""
    print("[Update Script] Avvio aggiornamento Moonraker/Klipper...")

    try:
        # 1️⃣ Controlla lo stato degli aggiornamenti
        status_resp = requests.get(f"{moonraker_url}/machine/update/status", timeout=5)
        status_resp.raise_for_status()
        status_data = status_resp.json().get("result", {})
        repos = status_data.get("version_info", {})

        if not repos:
            print("[Update Script] ⚠️ Nessun repository trovato in Moonraker.")
            return

        updates_found = False
        for name, info in repos.items():
            local = info.get("version")
            remote = info.get("remote_version")
            if local != remote:
                updates_found = True
                print(f"[Update Script] 🔄 Aggiornamento disponibile per {name}: {local} → {remote}")
                # 2️⃣ Avvia aggiornamento singolo repo
                try:
                    repo_resp = requests.post(f"{moonraker_url}/machine/update/repo?repo={name}", timeout=10)
                    if repo_resp.status_code == 200:
                        print(f"[Update Script] ✅ Aggiornamento di {name} avviato correttamente.")
                    else:
                        print(f"[Update Script] ⚠️ Errore nell'avviare update di {name}: {repo_resp.status_code}")
                except requests.RequestException as e:
                    print(f"[Update Script] ❌ Errore aggiornando {name}: {e}")

        if not updates_found:
            print("[Update Script] ✅ Tutti i componenti Moonraker/Klipper sono già aggiornati.")

    except requests.RequestException as e:
        print(f"[Update Script] ❌ Errore durante la connessione a Moonraker: {e}")


def update_raspberry():
    """Esegue apt-get upgrade automatico."""
    print("[Update Script] Avvio aggiornamento pacchetti Raspberry (APT)...")
    try:
        subprocess.run(["sudo", "apt-get", "update", "-qq"], check=True)
        subprocess.run(["sudo", "apt-get", "upgrade", "-y"], check=True)
        subprocess.run(["sudo", "apt-get", "autoremove", "-y"], check=True)
        print("[Update Script] ✅ Aggiornamento APT completato.")
    except subprocess.CalledProcessError as e:
        print(f"[Update Script] ❌ Errore durante aggiornamento APT: {e}")


def run():
    print("[Update Script] Running update...")

    # --- Path setup ---
    if os.name == "nt":
        basePath = os.getcwd()
        configPath = os.path.normpath(os.path.join(basePath, "..", "out", "config"))
        databasePath = os.path.normpath(os.path.join(basePath, "..", "out", "database"))
        backupConfigPath = os.path.normpath(os.path.join(basePath, "..", "Configs"))
    else:
        configPath = os.path.normpath(os.path.join("/home", "pi", "printer_data", "config"))
        databasePath = os.path.normpath(os.path.join("/home", "pi", "printer_data", "database"))
        backupConfigPath = os.path.normpath(os.path.join("/home", "pi", "G1-Configs", "Configs"))

    g1_conf_path = os.path.join(databasePath, "G1.Conf")
    update_temp_path = os.path.join(databasePath, "G1-Update.temp")

    if not os.path.exists(g1_conf_path):
        print(f"[Update Script] File non trovato: {g1_conf_path}")
        return False
    if not os.path.exists(update_temp_path):
        print(f"[Update Script] Nessun aggiornamento da eseguire ({update_temp_path} mancante).")
        return True

    # --- Carica configurazione locale e lista update ---
    try:
        with open(g1_conf_path, "r") as f:
            g1_conf = json.load(f)
        with open(update_temp_path, "r") as f:
            updates = json.load(f)
    except Exception as e:
        print(f"[Update Script] Errore nel caricamento file di configurazione: {e}")
        return False

    serial_number = g1_conf.get("serial_number")
    if not serial_number:
        print("[Update Script] Serial number mancante in G1.Conf.")
        return False

    success_count = 0
    failed_files = []

    # --- Aggiornamento file GitHub ---
    if "files" in updates and updates["files"]:
        print("[Update Script] Inizio aggiornamento file di configurazione...")
        GITHUB_REPO = "gingeradditive/G1-Printers"
        RAW_BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main"

        for f in updates["files"]:
            filename = f["file"]
            new_sha = f["new"]
            url = f"{RAW_BASE_URL}/{serial_number}/{filename}"
            local_dest = os.path.join(configPath, filename)

            try:
                print(f"[Update Script] Scaricamento {filename}...")
                resp = requests.get(url)
                resp.raise_for_status()

                with open(local_dest, "w", encoding="utf-8") as local_file:
                    local_file.write(resp.text)

                g1_conf[filename] = new_sha
                success_count += 1
                print(f"[Update Script] Aggiornato: {filename}")

                if filename == "printer.cfg":
                    update_printer_cfg_serials(local_dest)

            except Exception as e:
                print(f"[Update Script] Errore durante l'aggiornamento di {filename}: {e}")
                failed_files.append(filename)
    else:
        print("[Update Script] Nessun file di configurazione da aggiornare.")

    # --- Aggiornamento Moonraker ---
    if "moonraker" in updates and updates["moonraker"]:
        update_moonraker()
        # Attendere un po' per evitare conflitti con riavvio di servizi
        time.sleep(10)

    # --- Aggiornamento APT ---
    if "raspberry" in updates and updates["raspberry"]:
        update_raspberry()

    # --- Salva nuovo stato G1.Conf ---
    try:
        with open(g1_conf_path, "w") as f:
            json.dump(g1_conf, f, indent=2)
        print("[Update Script] G1.Conf aggiornato con nuovi hash.")
    except Exception as e:
        print(f"[Update Script] Errore nel salvataggio G1.Conf: {e}")
        return False

    # --- Rimuove file temporaneo ---
    try:
        os.remove(update_temp_path)
        print(f"[Update Script] File temporaneo rimosso: {update_temp_path}")
    except Exception as e:
        print(f"[Update Script] Impossibile rimuovere file temporaneo: {e}")

    # --- Risultato finale ---
    if failed_files:
        print("[Update Script] Aggiornamento completato parzialmente. File non aggiornati:")
        for f in failed_files:
            print(f" - {f}")
        return False

    print(f"[Update Script] ✅ Aggiornamento completato con successo ({success_count} file).")
    return True


# Per test manuale
if __name__ == "__main__":
    print(run())
