"""Audit a deck against the figure rules (../style-rules.md) and print a Markdown report.

    python audit_pptx.py deck.pptx [--slides 1,2]

Checks what can be measured: sentences in labels (R1), grey vs colour share (R2), typefaces and
sizes (R3), rounded shapes / radii / line and arrow widths (R4), number of hues (R5), labels that
collide or leave the frame (R6). Judgement calls (is the structure clear?) still need eyes on the
rendered PNG.
"""
import argparse
import colorsys
import re
from collections import Counter

from lxml import etree
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.oxml.ns import qn

import tokens as T

EMU_IN = 914400
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
SERIF = ("times", "cambria", "georgia", "garamond", "palatino", "book antiqua", "baskerville", "charter",
         "libertine", "computer modern", "cmu serif", "latin modern", "stix", "caladea", "songti", "simsun",
         "宋体", "minion", "constantia", "linux libertine", "noto serif", "source serif", "dejavu serif")
SANS = ("inter", "arial", "helvetica", "calibri", "segoe", "roboto", "open sans", "lato", "source sans",
        "sf pro", "pingfang", "yahei", "微软雅黑", "noto sans", "dejavu sans", "avenir", "futura", "gill sans",
        "verdana", "tahoma", "liberation sans", "myriad", "frutiger", "ibm plex sans", "manrope")


def classify(face):
    f = (face or "").lower()
    if any(s in f for s in SERIF):
        return "serif"
    if any(s in f for s in SANS):
        return "sans"
    if "math" in f or "symbol" in f:
        return "symbol"
    return "?"


def theme_fonts(prs):
    """Theme fonts (+mj-lt / +mn-lt) and theme colours (scheme:accent1 -> hex) of the first master."""
    try:
        part = prs.slide_masters[0].part.part_related_by(RT.THEME)
        root = etree.fromstring(part.blob)
        out = {"+mj-lt": root.find(f".//{A}majorFont/{A}latin").get("typeface"),
               "+mn-lt": root.find(f".//{A}minorFont/{A}latin").get("typeface")}
        scheme = root.find(f".//{A}clrScheme")
        for el in scheme if scheme is not None else []:
            name = etree.QName(el).localname
            c = el.find(f"{A}srgbClr")
            sysc = el.find(f"{A}sysClr")
            val = c.get("val") if c is not None else (sysc.get("lastClr") if sysc is not None else None)
            if val:
                out["scheme:" + name] = val.upper()
        for alias, src in (("tx1", "dk1"), ("bg1", "lt1"), ("tx2", "dk2"), ("bg2", "lt2")):
            if "scheme:" + src in out:
                out["scheme:" + alias] = out["scheme:" + src]
        return out
    except Exception:
        return {}


def walk(shapes):
    for s in shapes:
        yield s
        if s.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from walk(s.shapes)


def _clr(parent):
    """Colour inside a fill-bearing element: hex, 'scheme:x', 'gradient' or None."""
    if parent is None:
        return None
    sf = parent.find(f"{A}solidFill")
    if sf is not None:
        c = sf.find(f"{A}srgbClr")
        if c is not None:
            return c.get("val").upper()
        c = sf.find(f"{A}schemeClr")
        if c is not None:
            return "scheme:" + c.get("val")
        return "other"
    if parent.find(f"{A}gradFill") is not None:
        return "gradient"
    return None


def shape_info(s, theme):
    el = s._element
    sppr = el.find(qn("p:spPr"))
    style = el.find(qn("p:style"))
    info = {"name": s.name, "geom": None, "adj": None, "fill": None, "line": None, "lw": None, "dash": None,
            "heads": (), "glow": False, "runs": [], "text": "", "kind": s.shape_type,
            "box": (s.left or 0, s.top or 0, s.width or 0, s.height or 0)}
    if sppr is not None:
        g = sppr.find(f"{A}prstGeom")
        if g is not None:
            info["geom"] = g.get("prst")
            gd = g.find(f"{A}avLst/{A}gd")
            if gd is not None and gd.get("fmla", "").startswith("val "):
                info["adj"] = int(gd.get("fmla")[4:]) / 100000
        elif sppr.find(f"{A}custGeom") is not None:
            info["geom"] = "custom"
        info["fill"] = _clr(sppr)
        if info["fill"] is None and sppr.find(f"{A}noFill") is None and style is not None:
            ref = style.find(f"{A}fillRef")
            if ref is not None and ref.get("idx", "0") != "0":
                info["fill"] = "theme"
        ln = sppr.find(f"{A}ln")
        if ln is not None and ln.find(f"{A}noFill") is None:
            info["line"] = _clr(ln) or ("theme" if style is not None else None)
            info["lw"] = round(int(ln.get("w", 9525)) / 12700, 2)
            d = ln.find(f"{A}prstDash")
            info["dash"] = d.get("val") if d is not None else None
            info["heads"] = tuple((h.get("type") or "") for h in (ln.find(f"{A}headEnd"), ln.find(f"{A}tailEnd"))
                                  if h is not None and h.get("type") not in (None, "none"))
        elif ln is None and style is not None:
            ref = style.find(f"{A}lnRef")
            if ref is not None and ref.get("idx", "0") != "0":
                info["line"], info["lw"] = "theme", 0.75
        eff = sppr.find(f"{A}effectLst")
        info["glow"] = eff is not None and eff.find(f"{A}glow") is not None
    if getattr(s, "has_text_frame", False) and s.has_text_frame:
        info["text"] = s.text_frame.text.strip()
        for p in s.text_frame.paragraphs:
            ppr = p._p.find(f"{A}pPr")
            dflt = ppr.find(f"{A}defRPr") if ppr is not None else None
            for r in p.runs:
                if not r.text.strip():
                    continue
                rpr = r._r.find(f"{A}rPr")
                face, sz, base = None, None, 0
                for src in (rpr, dflt):
                    if src is None:
                        continue
                    lat = src.find(f"{A}latin")
                    face = face or (lat.get("typeface") if lat is not None else None)
                    sz = sz or (int(src.get("sz")) / 100 if src.get("sz") else None)
                if rpr is not None and rpr.get("baseline"):
                    base = int(rpr.get("baseline"))
                if face is None or face.startswith("+"):
                    face = theme.get(face or "+mn-lt", "theme") + " (theme)"
                col = _clr(rpr) if rpr is not None else None
                info["runs"].append({"face": face, "size": sz or 18.0, "baseline": base, "color": col, "text": r.text})
    return info


def hue_family(hex_):
    """Hue name of a colour, or None for neutrals. Uses HLS saturation so pale tints still count."""
    if not hex_ or len(hex_) != 6:
        return None
    r, g, b = (int(hex_[i:i + 2], 16) / 255 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    if max(r, g, b) - min(r, g, b) < 0.03 or s < 0.25:
        return None  # grey / black / white
    names = ["red", "orange", "yellow", "lime", "green", "teal", "cyan", "azure", "blue", "violet", "purple", "pink"]
    return names[int(((h * 360 + 15) % 360) // 30)]


def sentence_like(t):
    t = " ".join(t.split())
    words = re.findall(r"[A-Za-z一-鿿]+", t)
    return len(words) > 6 or bool(re.search(r"[a-z]\.\s+[A-Za-z]", t)) or (t.endswith(".") and not re.search(r"\d\.$", t))


def audit_slide(slide, idx, theme):
    shapes = [shape_info(s, theme) for s in walk(slide.shapes)]
    for x in shapes:  # theme colours -> hex
        for k in ("fill", "line"):
            if isinstance(x[k], str) and x[k].startswith("scheme:"):
                x[k] = theme.get(x[k], x[k])
        for r in x["runs"]:
            if isinstance(r["color"], str) and r["color"].startswith("scheme:"):
                r["color"] = theme.get(r["color"], r["color"])
    frame = next((x for x in shapes if x["name"].startswith("FRAME")), None)
    shapes = [x for x in shapes if not x["name"].startswith("FRAME")]
    rows, facts = [], {}
    facts["frame"] = frame["name"] if frame else "（无 FRAME：整页即图）"
    facts["pictures"] = sum(1 for x in shapes if x["kind"] == MSO_SHAPE_TYPE.PICTURE)
    if all(x["kind"] == MSO_SHAPE_TYPE.PICTURE for x in shapes):
        rows.append(("全部规则", "—", "整页只有图片（如 matplotlib 导出），矢量审计不适用：看渲染 PNG，并检查出图脚本是否用 plot_style.py"))
        return rows, facts

    # R1 sentences
    texts = [x for x in shapes if x["text"]]
    bad = [x["text"].replace("\n", " ")[:70] for x in texts if sentence_like(x["text"])]
    rows.append(("R1 结构不是句子", "⚠️" if bad else "✅",
                 f"{len(bad)} 个文本框像句子：" + "；".join(f"「{b}」" for b in bad[:4]) if bad else f"{len(texts)} 个文本框都是短标签"))

    # R2 grey base vs colour
    mods = [x for x in shapes if x["geom"] not in (None, "line", "ellipse", "custom") and x["fill"]
            and len(x["fill"]) == 6 and x["fill"] != "FFFFFF" and x["box"][2] > 0.25 * EMU_IN]
    area = lambda x: x["box"][2] * x["box"][3]
    col_area = sum(area(x) for x in mods if hue_family(x["fill"]))
    tot = sum(area(x) for x in mods) or 1
    share = col_area / tot
    emph = sum(1 for x in shapes if x["glow"] or (x["lw"] or 0) >= T.LINE["emphasis"] - 0.01)
    r2_bad = share > 0.5 or (len(mods) >= 3 and emph == 0)
    rows.append(("R2 创新点高亮", "⚠️" if r2_bad else "✅",
                 f"彩色模块占模块面积 {share:.0%}（基础组件应为灰，宜 ≤50%）；强调描边/glow 元素 {emph} 个" +
                 ("（没有强调的创新模块）" if len(mods) >= 3 and emph == 0 else "")))

    # R3 fonts and sizes
    runs = [r for x in shapes for r in x["runs"]]
    faces = Counter(r["face"] for r in runs)
    classes = {classify(f.replace(" (theme)", "")) for f in faces}
    sizes = sorted({r["size"] for r in runs if not r["baseline"]})
    non_inter = [f for f in faces if not f.lower().startswith("inter")]
    tiers = set(T.SIZE.values())
    st = "❌" if {"serif", "sans"} <= classes or len(sizes) > 3 else ("⚠️" if non_inter or set(sizes) - tiers else "✅")
    rows.append(("R3 字体统一", st, "字体 " + "，".join(f"{f}×{n}" for f, n in faces.most_common()) +
                 f"；字号 {', '.join(f'{s:g}' for s in sizes)} pt" + ("；混用衬线与无衬线" if {"serif", "sans"} <= classes else "")))

    # R4 shapes and lines
    sharp = [x for x in shapes if x["geom"] in ("rect", "cube", "trapezoid") and (x["fill"] or x["line"])]
    radii = sorted({round((x["adj"] if x["adj"] is not None else 0.16667) * min(x["box"][2], x["box"][3]) / EMU_IN, 2)
                    for x in shapes if x["geom"] == "roundRect" and x["box"][2] > EMU_IN * 0.3})
    borders = sorted({x["lw"] for x in shapes if x["geom"] in ("roundRect", "rect", "ellipse") and x["lw"]})
    arrows = [x for x in shapes if x["heads"]]
    aw = sorted({x["lw"] for x in arrows})
    heads = sorted({h for x in arrows for h in x["heads"]})
    dashes = sorted({x["dash"] for x in shapes if x["dash"]})
    issues = []
    if sharp:
        issues.append(f"{len(sharp)} 个非圆角模块（{', '.join(sorted({x['geom'] for x in sharp}))}）")
    if len(radii) > 1:
        issues.append(f"圆角半径 {len(radii)} 种 {radii} in")
    if len(borders) > 2:
        issues.append(f"边框粗细 {len(borders)} 种 {borders} pt")
    if len(aw) > 1:
        issues.append(f"箭头粗细 {len(aw)} 种 {aw} pt")
    if len(heads) > 1:
        issues.append(f"箭头样式 {heads}")
    if len(dashes) > 1:
        issues.append(f"虚线样式 {dashes}")
    rows.append(("R4 形状/线条统一", "⚠️" if issues else "✅",
                 "；".join(issues) if issues else f"圆角 {radii or '—'} in；边框 {borders or '—'} pt；箭头 {aw or '—'} pt {heads or ''}"))

    # R5 hues
    colors = [x["fill"] for x in shapes] + [x["line"] for x in shapes] + [r["color"] for r in runs]
    fam = Counter(hue_family(c) for c in colors if c and len(c) == 6)
    fam.pop(None, None)
    rows.append(("R5 色彩克制（2–4 种）", "❌" if len(fam) > 4 else "✅",
                 f"{len(fam)} 个色相：" + "，".join(f"{k}×{v}" for k, v in fam.most_common()) if fam else "只有灰阶"))

    # R6 collisions / out of frame
    labels = [x for x in shapes if x["text"]]
    clash = []
    for i in range(len(labels)):
        for j in range(i + 1, len(labels)):
            a, b = labels[i]["box"], labels[j]["box"]
            ix = min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0])
            iy = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1])
            if ix > 0.02 * EMU_IN and iy > 0.02 * EMU_IN:
                inside = lambda p, q: p[0] >= q[0] and p[1] >= q[1] and p[0] + p[2] <= q[0] + q[2] and p[1] + p[3] <= q[1] + q[3]
                if not (inside(a, b) or inside(b, a)):
                    clash.append(f"「{labels[i]['text'][:18]}」×「{labels[j]['text'][:18]}」")
    out = []
    if frame:
        fx, fy, fw, fh = frame["box"]
        out = [x["name"] for x in shapes if x["box"][2] and (x["box"][0] < fx - 1 or x["box"][1] < fy - 1 or
               x["box"][0] + x["box"][2] > fx + fw + 1 or x["box"][1] + x["box"][3] > fy + fh + 1)]
    rows.append(("R6 留白/不重叠", "⚠️" if clash or out else "✅",
                 ("文本框部分重叠：" + "；".join(clash[:4]) if clash else "无文本重叠") + (f"；{len(out)} 个元素超出 FRAME" if out else "")))

    return rows, facts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("--slides")
    a = ap.parse_args()
    prs = Presentation(a.deck)
    theme = theme_fonts(prs)
    pick = {int(s) for s in a.slides.split(",")} if a.slides else None
    print(f"# 风格审计：{a.deck.split('/')[-1]}\n")
    fonts = {k: v for k, v in theme.items() if k.startswith("+")}
    print(f"幻灯片 {prs.slide_width / EMU_IN:.2f} × {prs.slide_height / EMU_IN:.2f} in；主题字体 {fonts or '—'}\n")
    for i, slide in enumerate(prs.slides, 1):
        if pick and i not in pick:
            continue
        rows, facts = audit_slide(slide, i, theme)
        print(f"## 第 {i} 页 · {facts['frame']} · 图片 {facts['pictures']} 张\n")
        print("| 规则 | 结果 | 细节 |\n|---|---|---|")
        for r in rows:
            print(f"| {r[0]} | {r[1]} | {r[2]} |")
        print()


if __name__ == "__main__":
    main()
