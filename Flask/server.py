from flask import Flask, jsonify, render_template, request
import subprocess
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

printerCfgPath = "C:/Users/guare/source/gingerRepos/G1-Configs/Configs/printer.cfg"
folder_path = "./static/printerCfg_Parts"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/backend/read-printer-cfg", methods=["GET"])
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
    
@app.route("/backend/write-printer-cfg", methods=["POST"])
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
                            line = line.replace("{{" + key + "}}", str(values[key]))
                        except:
                            return jsonify({"success": False})
                            
                    outfile.write(line)
                outfile.write("\n\n") 

    return jsonify({"success": True})

@app.route("/run/<script_name>", methods=["POST"])
def run_script(script_name):
    script_path = f"/home/pi/G1-Configs/scripts/{script_name}.sh"
    try:
        result = subprocess.run(
            ["/bin/bash", script_path], capture_output=True, text=True, check=True
        )
        return jsonify({"success": True, "output": result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "error": e.stderr}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)