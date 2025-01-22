from flask import *
import subprocess
import shutil
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

if os.name == "nt":
    configPath = "C:/Users/guare/source/gingerRepos/G1-Configs/out/config"
    backupConfigPath = "C:/Users/guare/source/gingerRepos/G1-Configs/Configs"
else:
    configPath = "/home/pi/printer_data/config"
    backupConfigPath = "/home/pi/G1-Configs/Configs"


@app.route('/tools/static/<path:path>')
def send_report(path):
    # Using request args for path will expose you to directory traversal attacks
    return send_from_directory('static', path)


@app.route("/tools/backend/read-printer-cfg", methods=["GET"])
def read_printer_cfg():
    with open(configPath + "/printer.cfg", "r") as file:
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


@app.route("/tools/backend/write-printer-cfg", methods=["POST"])
def write_printer_cfg():
    values = request.form
    print(values)

    with open(configPath + "/printer.cfg", "w") as outfile:
        # values[key]
        outfile.write(
            '############################ G1 Configuration #############################\n')
        outfile.write('#\n')
        outfile.write(
            '# WARNING: this file is generated by the configuration tool.\n')
        outfile.write('# Any manual changes will be overwritten.\n')
        outfile.write('# \n')
        outfile.write(
            '###########################################################################\n')
        outfile.write('\n')
        outfile.write('[include mainsail.cfg]\n')
        outfile.write('[include kamp.cfg]\n')
        outfile.write('[include G1-Configs/macro.cfg]\n')
        outfile.write('[include G1-Configs/main.cfg]\n')
        outfile.write('# [include G1-Configs/accelerometer.cfg]\n')
        outfile.write('# [include moonraker_obico_macros.cfg]\n')
        outfile.write('\n')
        outfile.write(
            '################################### Bed ###################################\n')
        outfile.write('\n')
        outfile.write('[heater_bed]\n')
        outfile.write('heater_pin: extruder_board: PB3 #D11\n')
        outfile.write('sensor_pin: PF3 #PF3\n')
        outfile.write('sensor_type: EPCOS 100K B57560G104F\n')
        outfile.write('control: pid\n')
        outfile.write('pid_Kp: 75.616\n')
        outfile.write('pid_Ki: 1.110\n')
        outfile.write('pid_Kd: 1287.354\n')
        outfile.write('min_temp: 0\n')
        outfile.write('max_temp: ' + values["heater_bed/max_temp"] + '\n')
        outfile.write('pwm_cycle_time: 0.200\n')
        outfile.write('max_power: ' + values["heater_bed/max_power"] + '\n')
        outfile.write('\n')
        outfile.write('[verify_heater heater_bed]\n')
        outfile.write('max_error: 200 #120\n')
        outfile.write('check_gain_time:100 #20\n')
        outfile.write('hysteresis: 8 #5\n')
        outfile.write('heating_gain: 1 #2\n')
        outfile.write('\n')
        outfile.write(
            '################################### Buzzer #################################\n')
        outfile.write('\n')
        outfile.write('[output_pin BUZZER_PIN]\n')
        outfile.write('pin: extruder_board: PB0 #D2\n')
        outfile.write('\n')
        outfile.write(
            '################################# Cooler #####################################\n')
        outfile.write('\n')
        outfile.write('[fan]\n')
        outfile.write('pin: extruder_board: PD3  #D3\n')
        outfile.write('cycle_time: 0.2\n')
        outfile.write('hardware_pwm: False\n')
        outfile.write('kick_start_time: 0.5\n')
        outfile.write('off_below: 0.2\n')
        outfile.write('\n')
        outfile.write(
            '################################# Etruder #####################################\n')
        outfile.write('\n')
        outfile.write(
            '#-------------------------------------------------------------------------------\n')
        outfile.write('# extruder motor: E0\n')
        outfile.write(
            '#-------------------------------------------------------------------------------\n')
        outfile.write('[firmware_retraction]\n')
        outfile.write('retract_length: 0\n')
        outfile.write('retract_speed: 20\n')
        outfile.write('unretract_extra_length: 0\n')
        outfile.write('unretract_speed: 10\n')
        outfile.write('\n')
        outfile.write(
            '#-------------------------------------------------------------------------------\n')
        outfile.write('# extruder motor: E1\n')
        outfile.write(
            '#-------------------------------------------------------------------------------\n')
        outfile.write('[extruder_stepper mixing_stepper]\n')
        outfile.write('extruder: extruder\n')
        outfile.write('step_pin: PC13\n')
        outfile.write('dir_pin: !PF0\n')
        outfile.write('enable_pin: !PF1 \n')
        outfile.write('microsteps: 8\n')
        outfile.write('rotation_distance: 7600 \n')
        outfile.write('\n')

        if (values["extruder_stepper_model_select"] == "tmc5160"):
            outfile.write('[tmc5160 extruder_stepper mixing_stepper]\n')
            outfile.write('cs_pin: PE4\n')
            outfile.write('spi_software_miso_pin: PA6\n')
            outfile.write('spi_software_mosi_pin: PA7\n')
            outfile.write('spi_software_sclk_pin: PA5\n')
            outfile.write('run_current: ' +
                          values["mixing_stepper/run_current"] + '\n')
            outfile.write('sense_resistor: 0.022\n')
            outfile.write('#stealthchop_threshold: 999999\n')
            outfile.write('interpolate: False\n')
        elif (values["extruder_stepper_model_select"] == "tmc2209"):
            outfile.write('[tmc2209 extruder_stepper mixing_stepper]\n')
            outfile.write('uart_pin: PE4\n')
            outfile.write('run_current: ' +
                          values["mixing_stepper/run_current"] + '\n')
            outfile.write('#stealthchop_threshold: 999999\n')
            outfile.write('interpolate: False\n')

        outfile.write('\n')
        outfile.write(
            '#-------------------------------------------------------------------------------\n')
        outfile.write('# extruder band position: UP\n')
        outfile.write(
            '#-------------------------------------------------------------------------------\n')
        outfile.write('[extruder]\n')
        outfile.write('step_pin: PF9\n')
        outfile.write('dir_pin: PF10\n')
        outfile.write('enable_pin: !PG2 \n')
        outfile.write('microsteps: 8\n')
        outfile.write('rotation_distance: 456\n')
        outfile.write('\n')
        outfile.write('#456 PLA  [mm^3/rotation]\n')
        outfile.write('#624 PETG  [mm^3/rotation]\n')
        outfile.write(
            '#rotation_distance is the volume of material (mm^3) extruded per rotation\n')
        outfile.write('\n')
        outfile.write('full_steps_per_rotation: 200\n')
        outfile.write('gear_ratio: 5:1 \n')
        outfile.write('nozzle_diameter: 1\n')
        outfile.write(
            'filament_diameter: 1.1284 #con questo valore i mm di filamento equivalgono ai mm^3\n')
        outfile.write('max_extrude_cross_section: 150\n')
        outfile.write(
            'step_pulse_duration: 0.00002 #10 volte gli altri driver dovrebbe bastare\n')
        outfile.write('instantaneous_corner_velocity: 30.0\n')
        outfile.write('max_extrude_only_distance: 9999999999\n')
        outfile.write('max_extrude_only_velocity: 300 #da modificare\n')
        outfile.write('max_extrude_only_accel: 1000 #da modificare\n')
        outfile.write(
            '#max_extruder_velocity: 100 #max_volumeric_speed / ((filament_diameter / 2)^2 * PI()) 100 è tipo 250mm3/s\n')
        outfile.write('pressure_advance: 0.0\n')
        outfile.write('pressure_advance_smooth_time: 0.040\n')
        outfile.write('max_power: 1.0\n')
        outfile.write('pullup_resistor: 4700\n')
        outfile.write('smooth_time: 1.0\n')
        outfile.write('heater_pin: extruder_board: PD2 #D2\n')
        outfile.write('sensor_pin:  PF4 #PF4\n')
        outfile.write('sensor_type: EPCOS 100K B57560G104F\n')
        outfile.write('control: pid\n')
        outfile.write('pid_Kp: 38.284\n')
        outfile.write('pid_Ki: 0.472\n')
        outfile.write('pid_Kd: 776.691\n')
        outfile.write('min_temp: 0\n')
        outfile.write('max_temp: ' + values["extruder/max_temp"] + '\n')
        outfile.write('#delta_max: 2.0\n')
        outfile.write('pwm_cycle_time: 0.300\n')
        outfile.write('min_extrude_temp: ' +
                      values["extruder/min_extrude_temp"] + '\n')
        outfile.write('\n')
        outfile.write('[verify_heater extruder]\n')
        outfile.write('max_error: 250 #120\n')
        outfile.write('check_gain_time:150 #20\n')
        outfile.write('hysteresis: 20 #5\n')
        outfile.write('heating_gain: 1 #2\n')
        outfile.write('\n')
        outfile.write(
            '#-------------------------------------------------------------------------------\n')
        outfile.write('# extruder band position: MID\n')
        outfile.write(
            '#-------------------------------------------------------------------------------\n')
        outfile.write('[extruder1]\n')
        outfile.write('nozzle_diameter: 1.750\n')
        outfile.write('filament_diameter: 1.750\n')
        outfile.write('heater_pin: extruder_board: PD4 #D4\n')
        outfile.write('sensor_pin:  PF5 #PF5\n')
        outfile.write('sensor_type: EPCOS 100K B57560G104F\n')
        outfile.write('control: pid\n')
        outfile.write('pid_kp: 34.874\n')
        outfile.write('pid_ki: 0.144\n')
        outfile.write('pid_kd: 2109.429\n')
        outfile.write('min_temp: 0\n')
        outfile.write('max_temp: ' + values["extruder1/max_temp"] + '\n')
        outfile.write('\n')
        outfile.write('[verify_heater extruder1]\n')
        outfile.write('max_error: 250 #120\n')
        outfile.write('check_gain_time:150 #20\n')
        outfile.write('hysteresis: 10 #5\n')
        outfile.write('heating_gain: 1 #2\n')
        outfile.write('\n')
        outfile.write(
            '#-------------------------------------------------------------------------------\n')
        outfile.write('# extruder band position: DOWN\n')
        outfile.write(
            '#-------------------------------------------------------------------------------\n')
        outfile.write('[extruder2]\n')
        outfile.write('nozzle_diameter: 1.750\n')
        outfile.write('filament_diameter: 1.750\n')
        outfile.write('heater_pin: extruder_board: PD7 #D7\n')
        outfile.write('sensor_pin:  PF6 #PF6\n')
        outfile.write('sensor_type: EPCOS 100K B57560G104F\n')
        outfile.write('control: pid\n')
        outfile.write('pid_kp: 34.495\n')
        outfile.write('pid_ki: 0.322\n')
        outfile.write('pid_kd: 924.890\n')
        outfile.write('min_temp: 0\n')
        outfile.write('max_temp: ' + values["extruder2/max_temp"] + '\n')
        outfile.write('\n')
        outfile.write('[verify_heater extruder2]\n')
        outfile.write('max_error: 250 #120\n')
        outfile.write('check_gain_time:150 #20\n')
        outfile.write('hysteresis: 10 #5\n')
        outfile.write('heating_gain: 1 #2\n')
        outfile.write('\n')
        outfile.write(
            '################################# Feeder ###################################\n')
        outfile.write('\n')
        outfile.write('[output_pin FEEDER_STATUS]\n')
        outfile.write('pin: extruder_board: PB1 #D9\n')
        outfile.write('\n')
        outfile.write('[filament_switch_sensor FEEDER]\n')
        outfile.write('switch_pin: ^extruder_board: PC4 #A4\n')
        outfile.write('pause_on_runout: False\n')
        outfile.write('\n')
        outfile.write(
            '# delayed Gcode for checking the status of the feeder sensor every 1 second \n')
        outfile.write('# and updating the status pin\n')
        outfile.write('[delayed_gcode FEEDER_CHECK_STATUS]\n')
        outfile.write('initial_duration: 0.5\n')
        outfile.write('gcode:\n')
        outfile.write(
            '  {% if printer["filament_switch_sensor FEEDER"].enabled %}\n')
        outfile.write('    SET_PIN PIN=FEEDER_STATUS VALUE=1\n')
        outfile.write('  {% else %}\n')
        outfile.write('    SET_PIN PIN=FEEDER_STATUS VALUE=0\n')
        outfile.write('  {% endif %}\n')
        outfile.write(
            '  UPDATE_DELAYED_GCODE ID=FEEDER_CHECK_STATUS DURATION=1.0\n')
        outfile.write('\n')
        outfile.write(
            '# delayed Gcode for deactivate the feeder sensor on startup\n')
        outfile.write('[delayed_gcode FEEDER_STARTUP_STATUS]\n')
        outfile.write('initial_duration: 0.1\n')
        outfile.write('gcode: \n')
        outfile.write('  _GINGER_FEEDER_DISABLE\n')
        outfile.write('\n')
        outfile.write(
            '################################### LED ###################################\n')
        outfile.write('\n')
        outfile.write('[led LED_CAMERA]\n')
        outfile.write('white_pin: extruder_board: PB5 #D13\n')
        outfile.write('cycle_time: 0.01\n')
        outfile.write('\n')
        outfile.write(
            '################################### Probe ##################################\n')
        outfile.write('\n')
        outfile.write('[servo PROBE_SERVO]\n')
        outfile.write('pin: extruder_board: PB2 #D10\n')
        outfile.write('maximum_servo_angle: 190\n')
        outfile.write(
            'minimum_pulse_width: 0.00077 #valore che corrisponde allo zero\n')
        outfile.write(
            'maximum_pulse_width: 0.00216 #valore che corrisponde al maximum_servo_angle\n')
        outfile.write('initial_angle: 185 #lo setto che sta in alto\n')
        outfile.write('\n')
        outfile.write('[probe]\n')
        outfile.write('pin: PG10\n')
        outfile.write('deactivate_on_each_sample: false #importante\n')
        outfile.write('x_offset: ' + values["probe/x_offset"] + '\n')
        outfile.write('y_offset: ' + values["probe/y_offset"] + '\n')
        outfile.write('z_offset: 10\n')
        outfile.write('speed: ' + values["probe/speed"] + '\n')
        outfile.write('samples: ' + values["probe/samples"] + '\n')
        outfile.write('sample_retract_dist: 2.0\n')
        outfile.write('samples_result: average\n')
        outfile.write('samples_tolerance: 0.200\n')
        outfile.write('samples_tolerance_retries: 1\n')
        outfile.write('activate_gcode: \n')
        outfile.write('  _GINGER_PROBE_DOWN\n')
        outfile.write('deactivate_gcode: \n')
        outfile.write('  _GINGER_PROBE_UP\n')
        outfile.write('\n')
        outfile.write('[safe_z_home]\n')
        outfile.write('home_xy_position: 0, 0\n')
        outfile.write('speed: ' + values["safe_z_home/speed"] + '\n')
        outfile.write('z_hop: 15\n')
        outfile.write('z_hop_speed: 8.0\n')
        outfile.write('\n')
        outfile.write('[bed_mesh]\n')
        outfile.write('speed: ' + values["bed_mesh/speed"] + '\n')
        outfile.write(
            'horizontal_move_z: 20 #15; Da scegliere a seconda dello z offset, deve essere di più\n')
        outfile.write('mesh_min: 0, 90\n')
        outfile.write('mesh_max: 1000, 1000 #1000\n')
        outfile.write('probe_count: 12, 12\n')
        outfile.write('fade_start: ' + values["bed_mesh/fade_start"] + '\n')
        outfile.write('fade_end: ' + values["bed_mesh/fade_end"] + '\n')
        outfile.write('algorithm: bicubic\n')
        outfile.write('bicubic_tension: 0.2\n')
        outfile.write('\n')
        outfile.write('[screws_tilt_adjust]\n')
        outfile.write('screw1: 0, 0\n')
        outfile.write('screw1_name: front left screw\n')
        outfile.write('screw2: 1000, 0\n')
        outfile.write('screw2_name: front right screw\n')
        outfile.write('screw3: 0, 1000\n')
        outfile.write('screw3_name: rear right screw\n')
        outfile.write('screw4: 1000, 1000\n')
        outfile.write('screw4_name: rear left screw\n')
        outfile.write('horizontal_move_z: 35\n')
        outfile.write('speed: 150\n')
        outfile.write('screw_factor: 2.365\n')
        outfile.write('screw_direction: CCW\n')
        outfile.write('\n')
        outfile.write(
            '############################### Thermistor #################################\n')
        outfile.write('\n')
        outfile.write('[temperature_sensor Octopus]\n')
        outfile.write('sensor_type: temperature_mcu\n')
        outfile.write('sensor_mcu: mcu\n')
        outfile.write('#sensor_temperature1:\n')
        outfile.write('#sensor_adc1:\n')
        outfile.write('\n')
        outfile.write('[temperature_sensor Pi]\n')
        outfile.write('sensor_type: temperature_host\n')
        outfile.write('\n')
        outfile.write(
            '############################### Kinematics #################################\n')
        outfile.write('\n')
        outfile.write('[printer]\n')
        outfile.write('kinematics: cartesian\n')
        outfile.write('max_velocity: 250 #up to 300           \n')
        outfile.write('max_accel: 4000                \n')
        outfile.write('max_z_velocity: 10               \n')
        outfile.write('max_z_accel: 500                 \n')
        outfile.write('square_corner_velocity: 5.0     \n')
        outfile.write('minimum_cruise_ratio: 0.0\n')
        outfile.write('\n')
        outfile.write('[gcode_arcs]\n')
        outfile.write('resolution: 1.0\n')
        outfile.write('\n')
        outfile.write('[input_shaper]\n')
        outfile.write('shaper_type_x:mzv\n')
        outfile.write('shaper_freq_x: 12.2\n')
        outfile.write('damping_ratio_x: 0.076\n')
        outfile.write('shaper_type_y:3hump_ei\n')
        outfile.write('shaper_freq_y: 19.8\n')
        outfile.write('damping_ratio_y: 0.07 #0.078\n')
        outfile.write('#shaper_type: mzv\n')
        outfile.write('\n')
        outfile.write(
            '#-------------------------------------------------------------------------------\n')
        outfile.write('# Axis: X\n')
        outfile.write(
            '#-------------------------------------------------------------------------------\n')
        outfile.write('[stepper_x]\n')
        outfile.write('step_pin: PF13\n')
        outfile.write('dir_pin: PF12\n')
        outfile.write('enable_pin: !PF14\n')
        outfile.write('microsteps: 16\n')
        outfile.write('rotation_distance: 60\n')
        outfile.write('full_steps_per_rotation: 200\n')
        outfile.write('step_pulse_duration: 0.00001 #0.000002\n')
        outfile.write('endstop_pin: PG6\n')
        outfile.write('position_endstop: 0\n')
        outfile.write('position_max: ' +
                      values["stepper_x/position_max"] + '\n')
        outfile.write('homing_speed: 40\n')
        outfile.write('homing_retract_dist: 5\n')
        outfile.write('homing_retract_speed: 20\n')
        outfile.write('second_homing_speed: 10\n')
        outfile.write('\n')
        outfile.write('[tmc5160 stepper_x]\n')
        outfile.write('cs_pin: PC4\n')
        outfile.write('spi_software_miso_pin: PA6\n')
        outfile.write('spi_software_mosi_pin: PA7\n')
        outfile.write('spi_software_sclk_pin: PA5\n')
        outfile.write('run_current: ' + values["stepper_x/run_current"] + '\n')
        outfile.write('sense_resistor: 0.022\n')
        outfile.write('#stealthchop_threshold: 999999\n')
        outfile.write('interpolate: False\n')
        outfile.write('\n')
        outfile.write(
            '#-------------------------------------------------------------------------------\n')
        outfile.write('# Axis: Y\n')
        outfile.write(
            '#-------------------------------------------------------------------------------\n')
        outfile.write('[stepper_y]\n')
        outfile.write('step_pin: PG0\n')
        outfile.write('dir_pin: PG1\n')
        outfile.write('enable_pin: !PF15\n')
        outfile.write('microsteps: 16\n')
        outfile.write('rotation_distance: 60\n')
        outfile.write('full_steps_per_rotation: 200\n')
        outfile.write('step_pulse_duration: 0.00001 #0.000002\n')
        outfile.write('endstop_pin: PG9\n')
        outfile.write('position_endstop: 0\n')
        outfile.write('position_max: ' +
                      values["stepper_y/position_max"] + '\n')
        outfile.write('homing_speed: 40\n')
        outfile.write('homing_retract_dist: 5\n')
        outfile.write('homing_retract_speed: 20\n')
        outfile.write('second_homing_speed: 10\n')
        outfile.write('\n')
        outfile.write('[tmc5160 stepper_y]\n')
        outfile.write('cs_pin: PD11\n')
        outfile.write('spi_software_miso_pin: PA6\n')
        outfile.write('spi_software_mosi_pin: PA7\n')
        outfile.write('spi_software_sclk_pin: PA5\n')
        outfile.write('run_current: ' + values["stepper_y/run_current"] + '\n')
        outfile.write('sense_resistor: 0.022\n')
        outfile.write('#stealthchop_threshold: 999999\n')
        outfile.write('interpolate: False\n')
        outfile.write('\n')
        outfile.write(
            '#-------------------------------------------------------------------------------\n')
        outfile.write('# Axis: Z\n')
        outfile.write(
            '#-------------------------------------------------------------------------------\n')
        outfile.write('[stepper_z]\n')
        outfile.write('step_pin: PF11\n')
        outfile.write('dir_pin: !PG3\n')
        outfile.write('enable_pin: !PG5\n')
        outfile.write('microsteps: 8\n')
        outfile.write('rotation_distance: 4 #passo vite\n')
        outfile.write('full_steps_per_rotation: 200\n')
        outfile.write('step_pulse_duration: 0.00002\n')
        outfile.write('endstop_pin: probe:z_virtual_endstop\n')
        outfile.write('#endstop_pin: PG10\n')
        outfile.write('#position_endstop: 15 #sarebbe il mio zeta offset?\n')
        outfile.write('position_min: -5\n')
        outfile.write('position_max: ' +
                      values["stepper_z/position_max"] + '\n')
        outfile.write('homing_speed: 7\n')
        outfile.write('homing_retract_dist: 2\n')
        outfile.write('homing_retract_speed: 8\n')
        outfile.write('second_homing_speed: 5\n')
        outfile.write('\n')
        outfile.write('[tmc5160 stepper_z]\n')
        outfile.write('cs_pin: PC6\n')
        outfile.write('spi_software_miso_pin: PA6\n')
        outfile.write('spi_software_mosi_pin: PA7\n')
        outfile.write('spi_software_sclk_pin: PA5\n')
        outfile.write('run_current: ' + values["stepper_z/run_current"] + '\n')
        outfile.write('hold_current: 4\n')
        outfile.write('sense_resistor: 0.022\n')
        outfile.write('#stealthchop_threshold: 999999\n')
        outfile.write('interpolate: False\n')
        outfile.write('\n')
        outfile.write(
            '############################### Printer #################################\n')
        outfile.write('\n')
        outfile.write('[virtual_sdcard]\n')
        outfile.write('path: ~/printer_data/gcodes\n')
        outfile.write('on_error_gcode: CANCEL_PRINT\n')
        outfile.write('\n')
        outfile.write('[force_move]\n')
        outfile.write('enable_force_move: True\n')
        outfile.write('\n')
        outfile.write('[exclude_object]\n')
        outfile.write('\n')
        outfile.write('[display_status]\n')
        outfile.write('\n')
        outfile.write('[mcu]\n')
        outfile.write('serial: ' + values["mcu/serial"] + '\n')
        outfile.write('\n')
        outfile.write('[mcu extruder_board]\n')
        outfile.write('serial: ' + values["mcu extruder_board/serial"] + '\n')
        outfile.write('\n')
        outfile.write('[idle_timeout]\n')
        outfile.write('timeout: 900\n')
        outfile.write('\n')
        outfile.write('[pause_resume]\n')
        outfile.write('recover_velocity: 80\n')
        outfile.write('\n')
        outfile.write(
            '############################### Auto Setup #################################""")\n')

    # execute klipper restart
    try:
        # TODO: restart klipper service, currently not working
        # subprocess.run(["sudo", "systemctl", "restart", "klipper.service"], check=True)
        # Ottieni solo il nome host, senza la porta
        host = request.host.split(':')[0]
        # Redirigi al servizio sulla porta 80
        return redirect(f"http://{host}:80/")
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "error": e.stderr}), 500


@app.route("/tools/backend/update-mainboard-serial", methods=["GET"])
def update_mainboard_serial():
    if os.name == "nt":
        serial = "/dev/serial/by-id/usb-Klipper_stm32h723xx_XXXXXXXXXXXXXXXXXXXXXXXX-XXXX"
    else:
        try:
            serials = os.listdir("/dev/serial/by-id/")
            serial = next(
                (s for s in serials if "usb-Klipper" in s),
                "Nessun dispositivo trovato"
            )
            serial = f"/dev/serial/by-id/{serial}" if "Nessun dispositivo trovato" not in serial else serial
        except FileNotFoundError:
            serial = "Directory /dev/serial/by-id/ non trovata"

    return jsonify({"success": True, "serial": serial})


@app.route("/tools/backend/update-extruder-board-serial", methods=["GET"])
def update_extruder_board_serial():
    if os.name == "nt":
        serial = "/dev/serial/by-id/usb-1a86_USB2.0-XXXX-XXXX-XXXXX"
    else:
        try:
            # Legge i seriali disponibili
            serials = os.listdir("/dev/serial/by-id/")
            serial = next(
                (s for s in serials if "usb-1a86_USB" in s),
                "Nessun dispositivo trovato"
            )
            serial = f"/dev/serial/by-id/{serial}" if "Nessun dispositivo trovato" not in serial else serial
        except FileNotFoundError:
            serial = "Directory /dev/serial/by-id/ non trovata"
    return jsonify({"success": True, "serial": serial})


@app.route("/tools/backend/restore-kamp-cfg", methods=["POST"])
def restore_kamp_cfg():
    backupFilePath = backupConfigPath + "/kamp.cfg"
    configFilePath = configPath + "/kamp.cfg"
    try:
        if os.path.exists(configFilePath):
            os.remove(configFilePath)
        shutil.copy2(backupFilePath, configFilePath)
        return redirect("/tools/utilities")
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "error": e.stderr}), 500


@app.route("/tools/backend/restore-klipperscreen-conf", methods=["POST"])
def restore_klipperscreen_conf():
    backupFilePath = backupConfigPath + "/klipperscreen.conf"
    configFilePath = configPath + "/klipperscreen.conf"
    try:
        if os.path.exists(configFilePath):
            os.remove(configFilePath)
        shutil.copy2(backupFilePath, configFilePath)
        return redirect("/tools/utilities")
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "error": e.stderr}), 500


@app.route("/tools/backend/restore-moonraker-conf", methods=["POST"])
def restore_moonraker_conf():
    backupFilePath = backupConfigPath + "/moonraker.conf"
    configFilePath = configPath + "/moonraker.conf"
    try:
        if os.path.exists(configFilePath):
            os.remove(configFilePath)
        shutil.copy2(backupFilePath, configFilePath)
        return redirect("/tools/utilities")
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "error": e.stderr}), 500
    

@app.route("/tools/run/<script_name>", methods=["POST"])
def run_script(script_name):
    script_path = f"/home/pi/G1-Configs/scripts/{script_name}.sh"
    try:
        result = subprocess.run(
            ["/bin/bash", script_path], capture_output=True, text=True, check=True
        )
        return jsonify({"success": True, "output": result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "error": e.stderr}), 500


@app.route("/tools/<path:subpath>", methods=["GET"])
def get_page(subpath):
    return render_template("index.html", subpath=subpath)


@app.route("/tools/")
def get_index():
    return render_template("index.html", subpath="")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
