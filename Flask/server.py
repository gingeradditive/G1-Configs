from flask import Flask, render_template_string, request, redirect, render_template, url_for

import threading
import time
from markupsafe import Markup
import socket
import platform
import json
import os

from utils.mainsail_menu import UpdateMainsailMenu
import scripts.init_script as init_script
import scripts.update_script as update_script
import scripts.sethostname_script as sethostname_script
import scripts.checkforupdate_script as checkforupdate_script
import scripts.factoryreset_script as factoryreset_script


app = Flask(__name__)

menu = UpdateMainsailMenu()


# funzione helper per il redirect
def get_base_url():
    system_name = platform.system()

    if system_name == "Windows":
        return "http://127.0.0.1"
    else:  # Linux (quindi anche Raspberry)
        hostname = socket.gethostname()

        if not hostname.endswith(".local"):
            hostname += ".local"

        return f"http://{hostname}"


#  --------- DOCUMENTATION ----------
@app.route("/docs")
def docs():
    endpoints = [
        ("/init", "Inizializza stampante"),
        ("/update", "Aggiorna stampante"),
        ("/checkforupdate", "Controlla aggiornamenti"),
        ("/sethostname", "[WIP] Imposta hostname (GET/POST)"),
        ("/factoryreset", "Ripristino fabbrica"),
        ("/testicon", "Test icone menu (GET/POST)")
    ]

    html = ["<h1>G1 Config - API Endpoints</h1><ul>"]
    for path, desc in endpoints:
        html.append(f'<li><a href="{path}">{path}</a> - {desc}</li>')
    html.append("</ul>")

    return Markup("\n".join(html))

# ---------- INIT ----------
@app.route("/init", methods=["GET", "POST"])
def init():
    if request.method == "POST":
        serial = request.form["serial"]
        timezone = request.form["timezone"]
        init_script.run(serial, timezone)
        run_check_update(get_base_url())
        return redirect(get_base_url())

    with open("static/data/timezones.json") as f:
        timezones = json.load(f)

    return render_template("init.html", timezones=timezones)


# ---------- CHECK FOR UPDATE ----------
def run_check_update(url):
    update_status = checkforupdate_script.run()
    if (update_status == "update available"):
        menu.set_to_update_available(url)
    elif (update_status == "system not initialized"):
        menu.set_to_initialize_printer(url)
    else:
        menu.set_to_system_ok(url)


# ---------- UPDATE ----------
@app.route("/update")
def update():
    update_complete = update_script.run()
    if (update_complete):
        menu.set_to_system_ok(get_base_url())
    else:
        menu.set_to_update_available(get_base_url())
    return redirect(get_base_url())


def periodic_check():
    while True:
        run_check_update(get_base_url())
        # time.sleep(10)  # ogni 10 secondi
        time.sleep(3600)  # <-- in produzione, ogni 1 ora


@app.route("/checkforupdate")
def checkforupdate():
    run_check_update(get_base_url())
    return redirect(get_base_url())


# ---------- SET HOSTNAME ----------
@app.route("/sethostname", methods=["GET", "POST"])
def sethostname():
    if request.method == "POST":
        hostname = request.form["hostname"]
        sethostname_script.run(hostname)
        menu.set_to_system_ok(get_base_url())
        return redirect(get_base_url())

    form_html = """
    <form method="post">
        Hostname: <input type="text" name="hostname" placeholder="g1os.local"><br>
        <button type="submit">Invia</button>
    </form>
    """
    return render_template_string(form_html)


# ---------- FACTORY RESET ----------
@app.route("/factoryreset")
def factoryreset():
    reset_complete = factoryreset_script.run()
    
    if reset_complete: 
        run_check_update(get_base_url())

    return redirect(get_base_url())

# ---------- TEST ICON ----------
@app.route("/testicon", methods=["GET", "POST"])
def testicon():
    if request.method == "POST":
        selected_action = request.form.get("action")
        base_url = get_base_url()

        if selected_action == "update_available":
            menu.set_to_update_available(base_url)
        elif selected_action == "initialize_printer":
            menu.set_to_initialize_printer(base_url)
        elif selected_action == "system_ok":
            menu.set_to_system_ok(base_url)
        elif selected_action == "factory_reset":
            menu.set_to_system_ok(base_url)
        else:
            return render_template_string("<h2>Errore: azione sconosciuta</h2>")

        return redirect(base_url)

    form_html = """
    <h1>Test Icon Menu</h1>
    <form method="post">
        <label for="action">Seleziona stato menu:</label><br><br>
        <select name="action" id="action">
            <option value="update_available">Aggiornamento disponibile</option>
            <option value="initialize_printer">Inizializza stampante</option>
            <option value="system_ok">Sistema OK</option>
            <option value="factory_reset">Dopo reset di fabbrica</option>
        </select><br><br>
        <button type="submit">Applica</button>
    </form>
    """
    return render_template_string(form_html)


if __name__ == "__main__":
    # Avvia il check subito all’avvio
    print("🟢 Avvio controllo iniziale...")
    run_check_update(get_base_url())

    # Avvia thread periodico
    print("🟢 Avvio thread periodic_check...")
    threading.Thread(target=periodic_check, daemon=True).start()

    if os.name == "nt":
        app.run(debug=True)
    else:
        app.run(host="0.0.0.0", port=5000)
