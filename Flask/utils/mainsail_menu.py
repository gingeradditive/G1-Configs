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
                    "icon": "M 9.4369294,0.8578183 C 9.2983443,0.85417612 9.1583221,0.85492547 9.0165633,0.85942446 6.7507897,0.93142076 4.8940101,1.9419317 3.365556,3.7084197 0.85922563,6.6062756 0.79219614,11.493075 3.4074429,14.506642 c 1.368071,1.574869 3.0319682,2.489719 5.0331741,2.627247 2.424947,0.167139 4.541069,-0.619389 6.319704,-2.558152 l 0.0038,0.0016 c -0.01794,0.795808 -0.05241,1.507985 -0.148101,2.215082 -0.197498,1.446393 -0.885155,2.519538 -2.104823,3.200901 -1.114326,0.622266 -2.296801,0.820596 -3.5379573,0.783353 -2.0395071,-0.06178 -3.6870883,-0.875894 -4.793035,-2.779934 -0.09695,-0.165846 -0.2134469,-0.25808 -0.4061544,-0.255494 -0.6343629,0.0065 -1.2677591,0.0051 -1.9021195,0 -0.2429726,-0.0014 -0.2908265,0.09622 -0.1974674,0.330216 0.6786487,1.708643 1.6953469,3.112412 3.2537238,3.967379 2.3267933,1.276604 4.771501,1.384773 7.2539358,0.646769 1.974869,-0.587543 3.431479,-1.88096 4.259758,-3.926407 0.481137,-1.187956 0.626214,-2.461773 0.635785,-3.731974 0.03352,-4.459962 0.017,-8.9216704 0.02544,-13.3828855 0,-0.2815548 -0.09584,-0.3972206 -0.356787,-0.3920784 -0.514666,0.009 -1.029626,0.019124 -1.543089,-0.00402 -0.348328,-0.016724 -0.460971,0.1260897 -0.446585,0.4924972 0.02275,0.5708308 0.006,1.1443449 0.006,1.8270206 C 13.242158,1.8767906 11.51571,0.91244775 9.4369294,0.8578183 Z m 0.139873,2.4496858 c 1.7652326,0.021844 3.2347656,0.7871789 4.3061366,2.4296 1.159771,1.7767811 1.272361,3.7579114 0.506382,5.7236999 -0.778017,1.996567 -2.299169,3.0238 -4.277711,3.266784 C 8.5915714,14.913996 7.1478022,14.659285 5.8982245,13.64616 4.5277638,12.535404 3.7809807,11.062984 3.8121016,9.0625389 3.8129141,6.171765 5.9920963,3.6282145 8.8018925,3.3428555 9.0658166,3.3160168 9.3246265,3.3043835 9.5768024,3.3075041 Z M 20.462191,13.341655 c -1.17107,8.41e-4 -2.060794,0.956475 -2.058447,2.209458 0.0024,1.230372 0.936036,2.234652 2.071911,2.229544 1.139428,-0.0052 2.058449,-1.006429 2.058449,-2.243202 0,-1.249109 -0.893387,-2.194995 -2.070416,-2.1958 h -7.22e-4 z"
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
                    "icon": "M6.5 20Q4.22 20 2.61 18.43 1 16.85 1 14.58 1 12.63 2.17 11.1 3.35 9.57 5.25 9.15 5.83 7.13 7.39 5.75 8.95 4.38 11 4.08V12.15L9.4 10.6L8 12L12 16L16 12L14.6 10.6L13 12.15V4.08Q15.58 4.43 17.29 6.39 19 8.35 19 11 20.73 11.2 21.86 12.5 23 13.78 23 15.5 23 17.38 21.69 18.69 20.38 20 18.5 20Z"
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
                    "icon": "M20,11H23V13H20V11M1,11H4V13H1V11M13,1V4H11V1H13M4.92,3.5L7.05,5.64L5.63,7.05L3.5,4.93L4.92,3.5M16.95,5.63L19.07,3.5L20.5,4.93L18.37,7.05L16.95,5.63M12,6A6,6 0 0,1 18,12C18,14.22 16.79,16.16 15,17.2V19A1,1 0 0,1 14,20H10A1,1 0 0,1 9,19V17.2C7.21,16.16 6,14.22 6,12A6,6 0 0,1 12,6M14,21V22A1,1 0 0,1 13,23H11A1,1 0 0,1 10,22V21H14M11,18H13V15.87C14.73,15.43 16,13.86 16,12A4,4 0 0,0 12,8A4,4 0 0,0 8,12C8,13.86 9.27,15.43 11,15.87V18Z"
                }
            ]

            # scrittura su file
            with open(navi_path, "w") as json_file:
                json.dump(data, json_file, indent=2)

            return True

        except Exception as e:
            return False
