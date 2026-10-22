from flask import Flask, render_template_string, request, redirect, render_template, url_for
from werkzeug.middleware.proxy_fix import ProxyFix

import threading
import time
from markupsafe import Markup
import socket
import json
import os

from utils.mainsail_menu import UpdateMainsailMenu
import scripts.init_script as init_script
import scripts.update_script as update_script
import scripts.sethostname_script as sethostname_script
import scripts.checkforupdate_script as checkforupdate_script
import scripts.factoryreset_script as factoryreset_script
import scripts.info_script as info_script


app = Flask(__name__)
# dietro nginx di G1OS l'app è su /g1/ (X-Forwarded-Prefix): url_for e
# request.script_root tengono conto del prefisso
app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1)

menu = UpdateMainsailMenu()

# sito nginx di G1OS: le immagini nuove inoltrano /g1/ alla porta 5000
NGINX_SITE = "/etc/nginx/sites-enabled/mainsail"


def get_machine_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"


# base dei link del menu Mainsail: /g1 (relativo all'host della pagina) se
# nginx ha la location /g1/, altrimenti IP e porta 5000 come sulle G1 con
# immagini precedenti
def get_menu_base_url():
    try:
        with open(NGINX_SITE) as f:
            if "location /g1/" in f.read():
                return "/g1"
    except OSError:
        pass
    return f"http://{get_machine_ip()}:5000"


# funzione helper per il redirect: Mainsail sullo stesso host usato dal
# browser (anche quando si entra direttamente dalla porta 5000)
def get_base_url():
    host = request.host
    if host.endswith(":5000"):
        host = host[:-len(":5000")]
    return f"http://{host}"


#  --------- DOCUMENTATION ----------
@app.route("/docs")
def docs():
    endpoints = [
        ("/init", "Inizializza stampante"),
        ("/update", "Aggiorna stampante"),
        ("/checkforupdate", "Controlla aggiornamenti"),
        ("/sethostname", "[WIP] Imposta hostname (GET/POST)"),
        ("/factoryreset", "Ripristino fabbrica"),
        ("/testicon", "Test icone menu (GET/POST)"),
        ("/info", "Mostra informazioni sistema e seriale")
    ]

    html = ["<h1>G1 Config - API Endpoints</h1><ul>"]
    for path, desc in endpoints:
        html.append(f'<li><a href="{request.script_root}{path}">{path}</a> - {desc}</li>')
    html.append("</ul>")

    return Markup("\n".join(html))

# ---------- INIT ----------


@app.route("/init", methods=["GET", "POST"])
def init():
    if request.method == "POST":
        serial = request.form["serial"]
        timezone = request.form["timezone"]
        init_script.run(serial, timezone)
        run_check_update(get_menu_base_url())
        return redirect(get_base_url())

    # Check if printer is already initialized by reading G1.Conf directly
    warning_message = None
    try:
        if os.name == "nt":
            basePath = os.getcwd()
            databasePath = os.path.normpath(os.path.join(basePath, "..", "out", "database"))
        else:
            databasePath = os.path.normpath(os.path.join("/home", "pi", "printer_data", "database"))

        g1_conf_path = os.path.join(databasePath, "G1.Conf")
        if os.path.exists(g1_conf_path):
            with open(g1_conf_path, "r") as f:
                g1_conf = json.load(f)
            serial_number = g1_conf.get("serial_number", "")
            if serial_number:
                warning_message = f"Printer is already initialized with serial number: {serial_number}"
    except Exception as e:
        print(f"[Init] Error checking printer status: {e}")

    with open("static/data/timezones.json") as f:
        timezones = json.load(f)

    return render_template("init.html", timezones=timezones, warning_message=warning_message)


# ---------- CHECK FOR UPDATE ----------
def run_check_update(url):
    update_status = checkforupdate_script.run()
    if (update_status == "update available"):
        menu.set_to_update_available(url)
    else:
        menu.set_to_system_ok(url)


# ---------- UPDATE ----------
@app.route("/update")
def update():
    update_result = update_script.run()
    if update_result is True:
        menu.set_to_system_ok(get_menu_base_url())
        return redirect(get_base_url())
    elif update_result == "redirect":
        menu.set_to_system_ok(get_menu_base_url())
        return redirect(f"{get_base_url()}/config")
    else:
        menu.set_to_update_available(get_menu_base_url())
        return redirect(get_base_url())


def periodic_check():
    # il primo controllo lo fa già l'avvio (__main__): attende prima di ripeterlo
    while True:
        # time.sleep(10)  # ogni 10 secondi
        time.sleep(3600)  # <-- in produzione, ogni 1 ora
        run_check_update(get_menu_base_url())


@app.route("/checkforupdate")
def checkforupdate():
    run_check_update(get_menu_base_url())
    return redirect(get_base_url())


# ---------- SET HOSTNAME ----------
@app.route("/sethostname", methods=["GET", "POST"])
def sethostname():
    if request.method == "POST":
        hostname = request.form["hostname"]
        sethostname_script.run(hostname)
        menu.set_to_system_ok(get_menu_base_url())
        return redirect(get_base_url())

    form_html = """
    <form method="post">
        Hostname: <input type="text" name="hostname" placeholder="192.168.1.100"><br>
        <button type="submit">Invia</button>
    </form>
    """
    return render_template_string(form_html)


# ---------- FACTORY RESET ----------
@app.route("/factoryreset")
def factoryreset():
    reset_complete = factoryreset_script.run()

    if reset_complete:
        run_check_update(get_menu_base_url())

    return redirect(get_base_url())

# ---------- INFO ----------
@app.route("/info")
def info():
    try:
        system_info = info_script.run()
        return json.dumps(system_info, indent=2)
    except Exception as e:
        error_info = {
            "error": str(e),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "message": "Failed to gather system information"
        }
        return json.dumps(error_info, indent=2), 500


# ---------- TEST ICON ----------


@app.route("/testicon", methods=["GET", "POST"])
def testicon():
    if request.method == "POST":
        selected_action = request.form.get("action")
        base_url = get_base_url()

        if selected_action == "update_available":
            menu.set_to_update_available(get_menu_base_url())
        elif selected_action == "system_ok":
            menu.set_to_system_ok(get_menu_base_url())
        elif selected_action == "factory_reset":
            menu.set_to_system_ok(get_menu_base_url())
        else:
            return render_template_string("<h2>Errore: azione sconosciuta</h2>")

        return redirect(base_url)

    form_html = """
    <h1>Test Icon Menu</h1>
    <form method="post">
        <label for="action">Seleziona stato menu:</label><br><br>
        <select name="action" id="action">
            <option value="update_available">Aggiornamento disponibile</option>
            <option value="system_ok">Sistema OK</option>
            <option value="factory_reset">Dopo reset di fabbrica</option>
        </select><br><br>
        <button type="submit">Applica</button>
    </form>
    """
    return render_template_string(form_html)



def is_internet_available(host="8.8.8.8", port=53, timeout=3):
    """
    Controlla la connessione tentando di aprire una socket verso un DNS pubblico (Google DNS).
    È più affidabile del ping.
    """
    try:
        # timeout solo per questa socket: setdefaulttimeout varrebbe per tutte
        # le connessioni del processo (anche quelle verso GitHub)
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False

if __name__ == "__main__":
    print("Controllo disponibilità rete...")
    timeout_limit = 120  # secondi
    retry_interval = 5   # secondi
    # ripeti finché non c'è connessione
    while not is_internet_available():        
        if retry_interval > timeout_limit:
            retry_interval = timeout_limit
        else:
            retry_interval += 5
        print(f"Nessuna connessione. Riprovo tra {retry_interval} secondi...")
        time.sleep(retry_interval)

    print("Connessione rilevata! Procedo con l'avvio...")

    # ora puoi lanciare il resto del tuo codice
    print("Avvio controllo iniziale...")
    run_check_update(get_menu_base_url())

    print("Avvio thread periodic_check...")
    threading.Thread(target=periodic_check, daemon=True).start()

    if os.name == "nt":
        app.run(debug=True)
    else:
        app.run(host="0.0.0.0", port=5000)