import json
from colorsys import rgb_to_hls, hls_to_rgb

# Function to adjust color brightness
def adjust_brightness(hex_color, factor):
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    h, l, s = rgb_to_hls(r, g, b)
    l = min(1, max(0, l * factor))
    r, g, b = hls_to_rgb(h, l, s)
    return f"{int(r * 255):02X}{int(g * 255):02X}{int(b * 255):02X}"

# Define category colors
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

# Initialize data structure for theme
theme = {
    "name": "Gradient Theme",
    "type": "dark",
    "tokenColors": []
}

# Parse the commands.txt file
current_category = None
seen_category_types = set()  # To avoid duplicate entries
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
            
            # Skip duplicate category+type combinations
            if (current_category, command_type) not in seen_category_types:
                seen_category_types.add((current_category, command_type))
                
                # Generate color based on category and block type
                base_color = category_colors.get(current_category, "FFFFFF")
                adjusted_color = adjust_brightness(base_color, block_types.get(command_type, 1.0))
                
                # Add the broader scope for the category and type
                theme["tokenColors"].append({
                    "scope": f"support.function.{current_category}.{command_type}.scratchtext",
                    "settings": {"foreground": f"#{adjusted_color}"}
                })
    
    theme["tokenColors"].append({
        "scope": "string.quoted.double.scratchtext",
        "settings": {"foreground": "#d60b37"}
    })
    theme["tokenColors"].append({
        "scope": "constant.numeric.scratchtext",
        "settings": {"foreground": "#d60b37"}
    })
    theme["tokenColors"].append({
        "scope": "comment.line.scratchtext",
        "settings": {"foreground": "#E4DB8C"}
    })
    theme["tokenColors"].append({
        "scope": "variable.scratchtext",
        "settings": {"foreground": "#FF8C1A"}
    })
    theme["tokenColors"].append({
        "scope": "list.scratchtext",
        "settings": {"foreground": "#FF661A"}
    })

# Save the theme file
with open("themes/scratchtext-dark.json", "w") as theme_file:
    json.dump(theme, theme_file, indent=4)

print("Gradient theme file generated: scratchtext-dark.json")
