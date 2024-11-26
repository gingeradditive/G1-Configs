$.ajax({
    url: './backend/read-printer-cfg',
    method: 'GET',
    dataType: 'json',
    success: function(response) {
        $('#configuratorForm input').each(function() {
            const id = $(this).attr('name'); // ID dell'input, es. "heater_bed/max_power"
            if (id) {
                // Suddividi l'ID su base "/" per accedere ai dati nel JSON
                const keys = id.split('/'); // ["heater_bed", "max_power"]
                
                // Usa i keys per navigare nel JSON
                let value = response;
                keys.forEach(key => {
                    if (value && value[key] !== undefined) {
                        value = value[key];
                    } else {
                        value = null; // Se una chiave non esiste, assegna null
                    }
                });

                // Imposta il valore dell'input
                if (value !== null) {
                    $(this).val(value);
                    console.log(`Valorizzato ${id} con: ${value}`);
                } else {
                    console.warn(`Nessun valore trovato per: ${id}`);
                }
            }
        });
    },
    error: function(xhr, status, error) {
        console.error("Errore nella richiesta AJAX:", error);
    }
});


$("#updateMainboardSerial").click(function() {
    $.ajax({
        url: './backend/update-mainboard-serial',
        method: 'GET',
        success: function(response) {
            if(response.success){
                $('#mainboardSerial').val(response.serial);
                console.log("Serial mainboard aggiornato");
            }
        },
        error: function(xhr, status, error) {
            console.error("Errore nella richiesta AJAX:", error);
        }
    });
});

$("#updateExtruderBoardSerial").click(function() {
    $.ajax({
        url: './backend/update-extruder-board-serial',
        method: 'GET',
        success: function(response) {
            if(response.success){
                $('#extruderBoardSerial').val(response.serial);
                console.log("Serial extruder board aggiornato");
            }
        },
        error: function(xhr, status, error) {
            console.error("Errore nella richiesta AJAX:", error);
        }
    });
}); 