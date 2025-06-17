function loadConfigurations(data) {
    $('#configuratorForm input, #configuratorForm textarea, #configuratorForm select').each(function () {
        try {
            const inputName = $(this).attr('name'); // ID dell'input, es. "heater_bed/max_power"
            if (inputName) {
                // Suddividi l'ID su base "/" per accedere ai dati nel JSON
                const keys = inputName.split('/'); // ["heater_bed", "max_power"]


                // Verifica e aggiornamento del valore "run_current" per "mixing_stepper"
                const keysToCheck = [
                    "tmc5160 extruder_stepper mixing_stepper",
                    "tmc2209 extruder_stepper mixing_stepper"
                ];
                if (!data["mixing_stepper"])
                    data["mixing_stepper"] = {};
                for (const key of keysToCheck) {
                    if (data[key]?.run_current) {
                        data["mixing_stepper"]["run_current"] = data[key].run_current;
                        break; // Esci dal ciclo una volta trovato il primo valore valido
                    }
                }

                if (data["stepper_x"] == undefined)
                    data["stepper_x"] = {};
                if (data["stepper_y"] == undefined)
                    data["stepper_y"] = {};
                if (data["stepper_z"] == undefined)
                    data["stepper_z"] = {};

                data["stepper_x"]["run_current"] = data["tmc5160 stepper_x"]["run_current"];
                data["stepper_y"]["run_current"] = data["tmc5160 stepper_y"]["run_current"];
                data["stepper_z"]["run_current"] = data["tmc5160 stepper_z"]["run_current"];


                // Usa i keys per navigare nel JSON
                let value = data;
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
                    const x = $(this).val().split(', ')[0];
                    const y = $(this).val().split(', ')[1];
                    $('#safe_z_home_x_position').val(x);
                    $('#safe_z_home_y_position').val(y);
                } else if (inputName === 'bed_mesh/probe_count') {
                    const x = $(this).val().split(', ')[0];
                    const y = $(this).val().split(', ')[1];
                    $('#bed_mesh_probe_x_points').val(x);
                    $('#bed_mesh_probe_y_points').val(y);
                } else if (inputName === 'bed_mesh/mesh_max') {
                    const x = $(this).val().split(', ')[0];
                    const y = $(this).val().split(', ')[1];
                    $('#bed_max_x').val(x);
                    $('#bed_max_y').val(y);
                }

                if (inputName === 'heater_bed/max_power') {
                    $('#heater_bed_max_power_percentage').val(value * 100);
                }

                // check if data has "tmc2209 extruder_stepper mixing_stepper" key
                if (inputName === 'extruder_stepper_model_select') {
                    if (data["tmc2209 extruder_stepper mixing_stepper"])
                        $('#extruder_stepper_model_select').val('tmc2209');
                    else if (data["tmc5160 extruder_stepper mixing_stepper"])
                        $('#extruder_stepper_model_select').val('tmc5160');
                }

                // Select prevous motor direction 
                if (inputName == "stepper_x/invert_rotation")
                    $("[name='stepper_x/invert_rotation']").prop('checked', data["stepper_x"]["dir_pin"].includes("!"));
                if (inputName == "stepper_y/invert_rotation")
                    $("[name='stepper_y/invert_rotation']").prop('checked', data["stepper_y"]["dir_pin"].includes("!"));
                if (inputName == "stepper_z/invert_rotation")
                    $("[name='stepper_z/invert_rotation']").prop('checked', data["stepper_z"]["dir_pin"].includes("!"));
                if (inputName == "extruder/invert_rotation")
                    $("[name='extruder/invert_rotation']").prop('checked', data["extruder"]["dir_pin"].includes("!"));
            }
        } catch (error) {
            console.error(`Errore durante il caricamento del valore per ${$(this).attr('name')}:`, error);
        }
    });
}

$.ajax({
    url: '/tools/backend/read-printer-cfg',
    method: 'GET',
    dataType: 'json',
    success: function (data) {
        loadConfigurations(data);
    },
    error: function (xhr, status, error) {
        // Show the first modal
        $('#configErrorModal').modal('show');
    }
});

// Handle "Start Clean" button
$('#startCleanBtn').off('click').on('click', function () {
    $('#configErrorModal').modal('hide');

    // Set every input to placeholder value
    $('#configuratorForm input, #configuratorForm textarea').each(function () {
        placeholderVal = $(this).attr('placeholder')
        if (typeof placeholderVal !== 'undefined' && placeholderVal !== false) {
            $(this).val($(this).attr('placeholder'));
            $(this).trigger('change');
            console.log("name: " + $(this).attr("name") + " | id: " + $(this).attr("id"))
        }
    });

    // Trigger updates
    $('#updateMainboardSerial').trigger('click');
    $('#updateExtruderBoardSerial').trigger('click');
});

// Handle "Download Default" button
$('#downloadDefaultBtn').off('click').on('click', function () {
    $('#configErrorModal').modal('hide');
    $('#serialNumberModal').modal('show');
});

// Handle "Confirm Download" button
$('#confirmSerialNumberDownload').off('click').on('click', function () {
    let serialNumber = $('#serialNumberInput').val().trim();
    const $serialNumberError = $('#serialNumberError');

    // Reset error state
    $serialNumberError.addClass('d-none').text('');
    const regex = /^G1-\d{4}-\d{2}$/;
    const number = Number(serialNumber);
    if (!serialNumber || (!regex.test(serialNumber) && (isNaN(number) || number < 10 || number > 25))
    ) {
        $serialNumberError.removeClass('d-none').text("Please enter a valid SerialNumber.");
        return;
    }

    if (number >= 10 && number <= 25) {
        // transform serial number to G1-XXXX-XX format
        const paddedNumber = String(number).padStart(4, '0');
        serialNumber = `G1-${paddedNumber}-20`;
    }

    // Disable button during request
    $('#confirmSerialNumberDownload').prop('disabled', true).text('Downloading...');

    // AJAX request
    $.ajax({
        url: `https://www.gingeradditive.com/wp-json/g1/v1/RestoreG1Config?serialNumber=${encodeURIComponent(serialNumber)}`,
        method: 'GET',
        success: function (data) {
            // TODO: handle config restore using returned `data`
            $('#serialNumberModal').modal('hide');
            loadConfigurations(data);
            // Trigger updates
            $('#updateMainboardSerial').trigger('click');
            $('#updateExtruderBoardSerial').trigger('click');
        },
        error: function (xhr, status, error) {
            // Show error inside the modal
            $serialNumberError.removeClass('d-none').text("Download failed. Please check the SerialNumber number and try again.");
        },
        complete: function () {
            $('#confirmSerialNumberDownload').prop('disabled', false).text('Download Configuration');
        }
    });
});

$("#ExportButton").click(function () {
    $.ajax({
        url: '/tools/backend/read-printer-cfg',
        method: 'GET',
        dataType: 'json',
        success: function (data) {
            // Funzione per scaricare il JSON come file
            // Converte i dati JSON in una stringa
            const jsonString = JSON.stringify(data, null, 2);

            // Crea un Blob con il tipo MIME 'application/json'
            const blob = new Blob([jsonString], { type: 'application/json' });

            // Crea un URL per il Blob
            const url = URL.createObjectURL(blob);

            // Crea un elemento di ancoraggio <a> per il download
            const a = document.createElement('a');
            a.href = url;
            a.download = 'config.json'; // Nome del file da scaricare
            a.click(); // Simula il clic per avviare il download

            // Libera l'URL dopo il download
            URL.revokeObjectURL(url);
        },
        error: function (xhr, status, error) {
            // Show the first modal
            $('#configErrorModal').modal('show');
        }
    });
});


$("#updateMainboardSerial").click(function () {
    $.ajax({
        url: '/tools/backend/update-mainboard-serial',
        method: 'GET',
        success: function (data) {
            if (data.success) {
                $('#mainboardSerial').val(data.serial);
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
        success: function (data) {
            if (data.success) {
                $('#extruderBoardSerial').val(data.serial);
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

$('#bed_max_x, #bed_max_y').change(function () {
    const x = $('#bed_max_x').val();
    const y = $('#bed_max_y').val();
    $('#bed_max_xy').val(`${x}, ${y}`);
});

$('#probe_x_offset, #probe_y_offset').change(function () {
    const x = $('#probe_x_offset').val();
    const y = $('#probe_y_offset').val();
    $('#probe_xy_offset').val(`${x}, ${y}`);
});

$("#heater_bed_max_power_percentage").change(function () {
    const max_power_percentage = $('#heater_bed_max_power_percentage').val();
    $('#heater_bed_max_power').val(max_power_percentage / 100);
});

$("#heater_bed_max_power").change(function () {
    const max_power = $('#heater_bed_max_power').val();
    $('#heater_bed_max_power_percentage').val(max_power * 100);
});

$(document).ready(function () {
    $('.collapse').on('shown.bs.collapse', function () {
        $('.btn-configurator').removeClass('active-button');

        var collapseId = $(this).attr('id');
        $('[data-bs-target="#' + collapseId + '"]').addClass('active-button');
    });

    $('.collapse').on('hidden.bs.collapse', function () {
        var collapseId = $(this).attr('id');
        $('[data-bs-target="#' + collapseId + '"]').removeClass('active-button');
    });
});

$('#jsonFileInput').on('change', function () {
    var file = this.files[0];
    var $status = $('#importStatus');
    var $confirmBtn = $('#confirmImportBtn');

    $status.text('');
    importedJsonData = null;
    $confirmBtn.prop('disabled', true);

    if (!file) return;

    if (file.type !== 'application/json') {
        $status.text('Please select a valid JSON file.');
        return;
    }

    var reader = new FileReader();

    reader.onload = function (e) {
        try {
            importedJsonData = JSON.parse(e.target.result);
            $status.text('File loaded successfully. Click "Confirm Import" to proceed.');
            $confirmBtn.prop('disabled', false);
        } catch (err) {
            $status.text('Error reading JSON file: ' + err.message);
        }
    };

    reader.onerror = function () {
        $status.text('Failed to read the file.');
    };

    reader.readAsText(file);
});

let importedJsonData = null;
$('#confirmImportBtn').on('click', function () {
    if (importedJsonData) {
        $('#ImportModal').modal('hide');
        setTimeout(function () {
            loadConfigurations(importedJsonData); // Call your function here
        }, 500); // Delay to allow modal to close smoothly
    }
});