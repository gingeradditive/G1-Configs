import os
import json


class UpdateMainsailMenu:
    def __init__(self):
        if os.name == "nt":
            basePath = os.getcwd()
            self.configPath = os.path.normpath(
                os.path.join(basePath, "..", "out", "config"))
            self.databasePath = os.path.normpath(
                os.path.join(basePath, "..", "out", "database"))

            self.backupConfigPath = os.path.normpath(
                os.path.join(basePath, "..", "Configs"))
            self.backupStylesPath = os.path.normpath(
                os.path.join(basePath, "..", "Styles"))
            self.backupDatabasePath = os.path.normpath(
                os.path.join(basePath, "..", "Database"))
        else:
            self.configPath = os.path.normpath(
                os.path.join("/home", "pi", "printer_data", "config"))
            self.databasePath = os.path.normpath(
                os.path.join("/home", "pi", "printer_data", "database"))

            self.backupConfigPath = os.path.normpath(
                os.path.join("/home", "pi", "G1-Configs", "Configs"))
            self.backupStylesPath = os.path.normpath(
                os.path.join("/home", "pi", "G1-Configs", "Styles"))
            self.backupDatabasePath = os.path.normpath(
                os.path.join("/home", "pi", "G1-Configs", "Database"))

    def set_to_system_ok(self, url):
        try:
            # percorso della cartella .theme dentro configPath
            themeFolderPath = os.path.join(self.configPath, ".theme")
            os.makedirs(themeFolderPath, exist_ok=True)

            # percorso del file navi.json
            navi_path = os.path.join(themeFolderPath, "navi.json")

            # contenuto da scrivere
            data = [
                {
                    "title": "by Ginger Additive",
                    "href": f"{url}:5000/checkforupdate",
                    "icon": "M7.5,5.6L5,7L6.4,4.5L5,2L7.5,3.4L10,2L8.6,4.5L10,7L7.5,5.6M19.5,15.4L22,14L20.6,16.5L22,19L19.5,17.6L17,19L18.4,16.5L17,14L19.5,15.4M22,2L20.6,4.5L22,7L19.5,5.6L17,7L18.4,4.5L17,2L19.5,3.4L22,2M13.34,12.78L15.78,10.34L13.66,8.22L11.22,10.66L13.34,12.78M14.37,7.29L16.71,9.63C17.1,10 17.1,10.65 16.71,11.04L5.04,22.71C4.65,23.1 4,23.1 3.63,22.71L1.29,20.37C0.9,20 0.9,19.35 1.29,18.96L12.96,7.29C13.35,6.9 14,6.9 14.37,7.29Z"
                }
            ]

            # scrittura su file
            with open(navi_path, "w") as json_file:
                json.dump(data, json_file, indent=2)

            return True

        except Exception as e:
            return False

    def set_to_update_available(self, url):
        try:
            # percorso della cartella .theme dentro configPath
            themeFolderPath = os.path.join(self.configPath, ".theme")
            os.makedirs(themeFolderPath, exist_ok=True)

            # percorso del file navi.json
            navi_path = os.path.join(themeFolderPath, "navi.json")

            # contenuto da scrivere
            data = [
                {
                    "title": "UPDATE G1",
                    "href": f"{url}:5000/update",
                    "icon": "M7.5,5.6L5,7L6.4,4.5L5,2L7.5,3.4L10,2L8.6,4.5L10,7L7.5,5.6M19.5,15.4L22,14L20.6,16.5L22,19L19.5,17.6L17,19L18.4,16.5L17,14L19.5,15.4M22,2L20.6,4.5L22,7L19.5,5.6L17,7L18.4,4.5L17,2L19.5,3.4L22,2M13.34,12.78L15.78,10.34L13.66,8.22L11.22,10.66L13.34,12.78M14.37,7.29L16.71,9.63C17.1,10 17.1,10.65 16.71,11.04L5.04,22.71C4.65,23.1 4,23.1 3.63,22.71L1.29,20.37C0.9,20 0.9,19.35 1.29,18.96L12.96,7.29C13.35,6.9 14,6.9 14.37,7.29Z"
                }
            ]

            # scrittura su file
            with open(navi_path, "w") as json_file:
                json.dump(data, json_file, indent=2)

            return True

        except Exception as e:
            return False

    def set_to_initialize_printer(self, url):
        try:
            # percorso della cartella .theme dentro configPath
            themeFolderPath = os.path.join(self.configPath, ".theme")
            os.makedirs(themeFolderPath, exist_ok=True)

            # percorso del file navi.json
            navi_path = os.path.join(themeFolderPath, "navi.json")

            # contenuto da scrivere
            data = [
                {
                    "title": "INITIALIZE PRINTER",
                    "href": f"{url}:5000/init",
                    "icon": "M7.5,5.6L5,7L6.4,4.5L5,2L7.5,3.4L10,2L8.6,4.5L10,7L7.5,5.6M19.5,15.4L22,14L20.6,16.5L22,19L19.5,17.6L17,19L18.4,16.5L17,14L19.5,15.4M22,2L20.6,4.5L22,7L19.5,5.6L17,7L18.4,4.5L17,2L19.5,3.4L22,2M13.34,12.78L15.78,10.34L13.66,8.22L11.22,10.66L13.34,12.78M14.37,7.29L16.71,9.63C17.1,10 17.1,10.65 16.71,11.04L5.04,22.71C4.65,23.1 4,23.1 3.63,22.71L1.29,20.37C0.9,20 0.9,19.35 1.29,18.96L12.96,7.29C13.35,6.9 14,6.9 14.37,7.29Z"
                }
            ]

            # scrittura su file
            with open(navi_path, "w") as json_file:
                json.dump(data, json_file, indent=2)

            return True

        except Exception as e:
            return False
