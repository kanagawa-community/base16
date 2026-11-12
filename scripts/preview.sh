# Preview hook for .github/scripts/render-previews.sh: prints the 16 slots of
# each scheme as color swatches with their hex values, so the image shows the
# scheme itself. A builder decides where each slot goes, so there is no app to
# run.
# Requires: python3.
# shellcheck shell=bash
name=base16

capture() {
  python3 -I - "$root/themes/kanagawa-$1.yaml" >"$2" <<'PY'
import re
import sys

text = open(sys.argv[1]).read()
slots = re.findall(r'^  (base0[0-9A-F]): "#([0-9a-f]{6})"', text, re.M)
for i, (slot, h) in enumerate(slots):
    r, g, b = (int(h[j : j + 2], 16) for j in (0, 2, 4))
    end = "\n" if i % 2 == 1 else "   "
    print(f"\x1b[48;2;{r};{g};{b}m      \x1b[0m {slot} #{h}", end=end)
PY
}
