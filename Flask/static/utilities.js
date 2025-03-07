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
});