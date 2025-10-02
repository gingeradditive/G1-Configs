from flask import Flask, render_template_string, request, redirect, url_for
from urllib.parse import urlparse

from utils.mainsail_menu import UpdateMainsailMenu

import scripts.init_script as init_script
import scripts.update_script as update_script
import scripts.sethostname_script as sethostname_script
import scripts.checkforupdate_script as checkforupdate_script
import scripts.factoryreset_script as factoryreset_script

app = Flask(__name__)
menu = UpdateMainsailMenu()

def get_base_url():
    parsed = urlparse(request.host_url)
    # Ricostruisce schema + dominio (senza porta e path)
    return f"{parsed.scheme}://{parsed.hostname}"

# ---------- INIT ----------
@app.route("/init", methods=["GET", "POST"])
def init():
    if request.method == "POST":
        serial = request.form["serial"]
        timezone = request.form["timezone"]

        init_script.run(serial, timezone)
        menu.setTo("Init eseguito")

        return redirect(get_base_url())

    form_html = """
    <form method="post">
        Serial Number: <input type="text" name="serial"><br>
        Timezone: <input type="text" name="timezone" placeholder="Australia/Sydney"><br>
        <button type="submit">Invia</button>
    </form>
    """
    return render_template_string(form_html)



# ---------- UPDATE ----------
@app.route("/update")
def update():
    update_script.run()
    menu.setTo("Update eseguito")
    return redirect(get_base_url())


# ---------- SET HOSTNAME ----------
@app.route("/sethostname", methods=["GET", "POST"])
def sethostname():
    if request.method == "POST":
        hostname = request.form["hostname"]
        sethostname_script.run(hostname)
        menu.setTo("SetHostname eseguito")
        return redirect(get_base_url())

    form_html = """
    <form method="post">
        Hostname: <input type="text" name="hostname" placeholder="g1os.local"><br>
        <button type="submit">Invia</button>
    </form>
    """
    return render_template_string(form_html)


# ---------- CHECK FOR UPDATE ----------
@app.route("/checkforupdate")
def checkforupdate():
    checkforupdate_script.run()
    menu.setTo("CheckForUpdate eseguito")
    return redirect(get_base_url())


# ---------- FACTORY RESET ----------
@app.route("/factoryreset")
def factoryreset():
    factoryreset_script.run()
    menu.setTo("FactoryReset eseguito")
    return redirect(get_base_url())


if __name__ == "__main__":
    app.run(debug=True)
