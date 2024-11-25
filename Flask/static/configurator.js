$.ajax({
<<<<<<< HEAD
    url: '/tools/backend/read-printer-cfg',
    method: 'GET',
    dataType: 'json',
    success: function (response) {
        $('#configuratorForm input, #configuratorForm textarea').each(function () {
            const inputName = $(this).attr('name'); // ID dell'input, es. "heater_bed/max_power"
            if (inputName) {
                // Suddividi l'ID su base "/" per accedere ai dati nel JSON
                const keys = inputName.split('/'); // ["heater_bed", "max_power"]

=======
    url: './backend/read-printer-cfg',
    method: 'GET',
    dataType: 'json',
    success: function(response) {
        $('#configuratorForm input').each(function() {
            const id = $(this).attr('name'); // ID dell'input, es. "heater_bed/max_power"
            if (id) {
                // Suddividi l'ID su base "/" per accedere ai dati nel JSON
                const keys = id.split('/'); // ["heater_bed", "max_power"]
                
>>>>>>> 46e2179 (refactor of cfg files and start configurator implementation)
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
<<<<<<< HEAD
                    console.log(`Valorizzato ${inputName} con: ${value}`);
                } else {
                    console.warn(`Nessun valore trovato per: ${inputName}`);
                }

                // compila campi "speciali"
                if (inputName === 'safe_z_home/home_xy_position') {
                    const x = $(this).val().split(', ')[0];
                    const y = $(this).val().split(', ')[1];
                    $('#safe_z_home_x_position').val(x);
                    $('#safe_z_home_y_position').val(y);
                } else if (inputName === 'bed_mesh/probe_count') {
                    const x = $(this).val().split(', ')[0];
                    const y = $(this).val().split(', ')[1];
                    $('#bed_mesh_probe_x_points').val(x);
                    $('#bed_mesh_probe_y_points').val(y);
                }

                // check if response has "tmc2209 extruder_stepper mixing_stepper" key
                if(inputName === 'extruder_stepper_model') {
                    if(response["tmc2209 extruder_stepper mixing_stepper"])
                        $('#extruder_stepper_model_select').val('tmc2209').trigger('change');
                    else if(response["tmc5160 extruder_stepper mixing_stepper"])
                        $('#extruder_stepper_model_select').val('tmc5160').trigger('change');
                }   
            }
        });
    },
    error: function (xhr, status, error) {
        console.log("Loading default value");
        //set every input to placeholder value
        $('#configuratorForm input, #configuratorForm textarea').each(function () {
            $(this).val($(this).attr('placeholder')).trigger('change');
        });

        // trigger change event of selects to set default value
        $('#extruder_stepper_model_select').trigger('change');

        // triggger updates buttons 
        $('#updateMainboardSerial').trigger('click');
        $('#updateExtruderBoardSerial').trigger('click');

        // alert that default value has been loaded
        alert("Configuration file not found, loaded default values");
    }
});


$("#updateMainboardSerial").click(function () {
    $.ajax({
        url: '/tools/backend/update-mainboard-serial',
        method: 'GET',
        success: function (response) {
            if (response.success) {
                $('#mainboardSerial').val(response.serial);
                console.log("Serial mainboard aggiornato");
            }
        },
        error: function (xhr, status, error) {
            console.error("Errore nella richiesta AJAX:", error);
        }
    });
});

$("#updateExtruderBoardSerial").click(function () {
    $.ajax({
        url: '/tools/backend/update-extruder-board-serial',
        method: 'GET',
        success: function (response) {
            if (response.success) {
                $('#extruderBoardSerial').val(response.serial);
                console.log("Serial extruder board aggiornato");
            }
        },
        error: function (xhr, status, error) {
            console.error("Errore nella richiesta AJAX:", error);
        }
    });
});

$('#safe_z_home_x_position, #safe_z_home_y_position').change(function () {
    const x = $('#safe_z_home_x_position').val();
    const y = $('#safe_z_home_y_position').val();
    $('#safe_z_home_xy_position').val(`${x}, ${y}`);
});

$('#bed_mesh_probe_x_points, #bed_mesh_probe_y_points').change(function () {
    const x = $('#bed_mesh_probe_x_points').val();
    const y = $('#bed_mesh_probe_y_points').val();
    $('#bed_mesh_probe_xy_points').val(`${x}, ${y}`);
});

$('#probe_x_offset, #probe_y_offset').change(function () {
    const x = $('#probe_x_offset').val();
    const y = $('#probe_y_offset').val();
    $('#probe_xy_offset').val(`${x}, ${y}`);
});

// extruder_stepper_model_select
// extruder_stepper_model_value

$('#extruder_stepper_model_select').change(function () {
    const model = $('#extruder_stepper_model_select').val();
    const tmc5160 = `[tmc5160 extruder_stepper mixing_stepper]
cs_pin: PE4
spi_software_miso_pin: PA6
spi_software_mosi_pin: PA7
spi_software_sclk_pin: PA5
run_current: 1.5
sense_resistor: 0.022
#stealthchop_threshold: 999999
interpolate: False`;
    const tmc2209 = `[tmc2209 extruder_stepper mixing_stepper]
uart_pin: PE4
run_current: 0.7
#stealthchop_threshold: 999999
interpolate: False`;
    let value = "";
    if (model === 'tmc5160') {
        value = tmc5160;
    } else if (model === 'tmc2209') {
        value = tmc2209;
    }

    $('#extruder_stepper_model_value').val(value);
});
=======
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
>>>>>>> 46e2179 (refactor of cfg files and start configurator implementation)
