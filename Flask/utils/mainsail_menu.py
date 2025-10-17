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
                    "icon": "M 13.241547 0.0038189954 C 13.011319 -0.0018136849 12.778704 -0.00065518721 12.543204 0.0063042022 C 8.7791343 0.11765397 5.6945157 1.6805158 3.1553357 4.4125758 C -1.0083643 8.8944158 -1.1197186 16.452365 3.2249214 21.113165 C 5.4976614 23.548865 8.2618496 24.963778 11.5864 25.176478 C 15.6149 25.434978 19.130356 24.218529 22.085156 21.220029 L 22.091369 21.222514 C 22.061569 22.453314 22.004333 23.554772 21.845333 24.648372 C 21.517233 26.885372 20.374847 28.545104 18.348647 29.598904 C 16.497447 30.561304 14.533033 30.868042 12.471133 30.810442 C 9.0828933 30.714942 6.3458107 29.455834 4.5085307 26.511034 C 4.3474707 26.254534 4.1539371 26.111887 3.8337971 26.115887 C 2.7799471 26.125787 1.7277027 26.123787 0.67385668 26.115887 C 0.27021268 26.113887 0.19071439 26.264697 0.34580939 26.626597 C 1.4732304 29.269197 3.1622441 31.440272 5.7511341 32.762572 C 9.6165741 34.736972 13.677902 34.904268 17.801902 33.762868 C 21.082702 32.854168 23.502528 30.853765 24.878528 27.690265 C 25.677828 25.852965 25.918841 23.882872 25.934741 21.918372 C 25.990441 15.020572 25.962989 8.1200677 25.976989 1.2203277 C 25.976989 0.78487371 25.817768 0.60598426 25.384268 0.61393726 C 24.529268 0.62785626 23.673777 0.64351524 22.820777 0.60772424 C 22.242177 0.58187524 22.055043 0.80275212 22.078943 1.3694401 C 22.116743 2.2522901 22.088883 3.1392902 22.088883 4.1951202 C 19.563071 1.5797671 16.694968 0.088309199 13.241547 0.0038189954 z M 13.473914 3.7925167 C 16.406448 3.8263031 18.847744 5.0099719 20.627582 7.5501494 C 22.554282 10.298129 22.741324 13.362156 21.468824 16.402456 C 20.176324 19.490356 17.649276 21.079081 14.362376 21.454881 C 11.837176 21.743181 9.4386807 21.349237 7.3627907 19.782337 C 5.0860807 18.064437 3.8454699 15.787185 3.8971699 12.693285 C 3.8985191 8.2223984 7.5187372 4.288529 12.186577 3.8471913 C 12.625027 3.8056825 13.054981 3.7876901 13.473914 3.7925167 z M 31.557521 19.31139 C 29.612054 19.312656 28.133978 20.790679 28.137877 22.72855 C 28.141877 24.63145 29.692888 26.184674 31.579888 26.176774 C 33.472788 26.168774 34.999533 24.620226 34.999533 22.707426 C 34.999533 20.775547 33.515374 19.312634 31.560007 19.31139 L 31.558764 19.31139 L 31.557521 19.31139 z "
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
