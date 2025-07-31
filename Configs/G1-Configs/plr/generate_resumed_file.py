import sys
from pathlib import Path
import re

G_COMMANDS_TO_COMMENT = {"G1", "G2", "G3", "G4"}


def extract_gcode_command(line):
    """Estrae il comando principale G/M/T da una riga G-code."""
    line = line.split(';')[0].strip()
    match = re.match(r'^([GMT]\d+)', line, re.IGNORECASE)
    return match.group(1).upper() if match else None


def convert_start_to_resume(line):
    """Funzione che trasforma la riga START_PRINT... in RESUME_PRINT."""
    return line.replace("START_PRINT", "RESUME_PRINT")


def process_file(input_path, output_path, plr_move_count):
    found_start = False
    comment_count = 0

    with input_path.open('r') as infile, output_path.open('w') as outfile:
        for line in infile:
            stripped_line = line.strip()

            if not found_start:
                if stripped_line.startswith("START_PRINT"):
                    found_start = True
                    # Scrivi la riga RESUME_PRINT al posto della START_PRINT
                    outfile.write(convert_start_to_resume(line))
                else:
                    outfile.write(line)
            else:
                # Dopo START_PRINT: commenta G1-G4 fino a raggiungere il plr_move_count
                cmd = extract_gcode_command(line)
                if cmd in G_COMMANDS_TO_COMMENT and comment_count < plr_move_count:
                    outfile.write(f"; {line}")
                    comment_count += 1
                else:
                    outfile.write(line)


def main():
    if len(sys.argv) != 3:
        print("Usage: python recover_plr.py <plr_move_count> <file_path>")
        sys.exit(1)

    plr_move_count = int(sys.argv[1])
    input_file = Path(sys.argv[2])

    if not input_file.exists():
        print(f"Error: File not found - {input_file}")
        sys.exit(1)

    output_file = input_file.with_suffix('.recovered.gcode')
    process_file(input_file, output_file, plr_move_count)

    print(f"Recovery completed. Output saved to: {output_file}")


if __name__ == '__main__':
    main()
