import os
import json


# Return 
#   True: Factory reset completato con successo
#   False: Factory reset fallito 
def run():
    print("[FactoryReset Script] Performing factory reset...")

    # --- Path setup ---
    if os.name == "nt":
        basePath = os.getcwd()
        configPath = os.path.normpath(os.path.join(basePath, "..", "out", "config"))
        databasePath = os.path.normpath(os.path.join(basePath, "..", "out", "database"))
    else:
        configPath = os.path.normpath(os.path.join("/home", "pi", "printer_data", "config"))
        databasePath = os.path.normpath(os.path.join("/home", "pi", "printer_data", "database"))

    g1_conf_path = os.path.join(databasePath, "G1.Conf")
    update_temp_path = os.path.join(databasePath, "G1-Update.temp")

    try:
        # --- Carica file G1.Conf se esiste ---
        if not os.path.exists(g1_conf_path):
            print(f"[FactoryReset Script] Nessun file G1.Conf trovato ({g1_conf_path}).")

            # Rimuove comunque il file G1-Update.temp se presente
            if os.path.exists(update_temp_path):
                os.remove(update_temp_path)
                print(f"[FactoryReset Script] Rimosso file temporaneo: {update_temp_path}")

            print("[FactoryReset Script] Nulla da resettare.")
            return True

        with open(g1_conf_path, "r") as f:
            g1_conf = json.load(f)

        serial_number = g1_conf.get("serial_number", "unknown")
        tracked_files = [k for k in g1_conf.keys() if k != "serial_number"]

        print(f"[FactoryReset Script] Serial: {serial_number}")
        if not tracked_files:
            print("[FactoryReset Script] Nessun file tracciato trovato in G1.Conf.")

        # --- Elimina i file tracciati ---
        for filename in tracked_files:
            file_path = os.path.join(configPath, filename)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"[FactoryReset Script] Rimosso: {file_path}")
                except Exception as e:
                    print(f"[FactoryReset Script] Errore durante la rimozione di {file_path}: {e}")
            else:
                print(f"[FactoryReset Script] File non trovato (già rimosso?): {file_path}")

        # --- Elimina G1.Conf ---
        try:
            os.remove(g1_conf_path)
            print(f"[FactoryReset Script] Rimosso file di configurazione: {g1_conf_path}")
        except Exception as e:
            print(f"[FactoryReset Script] Errore durante la rimozione di G1.Conf: {e}")

        # --- Elimina G1-Update.temp se presente ---
        if os.path.exists(update_temp_path):
            try:
                os.remove(update_temp_path)
                print(f"[FactoryReset Script] Rimosso file temporaneo: {update_temp_path}")
            except Exception as e:
                print(f"[FactoryReset Script] Errore durante la rimozione di G1-Update.temp: {e}")

        print("[FactoryReset Script] Factory reset completato con successo.")
        return True

    except Exception as e:
        print(f"[FactoryReset Script] Errore durante il factory reset: {e}")
        return False


# Per test manuale
if __name__ == "__main__":
    print(run())
