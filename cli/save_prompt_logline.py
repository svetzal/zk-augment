import json
import sys

if len(sys.argv) != 3:
    print("Usage: python save_prompt_logline.py <line_number>")
    sys.exit(1)

try:
    line_number = int(sys.argv[1])
except ValueError:
    print("Please provide a valid integer for the line number.")
    sys.exit(1)

key = sys.argv[2]

# read this specific line number out of zksv.log
with open("../zksv.log", "r") as file:
    lines = file.readlines()
    try:
        line = lines[line_number-1]
    except IndexError:
        print("Line number out of range.")
        sys.exit(1)

    data = json.loads(line)
    print(data[key])