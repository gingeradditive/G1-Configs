import os
import json
import requests


# Return 
#   True: Aggiornamento completato con successo
#   False: Aggiornamento fallito 
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

    # --- Percorsi principali ---
    g1_conf_path = os.path.join(databasePath, "G1.Conf")
    update_temp_path = os.path.join(databasePath, "G1-Update.temp")

    # --- Controllo presenza file ---
    if not os.path.exists(g1_conf_path):
        print(f"[Update Script] File non trovato: {g1_conf_path}")
        return False
    if not os.path.exists(update_temp_path):
        print(f"[Update Script] Nessun aggiornamento da eseguire ({update_temp_path} mancante).")
        return True  # niente da aggiornare → considerato successo

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

    if not updates:
        print("[Update Script] Nessun file da aggiornare.")
        os.remove(update_temp_path)
        return True

    # --- Imposta variabili GitHub ---
    GITHUB_REPO = "gingeradditive/G1-Printers"
    RAW_BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main"

    success_count = 0
    failed_files = []

    # --- Scarica e sostituisci i file aggiornati ---
    for f in updates:
        filename = f["file"]
        new_sha = f["new"]
        url = f"{RAW_BASE_URL}/{serial_number}/{filename}"
        local_dest = os.path.join(configPath, filename)

        try:
            print(f"[Update Script] Scaricamento {filename}...")
            resp = requests.get(url)
            resp.raise_for_status()

            # Scrivi file sul disco (sostituendo se esiste)
            with open(local_dest, "w", encoding="utf-8") as local_file:
                local_file.write(resp.text)

            # Aggiorna hash nel file G1.Conf
            g1_conf[filename] = new_sha
            success_count += 1
            print(f"[Update Script] Aggiornato: {filename}")

        except Exception as e:
            print(f"[Update Script] Errore durante l'aggiornamento di {filename}: {e}")
            failed_files.append(filename)

    # --- Salva nuovo stato in G1.Conf ---
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

    print(f"[Update Script] Aggiornamento completato con successo ({success_count} file).")
    return True


# Per test manuale
if __name__ == "__main__":
    print(run())
