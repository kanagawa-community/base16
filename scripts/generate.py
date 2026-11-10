#!/usr/bin/env python3
"""Write themes/kanagawa-<variant>.yaml from the shared palette.

Usage: scripts/generate.py [path/to/palette.json]   (default: ../.github/palette.json)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VARIANTS = ["wave", "dragon", "lotus"]
ANSI = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
# The 16 ANSI colors, normal then bright.
COLORS = [f"term.{c}" for c in ANSI] + [f"term.bright_{c}" for c in ANSI]


def roles(variant):
    """Map each role to its hex color; a role missing from the palette raises KeyError later."""
    return {role: c["hex"] for c in variant["colors"].values() for role in c["usage"]}

# base16 slot -> palette role, by the base16 styling guide.
SLOTS = {
    "base00": "ui.bg",  # default background
    "base01": "ui.bg_p1",  # lighter background (status bars)
    "base02": "ui.bg_visual",  # selection background
    "base03": "syn.comment",  # comments, invisibles
    "base04": "ui.fg_dim",  # dark foreground (status bars)
    "base05": "ui.fg",  # default foreground
    "base06": "term.bright_white",  # light foreground
    "base07": "ui.bg_p2",  # light background
    "base08": "term.red",  # variables, tags, deleted
    "base09": "syn.constant",  # integers, constants
    "base0A": "term.yellow",  # classes, search background
    "base0B": "syn.string",  # strings, inserted
    "base0C": "term.cyan",  # support, regular expressions
    "base0D": "syn.fun",  # functions, headings
    "base0E": "syn.keyword",  # keywords, changed
    "base0F": "term.extended_2",  # deprecated, embedded tags
}


def theme(variant, appearance, c):
    out = [
        'system: "base16"',
        f'name: "Kanagawa {variant.capitalize()}"',
        'author: "Kanagawa Community (https://github.com/kanagawa-community/base16)"',
        f'variant: "{appearance}"',
        "palette:",
    ]
    out += [f'  {k}: "{c[r]}"' for k, r in SLOTS.items()]
    return "\n".join(out) + "\n"


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / ".github" / "palette.json"
    variants = json.loads(path.read_text())["variants"]
    for v in VARIANTS:
        out = ROOT / "themes" / f"kanagawa-{v}.yaml"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(theme(v, variants[v]["appearance"], roles(variants[v])))
        print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
