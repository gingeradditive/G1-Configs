import os
import json
import requests


def run():
    print("[CheckForUpdate Script] Checking for updates...")

    # Path setup
    if os.name == "nt":
        basePath = os.getcwd()
        configPath = os.path.normpath(os.path.join(basePath, "..", "out", "config"))
        databasePath = os.path.normpath(os.path.join(basePath, "..", "out", "database"))
        backupConfigPath = os.path.normpath(os.path.join(basePath, "..", "Configs"))
        backupStylesPath = os.path.normpath(os.path.join(basePath, "..", "Styles"))
        backupDatabasePath = os.path.normpath(os.path.join(basePath, "..", "Database"))
    else:
        configPath = os.path.normpath(os.path.join("/home", "pi", "printer_data", "config"))
        databasePath = os.path.normpath(os.path.join("/home", "pi", "printer_data", "database"))
        backupConfigPath = os.path.normpath(os.path.join("/home", "pi", "G1-Configs", "Configs"))
        backupStylesPath = os.path.normpath(os.path.join("/home", "pi", "G1-Configs", "Styles"))
        backupDatabasePath = os.path.normpath(os.path.join("/home", "pi", "G1-Configs", "Database"))

    # --- Controllo presenza file G1.Conf ---
    g1_conf_path = os.path.join(databasePath, "G1.Conf")

    if not os.path.exists(g1_conf_path):
        print(f"[CheckForUpdate Script] File not found: {g1_conf_path}")
        return "system not initialized"

    # --- Carica il file di configurazione G1.Conf ---
    try:
        with open(g1_conf_path, "r") as f:
            g1_conf = json.load(f)
    except Exception as e:
        print(f"[CheckForUpdate Script] Errore nella lettura di G1.Conf: {e}")
        return ""

    serial_number = g1_conf.get("serial_number")
    if not serial_number:
        print("[CheckForUpdate Script] Serial number mancante in G1.Conf.")
        return ""

    print(f"[CheckForUpdate Script] Serial: {serial_number}")

    # --- Imposta variabili GitHub ---
    GITHUB_REPO = "gingeradditive/G1-Printers"
    GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}"
    files_to_update = []

    # --- Ottieni lista file remoti nella cartella del seriale ---
    try:
        contents_url = f"{GITHUB_API_URL}/contents/{serial_number}"
        response = requests.get(contents_url)
        response.raise_for_status()
        contents = response.json()
    except Exception as e:
        print(f"[CheckForUpdate Script] Errore nel recupero contenuti da GitHub: {e}")
        return ""

    # --- Cicla i file e confronta commit hash ---
    for item in contents:
        if item["type"] != "file":
            continue
        remote_path = item["path"]

        # Recupera l'ultimo commit SHA che ha modificato il file
        try:
            commits_url = f"{GITHUB_API_URL}/commits"
            params = {"path": remote_path, "per_page": 1}
            commit_data = requests.get(commits_url, params=params).json()
            if not commit_data:
                continue
            latest_sha = commit_data[0]["sha"]
        except Exception as e:
            print(f"[CheckForUpdate Script] Errore nel recupero commit per {remote_path}: {e}")
            continue

        local_sha = g1_conf.get(os.path.basename(remote_path))  # es. "config.cfg"

        if local_sha != latest_sha:
            files_to_update.append({
                "file": os.path.basename(remote_path),
                "old": local_sha,
                "new": latest_sha
            })

    # --- Gestione risultati ---
    update_file_path = os.path.join(databasePath, "G1-Update.temp")

    if not files_to_update:
        print("[CheckForUpdate Script] Tutti i file sono aggiornati.")
        # Sovrascrive eventuale file vecchio per coerenza
        with open(update_file_path, "w") as f:
            json.dump([], f, indent=2)
        return ""

    print("[CheckForUpdate Script] Aggiornamenti disponibili per:")
    for f in files_to_update:
        if f["old"]:
            print(f" - {f['file']}: {f['old']} → {f['new']}")
        else:
            print(f" - {f['file']} (nuovo file da scaricare)")

    # --- Salva elenco aggiornamenti in G1-Update.temp ---
    try:
        with open(update_file_path, "w") as f:
            json.dump(files_to_update, f, indent=2)
        print(f"[CheckForUpdate Script] File aggiornamenti salvato in: {update_file_path}")
    except Exception as e:
        print(f"[CheckForUpdate Script] Errore nel salvataggio di G1-Update.temp: {e}")
        return ""

    print("[CheckForUpdate Script] Update available.")
    return "update available"


# Per test manuale
if __name__ == "__main__":
    print(run())
