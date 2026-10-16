"""Build the style specimen (examples/specimen.pptx): tokens sheet, a generic architecture
figure and a demo plot. Doubles as the usage example and the regression test of figkit.

    python demo_specimen.py [--out ../examples]
    python render.py ../examples/specimen.pptx -o ../examples --frame
"""
import argparse
import os

import numpy as np

import plot_style as ps
import tokens as T
from figkit import Deck, text_width


def tokens_sheet(deck):
    fig = deck.figure("full", height=4.3, name="tokens (reference sheet, not a figure)")
    fig.title(0.2, 0.15, "(a)", "Type and colour")
    x = 0.35
    for size, weight, label in (("title", "semibold", "Title 20 · SemiBold"), ("module", "medium", "Module 16 · Medium"),
                                ("note", "regular", "Note 12 · Regular"), ("module", "regular", "Math  $e_0$, $z_p$, $r^{p−1}$, $α$")):
        w = text_width(label, size, weight) + 0.4
        fig.text(x, 0.85, w, 0.5, label, size=size, weight=weight, color="strong")
        x += w + 0.35

    x = 0.35
    for r in ("base", "orange", "blue", "violet", "green", "red"):
        fig.box(x, 1.65, 1.55, 0.6, "Base" if r == "base" else r.capitalize(), role=r)
        x += 1.85
    fig.box(0.35, 2.65, 1.55, 0.6, "Novel", role="orange", emphasis=True)
    fig.op(2.55, 2.95, "+", role="violet", emphasis=True)
    fig.vector(3.2, 2.63, n=4, role="base")
    fig.vector(3.55, 2.63, n=4, role="orange")
    fig.vector(3.9, 2.63, n=4, role="violet")
    fig.icon("snowflake", 4.45, 2.8, size=0.3)
    fig.icon("flame", 4.95, 2.8, size=0.3)
    a = fig.box(5.75, 2.65, 1.2, 0.6, "A")
    b = fig.box(7.65, 2.65, 1.2, 0.6, "B")
    fig.arrow(a, b)
    c = fig.box(9.55, 2.65, 1.2, 0.6, "C", role="violet")
    fig.arrow(b, c, dashed=True)
    fig.text(0.35, 3.55, 11.0, 0.4,
             "Canvas → print × 0.6:  20 / 16 / 12 pt → 12 / 9.6 / 7.2 pt   ·   border 1.25 pt   ·   arrow 1.5 pt   ·   radius 0.10 in",
             size="note", color="muted")


def architecture(deck):
    """Generic example (not from any paper): frozen backbone, trainable adapter, fusion."""
    fig = deck.figure("full", height=4.45, name="architecture")
    fig.title(0.2, 0.15, "(b)", "Example architecture")
    inp = fig.box(0.4, 1.55, 1.3, 0.7, "Image $x$")
    grp = fig.group(2.15, 0.8, 3.55, 2.2, "Frozen backbone")
    fig.icon("snowflake", 2.15 + 0.2 + text_width("Frozen backbone", "module", "semibold") + 0.12, 0.88, size=0.26)
    stem = fig.box(2.45, 1.55, 1.3, 0.7, "Stem")
    enc = fig.box(4.1, 1.55, 1.3, 0.7, "Encoder")
    fig.arrow(inp, stem)
    fig.arrow(stem, enc)
    fig.dot(6.0, 1.9)
    fig.path([enc.right, (6.0, 1.9)], head="none")
    head = fig.box(6.45, 0.75, 1.4, 0.7, "Head")
    ada = fig.box(6.45, 2.35, 1.4, 0.7, "Adapter", role="orange", emphasis=True)
    fig.icon("flame", 6.45 + 1.4 - 0.13, 2.35 - 0.14, size=0.28)
    fig.path([(6.0, 1.9), (6.0, 1.1), head.left])
    fig.path([(6.0, 1.9), (6.0, 2.7), ada.left])
    e0 = fig.vector(8.3, 0.72, n=4, role="base")
    e1 = fig.vector(8.3, 2.32, n=4, role="orange")
    fig.text(8.05, 0.28, 0.7, 0.4, "$e_0$", size="module", align="center")
    fig.text(8.05, 3.12, 0.7, 0.35, "$e_1$", size="module", align="center", color="orange.text")
    fig.arrow(head, e0)
    fig.arrow(ada, e1)
    op = fig.op(9.35, 1.9, "+", role="violet", emphasis=True)
    fig.path([e0.right, (9.35, 1.1), op.top])
    fig.path([e1.right, (9.35, 2.7), op.bottom])
    fig.text(8.7, 1.25, 0.6, 0.35, "$α$", size="note", align="right")
    fig.text(8.5, 2.2, 0.8, 0.35, "$1−α$", size="note", align="right")
    z = fig.vector(10.05, 1.52, n=4, role="violet")
    fig.arrow(op, z)
    fig.text(9.78, 1.05, 0.7, 0.4, "$z$", size="module", align="center", color="violet.text")
    loss = fig.text(9.63, 2.6, 1.0, 0.4, "$L_{task}$", size="module", align="center")
    fig.arrow((10.13, 2.36), (10.13, 2.62), dashed=True)
    fig.path([(10.13, 3.0), (10.13, 3.65), (7.15, 3.65), ada.bottom], dashed=True)
    fig.legend(0.4, 3.95, [("arrow", "Forward pass"), ("dashed", "Training only"),
                           ("icon:snowflake", "Frozen"), ("icon:flame", "Trainable")])
    return grp, loss


def demo_plot(deck, out):
    """Column-width plot with made-up numbers, inserted 1:1."""
    fig_mpl, ax = ps.figure("column", height=3.9)
    x = np.array([1, 2, 4, 8, 16])
    for k, (name, y0) in enumerate((("Baseline A", 61), ("Baseline B", 64))):
        y = y0 + 6 * np.log2(x) ** 0.8
        ax.plot(x, y, color=ps.BASE if k else ps.BASE_DARK, marker="o", ms=7)
        ax.annotate(name, (x[-1], y[-1]), xytext=(8, 0), textcoords="offset points", va="center", color=ps.BASE_DARK)
    y = 68 + 7 * np.log2(x) ** 0.8
    ax.plot(x, y, color=ps.C["violet"], marker="o")
    ax.annotate("Ours", (x[-1], y[-1]), xytext=(8, 0), textcoords="offset points", va="center",
                color=ps.DARK["violet"], weight="semibold")
    ax.set_xscale("log", base=2)
    ax.set_xticks(x, [str(v) for v in x])
    ax.set_xlim(0.8, 40)
    ax.spines["bottom"].set_bounds(1, 16)
    ax.set_xlabel("Compute (×)")
    ax.set_ylabel("Accuracy (%)")
    ax.set_title("(c)  Demo data")
    png = ps.save(fig_mpl, os.path.join(out, "demo_plot"))
    fig = deck.figure("column", height=3.9, name="demo plot")
    fig.picture(png, 0, 0, w=T.frame_width("column"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "examples"))
    a = ap.parse_args()
    deck = Deck()
    tokens_sheet(deck)
    architecture(deck)
    demo_plot(deck, a.out)
    print(deck.save(os.path.join(a.out, "specimen.pptx")))


if __name__ == "__main__":
    main()
