$.ajax({
    url: '/tools/backend/read-printer-cfg',
    method: 'GET',
    dataType: 'json',
    success: function(response) {
        $('#configuratorForm input').each(function() {
            const inputName = $(this).attr('name'); // ID dell'input, es. "heater_bed/max_power"
            if (inputName) {
                // Suddividi l'ID su base "/" per accedere ai dati nel JSON
                const keys = inputName.split('/'); // ["heater_bed", "max_power"]
                
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
                    console.log(`Valorizzato ${inputName} con: ${value}`);
                } else {
                    console.warn(`Nessun valore trovato per: ${inputName}`);
                }

                // compila campi "speciali"
                if (inputName === 'safe_z_home/home_xy_position') {
                    const x =  $(this).val().split(', ')[0];
                    const y =  $(this).val().split(', ')[1];
                    $('#safe_z_home_x_position').val(x);
                    $('#safe_z_home_y_position').val(y);
                }else if(inputName === 'bed_mesh/probe_count'){
                    const x =  $(this).val().split(', ')[0];
                    const y =  $(this).val().split(', ')[1];
                    $('#bed_mesh_probe_x_points').val(x);
                    $('#bed_mesh_probe_y_points').val(y);
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
        url: '/tools/backend/update-mainboard-serial',
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
        url: '/tools/backend/update-extruder-board-serial',
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

$('#safe_z_home_x_position, #safe_z_home_y_position').change(function() {
    const x = $('#safe_z_home_x_position').val();
    const y = $('#safe_z_home_y_position').val();
    $('#safe_z_home_xy_position').val(`${x}, ${y}`);
});

$('#bed_mesh_probe_x_points, #bed_mesh_probe_y_points').change(function() {
    const x = $('#bed_mesh_probe_x_points').val();
    const y = $('#bed_mesh_probe_y_points').val();
    $('#bed_mesh_probe_xy_points').val(`${x}, ${y}`);
});

$('#probe_x_offset, #probe_y_offset').change(function() {
    const x = $('#probe_x_offset').val();
    const y = $('#probe_y_offset').val();
    $('#probe_xy_offset').val(`${x}, ${y}`);
});