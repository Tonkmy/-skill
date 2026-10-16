"""Render a deck to PNG for self-checking, and crop figures to their FRAME for LaTeX.

    python render.py deck.pptx -o out/                    # PNG of every slide
    python render.py deck.pptx -o out/ --frame            # crop to FRAME -> slideN.png + slideN.pdf
    python render.py exported.pdf --pptx deck.pptx -o out/ --frame   # crop a PowerPoint "Save as PDF"
    options: --slides 1,3   --dpi 220

LibreOffice renders the preview. In headless mode it only sees fonts listed by fontconfig, so this
script points it at Homebrew's fonts.conf (which covers ~/Library/Fonts); without that, Inter,
Arial and Cambria silently fall back to bundled fonts. PowerPoint stays the reference for the
final look (glow and kerning can differ slightly).
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

import pymupdf
from pptx import Presentation

FONTCONF = ["/opt/homebrew/etc/fonts/fonts.conf", "/usr/local/etc/fonts/fonts.conf"]


def soffice_pdf(pptx, outdir):
    exe = shutil.which("soffice") or "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    env = dict(os.environ)
    for conf in FONTCONF:
        if os.path.exists(conf):
            env.setdefault("FONTCONFIG_FILE", conf)
            break
    profile = os.path.join(tempfile.gettempdir(), "paper-figure-lo-profile")
    cmd = [exe, "--headless", f"-env:UserInstallation=file://{profile}", "--convert-to", "pdf", "--outdir", outdir, pptx]
    subprocess.run(cmd, env=env, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)
    pdf = os.path.join(outdir, os.path.splitext(os.path.basename(pptx))[0] + ".pdf")
    if not os.path.exists(pdf):
        sys.exit(f"LibreOffice did not produce {pdf}")
    return pdf


def frames(pptx):
    """{slide index: (x, y, w, h) in EMU} of the shape whose name starts with FRAME, plus slide width."""
    prs = Presentation(pptx)
    out = {}
    for i, slide in enumerate(prs.slides):
        for shp in slide.shapes:
            if shp.name.startswith("FRAME"):
                out[i] = (shp.left, shp.top, shp.width, shp.height)
                break
    return out, prs.slide_width


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src", help=".pptx (rendered with LibreOffice) or .pdf (e.g. PowerPoint export)")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--pptx", help="deck that holds the FRAME shapes when src is a PDF")
    ap.add_argument("--frame", action="store_true", help="crop each slide to its FRAME and write a PDF too")
    ap.add_argument("--slides", help="1-based list, e.g. 1,3")
    ap.add_argument("--dpi", type=int, default=200)
    a = ap.parse_args()

    os.makedirs(a.out, exist_ok=True)
    src = os.path.abspath(a.src)
    deck = src if src.endswith(".pptx") else (os.path.abspath(a.pptx) if a.pptx else None)
    pdf = soffice_pdf(src, a.out) if src.endswith(".pptx") else src
    doc = pymupdf.open(pdf)
    fr, slide_w = frames(deck) if (a.frame and deck) else ({}, None)
    if a.frame and not deck:
        sys.exit("--frame on a PDF needs --pptx to know where the FRAMEs are")
    pick = [int(s) - 1 for s in a.slides.split(",")] if a.slides else range(doc.page_count)
    stem = os.path.splitext(os.path.basename(src))[0]
    for i in pick:
        page = doc[i]
        clip = None
        if a.frame and i in fr:
            k = page.rect.width / slide_w
            x, y, w, h = (v * k for v in fr[i])
            clip = pymupdf.Rect(x, y, x + w, y + h) & page.rect
            one = pymupdf.open()
            one.insert_pdf(doc, from_page=i, to_page=i)
            one[0].set_cropbox(clip)
            one.save(os.path.join(a.out, f"{stem}_slide{i + 1}.pdf"))
        png = os.path.join(a.out, f"{stem}_slide{i + 1}.png")
        page.get_pixmap(dpi=a.dpi, clip=clip).save(png)
        print(png)


if __name__ == "__main__":
    main()
