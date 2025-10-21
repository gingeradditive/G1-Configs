import os
import json
import requests
import subprocess


def check_moonraker_updates(moonraker_url="http://localhost:7125"):
    print("[CheckForUpdate Script] Controllo aggiornamenti Moonraker/Klipper...")

    try:
        response = requests.get(f"{moonraker_url}/machine/update/status", timeout=5)
        response.raise_for_status()
        data = response.json().get("result", {}).get("version_info", {})

        updates_available = []

        for name, info in data.items():
            local_ver = info.get("version")
            remote_ver = info.get("remote_version")
            if local_ver != remote_ver:
                updates_available.append({
                    "component": name,
                    "local": local_ver,
                    "remote": remote_ver
                })

        if updates_available:
            print("[CheckForUpdate Script] 🔄 Aggiornamenti disponibili (Moonraker):")
            for u in updates_available:
                print(f" - {u['component']}: {u['local']} → {u['remote']}")
        else:
            print("[CheckForUpdate Script] ✅ Moonraker/Klipper/Mainsail sono aggiornati.")

        return updates_available

    except requests.RequestException as e:
        print(f"[CheckForUpdate Script] ❌ Errore nel contatto con Moonraker: {e}")
        return []


def check_raspberry_updates():
    print("[CheckForUpdate Script] Controllo aggiornamenti Raspberry (APT)...")

    try:
        # Aggiorna la lista dei pacchetti ma non installa nulla
        subprocess.run(["sudo", "apt-get", "update", "-qq"], check=True)

        # Controlla pacchetti aggiornabili
        result = subprocess.run(
            ["apt", "list", "--upgradable"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        lines = [
            line for line in result.stdout.splitlines()
            if line and not line.startswith("Listing...")
        ]

        if lines:
            print("[CheckForUpdate Script] 🔄 Aggiornamenti APT disponibili:")
            for line in lines:
                print("  -", line)
        else:
            print("[CheckForUpdate Script] ✅ Nessun aggiornamento APT disponibile.")

        return lines

    except subprocess.CalledProcessError as e:
        print(f"[CheckForUpdate Script] ❌ Errore durante il controllo APT: {e}")
        return []


def run():
    print("[CheckForUpdate Script] Checking for updates...")

    # --- Path setup ---
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
    update_file_path = os.path.join(databasePath, "G1-Update.temp")

    if not os.path.exists(g1_conf_path):
        print(f"[CheckForUpdate Script] File not found: {g1_conf_path}")
        return "system not initialized"

    # --- Carica G1.Conf ---
    try:
        with open(g1_conf_path, "r") as f:
            g1_conf = json.load(f)
    except Exception as e:
        print(f"[CheckForUpdate Script] Errore nella lettura di G1.Conf: {e}")
        return "system not initialized"

    serial_number = g1_conf.get("serial_number")
    if not serial_number:
        print("[CheckForUpdate Script] Serial number mancante in G1.Conf.")
        return "system not initialized"

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

        filename = os.path.basename(item["path"])
        local_file_path = os.path.join(configPath, filename)
        local_sha = g1_conf.get(filename)

        # 1️⃣ Controlla se il file esiste localmente
        file_exists = os.path.exists(local_file_path)

        # 2️⃣ Recupera l'ultimo commit SHA remoto
        try:
            commits_url = f"{GITHUB_API_URL}/commits"
            params = {"path": item["path"], "per_page": 1}
            commit_data = requests.get(commits_url, params=params).json()
            if not commit_data:
                continue
            latest_sha = commit_data[0]["sha"]
        except Exception as e:
            print(f"[CheckForUpdate Script] Errore nel recupero commit per {filename}: {e}")
            continue

        # 3️⃣ Determina se serve aggiornamento
        if (not file_exists) or (local_sha != latest_sha):
            files_to_update.append({
                "file": filename,
                "old": local_sha,
                "new": latest_sha
            })

    # --- Nuovi controlli ---
    moonraker_updates = check_moonraker_updates()
    raspberry_updates = check_raspberry_updates()

    # --- Gestione risultati ---
    all_updates = {
        "files": files_to_update,
        "moonraker": moonraker_updates,
        "raspberry": raspberry_updates
    }

    try:
        with open(update_file_path, "w") as f:
            json.dump(all_updates, f, indent=2)
    except Exception as e:
        print(f"[CheckForUpdate Script] Errore nel salvataggio di G1-Update.temp: {e}")
        return ""

    has_updates = bool(files_to_update or moonraker_updates or raspberry_updates)

    if not has_updates:
        print("[CheckForUpdate Script] Tutti i componenti sono aggiornati.")
        return ""

    print("[CheckForUpdate Script] ✅ File aggiornamenti salvato in:", update_file_path)
    print("[CheckForUpdate Script] Update available.")
    return "update available"


# Per test manuale
if __name__ == "__main__":
    print(run())
