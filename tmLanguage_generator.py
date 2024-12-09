import json
from colorsys import rgb_to_hls, hls_to_rgb

# Define the template for the TextMate grammar
tmlanguage_template = {
    "$schema": "https://raw.githubusercontent.com/martinring/tmlanguage/master/tmlanguage.json",
    "name": "ScratchText",
    "patterns": [
        {
            "include": "#strings"
        },
        {
            "include": "#commands"
        }
    ],
    "repository": {
        "strings": {
            "name": "input.stringdoublequotes.scratchtext",
            "begin": "\"",
            "end": "\"",
            "patterns": []
        },
        "commands": {
            "patterns": []
        }
    },
    "scopeName": "source.scratchtext"
}

# Category colors
category_colors = {
    "motion": "4C97FF",
    "looks": "9966FF",
    "sound": "CF63CF",
    "events": "FFBF00",
    "control": "FFAB19",
    "sensing": "5CB1D6",
    "operators": "59C059",
    "variables": "FF8C1A",
    "lists": "FF661A",
    "pen": "0FBD8C"
}

# Define block types and brightness adjustments
block_types = {
    "hat": 1.0,
    "reporter": 0.8,
    "stack": 1.2,
    "c": 1.4,
    "cap": 1.6
}

# Function to adjust color brightness
def adjust_brightness(hex_color, factor):
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    h, l, s = rgb_to_hls(r, g, b)
    l = min(1, max(0, l * factor))
    r, g, b = hls_to_rgb(h, l, s)
    return f"{int(r * 255):02X}{int(g * 255):02X}{int(b * 255):02X}"

# Parse the commands.txt file and generate the tmlanguage patterns
current_category = None
all_type_combos = {}
with open("commands.txt", "r") as file:
    for line in file:
        line = line.strip()
        # Check for a category marker
        if line.startswith("# NAME:"):
            current_category = line.split(":")[1].strip().lower()
        # Skip comments and blank lines
        elif line and not line.startswith("#") and current_category:
            # Extract command and type
            parts = line.split(":")
            command_type = parts[2] if len(parts) > 2 else "unknown"
            
            # Generate color based on category and block type
            base_color = category_colors.get(current_category, "FFFFFF")
            adjusted_color = adjust_brightness(base_color, block_types.get(command_type, 1.0))

            # Generate the command pattern
            cmd_key = f"scrblock.{current_category}.{command_type}.scratchtext"

            # Add to dictionary
            if not cmd_key in all_type_combos:
                all_type_combos[cmd_key] = line.split(':')[0]
            else:
                all_type_combos[cmd_key] += "|" + line.split(':')[0]

    # Add all matches to the json structure
    for key in all_type_combos.keys():
        # Add the broader scope for the category and type
        tmlanguage_template["repository"]["commands"]["patterns"].append({
            "name": key,
            "match": f"(?i)\\b({all_type_combos[key]})\\b"
        })

    # Number matching
    tmlanguage_template["patterns"].append({
        "name": "input.num.scratchtext",
        "match": "(?<!-)\\b(\\d*\\.\\d+|\\d+)\\b"
    })

    # Comment line matching
    tmlanguage_template["patterns"].append({
        "name": "block.comment.scratchtext",
        "match": "#(?=(?:[^\"']*(?:\"|'))*[^\"']*$).*"
    })

    # Variable matching
    tmlanguage_template["patterns"].append({
        "name": "input.variable.scratchtext",
        "match": r"\$(.*?)(?=[,)])"
    })

    # List matching
    tmlanguage_template["patterns"].append({
        "name": "input.list.scratchtext",
        "match": r"\@(.*?)(?=[,)])"
    })

# Save the generated .tmlanguage.json file
with open("syntaxes/scratchtext.tmLanguage.json", "w") as tmlanguage_file:
    json.dump(tmlanguage_template, tmlanguage_file, indent=4)

print("TextMate grammar file generated: scratchtext.tmLanguage.json")
