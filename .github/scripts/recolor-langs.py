"""Replace GitHub's per-language colors in the top-langs cards with the profile palette."""
import re
import sys

PALETTES = {
    "light": {
        "langs": ["#D40063", "#A8004E", "#E8559A", "#F2B8D2", "#5F5A66", "#C9C4CF"],
        "track": "#E4E0E7",
    },
    "dark": {
        "langs": ["#F74D96", "#FF7AB0", "#D40063", "#A8004E", "#A29CAC", "#4A4454"],
        "track": "#332E3C",
    },
}

for path, theme in zip(sys.argv[1::2], sys.argv[2::2]):
    palette = PALETTES[theme]
    svg = open(path, encoding="utf-8").read()

    # Language colors appear as fill="#xxxxxx" attributes, ordered by usage; skip the transparent card bg.
    found = []
    for color in re.findall(r'fill="(#[0-9a-fA-F]{6})"', svg):
        if color not in found:
            found.append(color)
    for i, color in enumerate(found):
        svg = svg.replace(f'fill="{color}"', f'fill="{palette["langs"][i % len(palette["langs"])]}"')

    svg = re.sub(r"\.progress-background \{ fill: #[0-9a-fA-F]+; \}",
                 f".progress-background {{ fill: {palette['track']}; }}", svg)
    open(path, "w", encoding="utf-8").write(svg)
