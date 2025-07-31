import sys
from pathlib import Path
import re

G_COMMANDS_TO_COMMENT = {"G1", "G2", "G3", "G4"}

def extract_gcode_command(line):
    line = line.split(';')[0].strip()
    match = re.match(r'^([GMT]\d+)', line, re.IGNORECASE)
    return match.group(1).upper() if match else None

def extract_z_value(line):
    match = re.search(r'\bZ(-?\d+(?:\.\d+)?)', line, re.IGNORECASE)
    return float(match.group(1)) if match else None

def convert_start_to_resume(line, force_z):
    new_line = line.replace("START_PRINT", "RESUME_PRINT").strip()
    new_line += f" FORCE_Z={force_z:.3f}"
    return new_line + "\n"

def process_file(input_path, output_path, plr_move_count):
    lines = input_path.read_text().splitlines(keepends=True)
    
    resume_index = None
    comment_count = 0
    last_z = None
    output_lines = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        if resume_index is None and stripped.startswith("START_PRINT"):
            resume_index = len(output_lines)
            output_lines.append("__RESUME_PLACEHOLDER__")  # placeholder temporaneo
        else:
            cmd = extract_gcode_command(line)
            if resume_index is not None and cmd in G_COMMANDS_TO_COMMENT and comment_count < plr_move_count:
                z_val = extract_z_value(line)
                if z_val is not None:
                    last_z = z_val
                output_lines.append(f"; {line}")
                comment_count += 1
            else:
                output_lines.append(line)

    if resume_index is not None:
        resume_line = convert_start_to_resume(lines[resume_index], last_z if last_z is not None else 0.0)
        output_lines[resume_index] = resume_line

    output_path.write_text("".join(output_lines))

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
