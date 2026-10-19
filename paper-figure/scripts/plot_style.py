"""matplotlib in the house style: Inter everywhere (math too), canvas-scale sizes, shared palette.

    import plot_style as ps
    fig, ax = ps.figure("column", height=3.6)            # canvas inches = the PPT frame size
    ax.plot(x, y_base, color=ps.BASE, lw=ps.LW)          # baselines grey
    ax.plot(x, y_ours, color=ps.C["violet"], lw=ps.LW)   # ours in the accent
    ps.save(fig, "out/fig_tradeoff")                    # .png for PPT, .pdf/.svg vector copies

Draw at canvas size and insert 1:1 (fig.picture(png, 0, 0, w=frame width)), so tick labels,
axis labels and panel titles print at the same sizes as the diagram text (tokens.SIZE x PRINT_SCALE).
Do not save with bbox_inches="tight": it changes the size and therefore the printed type size.
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from cycler import cycler  # noqa: E402
from matplotlib import font_manager  # noqa: E402

import tokens as T  # noqa: E402

for _w in ("regular", "medium", "semibold", "bold"):
    for _it in (False, True):
        try:
            font_manager.fontManager.addfont(T.font_file(_w, _it))
        except FileNotFoundError:
            pass

C = {k: "#" + v["line"] for k, v in T.ACCENTS.items()}  # line / marker colours
FILL = {k: "#" + v["fill"] for k, v in T.ACCENTS.items()}  # area fills
DARK = {k: "#" + v["text"] for k, v in T.ACCENTS.items()}  # annotation text in an accent
BASE = "#" + T.GRAY["border"]  # baselines and reference series
BASE_DARK = "#" + T.GRAY["muted"]
TEXT = "#" + T.GRAY["text"]
LW = 1.4  # data lines (~0.85 pt in print; user 2026-10-19: thinner, legibility first)
MS = 6.5  # marker size

plt.rcParams.update({
    "font.family": "Inter",
    "font.size": T.SIZE["note"],
    "mathtext.fontset": "custom",
    "mathtext.rm": "Inter",
    "mathtext.it": "Inter:italic",
    "mathtext.bf": "Inter:bold",
    "mathtext.sf": "Inter",
    "mathtext.cal": "Inter:italic",
    "mathtext.tt": "Inter",
    "mathtext.fallback": "stixsans",  # missing symbols stay sans-serif (rule 3)
    "text.color": TEXT,
    "axes.titlesize": T.SIZE["title"],
    "axes.titleweight": "semibold",
    "axes.titlelocation": "left",
    "axes.titlepad": 10,
    "axes.labelsize": T.SIZE["module"],
    "axes.labelcolor": TEXT,
    "axes.edgecolor": BASE,
    "axes.linewidth": T.LINE["border"],
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "axes.axisbelow": True,
    "grid.color": "#" + T.GRAY["fill2"],
    "grid.linewidth": T.LINE["guide"],
    "axes.prop_cycle": cycler(color=[C["violet"], C["orange"], C["blue"], C["green"], C["red"], BASE_DARK]),
    "xtick.labelsize": T.SIZE["note"],
    "ytick.labelsize": T.SIZE["note"],
    "xtick.color": BASE_DARK,
    "ytick.color": BASE_DARK,
    "xtick.labelcolor": TEXT,
    "ytick.labelcolor": TEXT,
    "xtick.major.width": T.LINE["border"],
    "ytick.major.width": T.LINE["border"],
    "xtick.major.size": 5,
    "ytick.major.size": 5,
    "xtick.minor.width": T.LINE["guide"],
    "ytick.minor.width": T.LINE["guide"],
    "lines.linewidth": LW,
    "lines.markersize": MS,
    "patch.linewidth": T.LINE["border"],
    "legend.fontsize": T.SIZE["note"],
    "legend.frameon": False,
    "legend.handlelength": 1.6,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "savefig.dpi": 400,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
})


def figure(slot="column", height=3.6, nrows=1, ncols=1, width=None, venue="ieee", **kw):
    """Figure at canvas size (inches) with constrained layout."""
    w = width or T.frame_width(slot, venue)
    return plt.subplots(nrows, ncols, figsize=(w, height), layout="constrained", **kw)


def save(fig, stem, formats=("png", "pdf", "svg")):
    """Write stem.png (400 dpi, for PPT) and vector copies; returns the PNG path."""
    os.makedirs(os.path.dirname(os.path.abspath(stem)), exist_ok=True)
    for ext in formats:
        fig.savefig(f"{stem}.{ext}")
    plt.close(fig)
    return f"{stem}.png"
