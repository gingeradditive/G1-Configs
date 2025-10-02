function appenNotification(message, level) {
    $(".NotificationsContainer").append('<div class="alert alert-' + level + ' alert-dismissible fade show" role="alert">' + message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
    $("#NoNotification").remove()
}

$(document).ready(function () {

    const form = $("form[action='/tools/backend/change-hostname']");
    const input = $("#printerName");
    const errorMsg = $("#hostname-ErrorMessage")

    form.on("submit", function (event) {
        const hostname = input.val().trim();
        const hostnameRegex = /^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$/;

        if (!hostnameRegex.test(hostname)) {
            event.preventDefault(); // Blocca il submit
            errorMsg.text("Invalid printer name. Use only letters, numbers, and hyphens, and do not start or end with a hyphen.");
            errorMsg.removeClass("d-none");
        } else {
            errorMsg.text(""); // Rimuove il messaggio di errore se valido
            errorMsg.addClass("d-none");
        }
    });

    $.ajax({
        url: '/tools/backend/read-printer-hostname',
        method: 'GET',
        dataType: 'json',
        success: function (response) {
            input.val(response.hostname)
        }
    });

    $.ajax({
        url: '/tools/backend/check-files',
        method: 'GET',
        dataType: 'json',
        success: function (response) {
            if (response["KlipperScreen.conf"] == null) {
                appenNotification("<strong>⛔ KlipperScreen.conf file not found</strong> this may cause G1 to malfunction, please restore the file", "danger");
            }
            else if (response["KlipperScreen.conf"] == false) {
                appenNotification("<strong>⚠️ KlipperScreen.conf file has been modified or needs to be updated</strong>, please restore it", "warning");
            }

            if (response["kamp.cfg"] == null) {
                appenNotification("<strong>⛔ kamp.cfg file not found</strong> this may cause G1 to malfunction, please restore the file", "danger");
            }
            else if (response["kamp.cfg"] == false) {
                appenNotification("<strong>⚠️ kamp.cfg file has been modified or needs to be updated</strong>, please restore it", "warning");
            }

            if (response["moonraker.conf"] == null) {
                appenNotification("<strong>⛔ moonraker.conf file not found</strong> this may cause G1 to malfunction, please restore the file", "danger");
            }
            else if (response["moonraker.conf"] == false) {
                appenNotification("<strong>⚠️ moonraker.conf file has been modified or needs to be updated</strong>, please restore it", "warning");
            }

            if (response["splash.png"] == null || response["theme/custom.css"] == null) {
                appenNotification("<strong>⛔ Error some theme files seem to be missing</strong>, please restore the .theme folder", "danger");
            }
            else if (response["splash.png"] == false || response["theme/custom.css"] == false) {
                appenNotification("<strong>⚠️ Warning some theme files seem to be corrupted</strong>, please restore the .theme folder", "warning");
            }

            if (response["printer.cfg"] == false) {
                appenNotification("<strong>⛔ printer.cfg file not found</strong> this may cause G1 to malfunction, please generate a new file via the Printer Configurator page", "danger");
            }
        },
        error: function (xhr, status, error) {

        }
    });
});