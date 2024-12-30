from flask import *
import subprocess
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

if os.name == "nt":
    printerCfgPath = "C:/Users/guare/source/gingerRepos/G1-Configs/Configs/printer.cfg"
    folder_path = "./static/printerCfg_Parts"
else:  
    printerCfgPath = "/home/pi/printer_data/config/printer.cfg"
    folder_path = "./static/printerCfg_Parts"

@app.route('/tools/static/<path:path>')
def send_report(path):
    # Using request args for path will expose you to directory traversal attacks
    return send_from_directory('static', path)

@app.route("/tools/backend/read-printer-cfg", methods=["GET"])
def read_printer_cfg():
    with open(printerCfgPath, "r") as file:
        section = ""
        key = ""
        value = ""
        jsonOutput = {}

        for line in file:
            line = line.rstrip()
            
            if "#" in line:
                line = line[:line.index("#")]
                
            if not line:
                continue

            if line.startswith("[") and line.endswith("]"):
                section = line[1:-1]
                continue
        
            try:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                
            except ValueError:
                continue

            # add to jsonOutput
            if section not in jsonOutput:
                jsonOutput[section] = {}
            jsonOutput[section][key] = value
    
    return jsonify(jsonOutput)
    
@app.route("/tools/backend/write-printer-cfg", methods=["POST"])
def write_printer_cfg():
    values = request.form
    files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith(".cfg")],
        key=lambda x: int(x.split('_')[0])
    )

    with open(printerCfgPath, "w") as outfile:
        for file in files:
            file_path = os.path.join(folder_path, file)
            with open(file_path, "r") as infile:
                for line in infile:
                    if "{{" in line and "}}" in line:
                        try:
                            key = line.split("{{")[1].split("}}")[0]
                            newValue = str(values[key])
                            newValue = newValue.replace("\n", "")
                            line = line.replace("{{" + key + "}}", newValue)
                        except:
                            return jsonify({"success": False})
                            
                    outfile.write(line)
                outfile.write("\n\n") 

    # execute klipper restart
    try:
        # TODO: restart klipper service, currently not working
        # subprocess.run(["sudo", "systemctl", "restart", "klipper.service"], check=True)
        return redirect("/")
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "error": e.stderr}), 500

@app.route("/tools/backend/update-mainboard-serial", methods=["GET"])
def update_mainboard_serial():
    if os.name == "nt":
        serial = "/dev/serial/by-id/usb-Klipper_stm32h723xx_XXXXXXXXXXXXXXXXXXXXXXXX-XXXX"
    else:  
        try:
            serials = os.listdir("/dev/serial/by-id/")
            serial = next(
                (s for s in serials if "usb-Klipper" in s), 
                "Nessun dispositivo trovato"
            )
            serial = f"/dev/serial/by-id/{serial}" if "Nessun dispositivo trovato" not in serial else serial
        except FileNotFoundError:
            serial = "Directory /dev/serial/by-id/ non trovata"

    return jsonify({"success": True, "serial": serial})
    
@app.route("/tools/backend/update-extruder-board-serial", methods=["GET"])
def update_extruder_board_serial():
    if os.name == "nt":
        serial = "/dev/serial/by-id/usb-1a86_USB2.0-XXXX-XXXX-XXXXX"
    else: 
        try:
            serials = os.listdir("/dev/serial/by-id/")  # Legge i seriali disponibili
            serial = next(
                (s for s in serials if "usb-1a86_USB" in s), 
                "Nessun dispositivo trovato"
            )
            serial = f"/dev/serial/by-id/{serial}" if "Nessun dispositivo trovato" not in serial else serial
        except FileNotFoundError:
            serial = "Directory /dev/serial/by-id/ non trovata"
    return jsonify({"success": True, "serial": serial})
 
@app.route("/tools/run/<script_name>", methods=["POST"])
def run_script(script_name):
    script_path = f"/home/pi/G1-Configs/scripts/{script_name}.sh"
    try:
        result = subprocess.run(
            ["/bin/bash", script_path], capture_output=True, text=True, check=True
        )
        return jsonify({"success": True, "output": result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "error": e.stderr}), 500

@app.route("/tools/<path:subpath>", methods=["GET"])
def get_page(subpath):
    return render_template("index.html", subpath=subpath)

@app.route("/tools/")
def get_index():
    return render_template("index.html", subpath="")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)