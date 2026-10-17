"""House-style tokens shared by figkit.py (PowerPoint) and plot_style.py (matplotlib).

Every number here is on the PPT canvas. A figure is drawn at canvas size and shrunk by
PRINT_SCALE when it goes into the paper (canvas width = printed width / PRINT_SCALE), so all
figures print with the same type sizes and line weights. Change a value here, not in a figure
script; that is what keeps every figure in one style.
"""
import os

# ---- scale -----------------------------------------------------------------------------------
PRINT_SCALE = 0.6  # 20/16/12 pt on canvas -> 12/9.6/7.2 pt in print

# Printed widths (inches), read from the template class. Add a venue only after checking its
# \the\columnwidth and \the\textwidth.
VENUES = {
    "ieee": {"column": 3.4, "full": 7.0},  # ieeeconf.cls: textwidth 7.0in, columnsep 0.2in
}


def frame_width(slot="full", venue="ieee"):
    """Canvas width (inches) for a single-column ('column') or full-width ('full') figure."""
    return VENUES[venue][slot] / PRINT_SCALE


# ---- type ------------------------------------------------------------------------------------
FONT = "Inter"  # the only typeface in every figure, math included (Inter Italic)

# PowerPoint family name and bold flag per weight. Static Inter TTFs expose Medium/SemiBold as
# separate families ("Inter Medium"), which is how PowerPoint and LibreOffice both find them.
WEIGHTS = {
    "regular": ("Inter", False),
    "medium": ("Inter Medium", False),
    "semibold": ("Inter SemiBold", False),
    "bold": ("Inter", True),
}

# Three tiers only (user rule: title 18-20, module 14-16, note 11-12). One scale per paper.
TYPE_SCALES = {
    "standard": {"title": 20, "module": 16, "note": 12},
    "compact": {"title": 18, "module": 14, "note": 11},
}
SIZE = dict(TYPE_SCALES["standard"])


def use_type_scale(name):
    """Switch the whole paper to another scale (call once, before drawing)."""
    SIZE.clear()
    SIZE.update(TYPE_SCALES[name])


FONT_DIRS = [os.environ.get("INTER_DIR", ""), os.path.expanduser("~/Library/Fonts"), "/Library/Fonts"]


def font_file(weight="regular", italic=False):
    """Path of the static Inter TTF for a weight (used for text measuring and matplotlib)."""
    stem = {"regular": "Regular", "medium": "Medium", "semibold": "SemiBold", "bold": "Bold"}[weight]
    if italic:
        stem = "Italic" if stem == "Regular" else stem + "Italic"
    for d in FONT_DIRS:
        p = os.path.join(d, f"Inter-{stem}.ttf")
        if d and os.path.exists(p):
            return p
    raise FileNotFoundError(f"Inter-{stem}.ttf not found; install Inter static TTFs into ~/Library/Fonts")


# ---- colour ----------------------------------------------------------------------------------
# Neutral grey carries everything that is not new (frozen / pretrained / baseline modules,
# arrows, text). Accents are reserved for the contribution; use at most 2-4 hues per figure.
# Hex values follow Open Color (MIT): fill = shade 1, line = shade 6, text = shade 9, glow = 3.
GRAY = {
    "bg": "F8F9FA",  # group / panel background
    "fill": "F1F3F5",  # base module fill
    "fill2": "E9ECEF",
    "guide": "DEE2E6",  # dividers, grid
    "border": "ADB5BD",  # base module border
    "muted": "868E96",  # notes, secondary text, frozen icon
    "text": "343A40",  # module labels, arrows
    "strong": "212529",  # titles
    "white": "FFFFFF",
}

ACCENTS = {  # bg = shade 0, for large containers so colour stays light
    "orange": {"bg": "FFF4E6", "fill": "FFE8CC", "line": "FD7E14", "text": "D9480F", "glow": "FFC078"},
    "blue": {"bg": "E7F5FF", "fill": "D0EBFF", "line": "228BE6", "text": "1864AB", "glow": "74C0FC"},
    "violet": {"bg": "F3F0FF", "fill": "E5DBFF", "line": "7950F2", "text": "5F3DC4", "glow": "B197FC"},
    "green": {"bg": "EBFBEE", "fill": "D3F9D8", "line": "40C057", "text": "2B8A3E", "glow": "8CE99A"},
    "red": {"bg": "FFF5F5", "fill": "FFE3E3", "line": "FA5252", "text": "C92A2A", "glow": "FFA8A8"},
}

ROLE_BASE = {"bg": GRAY["bg"], "fill": GRAY["fill"], "line": GRAY["border"], "text": GRAY["text"], "glow": GRAY["guide"]}


def role(name):
    """Colour set for a role: 'base' (grey) or an accent name."""
    return ROLE_BASE if name in (None, "base", "gray", "grey") else ACCENTS[name]


# ---- lines and shapes (canvas pt / inches) ---------------------------------------------------
LINE = {
    "border": 1.25,  # every module and container border
    "emphasis": 2.0,  # border of the highlighted (novel) module
    "arrow": 1.5,  # every arrow / connector
    "guide": 1.0,  # dividers
}
ARROW_HEAD = {"type": "triangle", "w": "med", "len": "med"}
DASH = "dash"  # one dash style for every 'training-only' / auxiliary relation
RADIUS = 0.10  # inches, the same absolute corner radius on every rounded rectangle
GLOW = {"radius": 6.0, "alpha": 0.55}  # pt, opacity of the halo around a highlighted module

# ---- spacing (inches on canvas) --------------------------------------------------------------
GRID = 0.05  # all coordinates snap to this grid
PAD = 0.12  # text inset inside a module
GAP = 0.30  # minimum gap between neighbouring modules
GROUP_PAD = 0.20  # inset of a container around its modules
MARGIN = 0.20  # keep-out band inside the export frame
