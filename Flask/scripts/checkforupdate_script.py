import os
import json


# Return
#   "update available": Aggiornamenti disponibili
#   "system not initialized": Sistama non inizializzato
#   "": Tutto aggiornato / Errore
def run():
    print("[CheckForUpdate Script] Checking for updates...")

    # Path setup
    if os.name == "nt":
        basePath = os.getcwd()
        configPath = os.path.normpath(
            os.path.join(basePath, "..", "out", "config"))
        databasePath = os.path.normpath(
            os.path.join(basePath, "..", "out", "database"))

        backupConfigPath = os.path.normpath(
            os.path.join(basePath, "..", "Configs"))
        backupStylesPath = os.path.normpath(
            os.path.join(basePath, "..", "Styles"))
        backupDatabasePath = os.path.normpath(
            os.path.join(basePath, "..", "Database"))
    else:
        configPath = os.path.normpath(os.path.join(
            "/home", "pi", "printer_data", "config"))
        databasePath = os.path.normpath(os.path.join(
            "/home", "pi", "printer_data", "database"))

        backupConfigPath = os.path.normpath(
            os.path.join("/home", "pi", "G1-Configs", "Configs"))
        backupStylesPath = os.path.normpath(
            os.path.join("/home", "pi", "G1-Configs", "Styles"))
        backupDatabasePath = os.path.normpath(
            os.path.join("/home", "pi", "G1-Configs", "Database"))

    # --- Controllo presenza file G1.Conf ---
    g1_conf_path = os.path.join(databasePath, "G1.Conf")

    if not os.path.exists(g1_conf_path):
        print(f"[CheckForUpdate Script] File not found: {g1_conf_path}")
        return "system not initialized"

    # TODO: aggiungere logica per controllare davvero gli update

    # TODO: aggiungere logica per controllare corruzione/assenza file locali 

    print("[CheckForUpdate Script] Update available.")
    return "update available"
