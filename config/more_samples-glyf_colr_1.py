"""Compile samples that are infeasible or difficult by svg compilation.
"""

import datetime
from pathlib import Path
from fontTools import fontBuilder
from fontTools import ttLib
from fontTools.colorLib import builder as colorBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.tables._g_l_y_f import Glyph
import sys
from typing import Any, Mapping, NamedTuple, Optional
from fontTools.ttLib.tables import otTables as ot
from nanoemoji.colors import css_colors, Color
from fontTools.misc.transform import Transform

_UPEM = 1000
_ASCENT = 950
_DESCENT = 250
_FAMILY = "More COLR v1 Samples"
_STYLE = "Regular"
_PALETTE = {}  # <3 mutable globals


class SampleGlyph(NamedTuple):
    glyph_name: str
    accessor: str
    advance: int
    glyph: Glyph
    colr: Optional[Mapping[str, Any]] = None


def _cpal(color_str):
    color = Color.fromstring(color_str).to_ufo_color()
    if color not in _PALETTE:
        _PALETTE[color] = len(_PALETTE)
    return _PALETTE[color]


def _sample_sweep():
    glyph_name = "sweep"

    pen = TTGlyphPen(None)
    pen.moveTo((100, 500))
    pen.qCurveTo((500, 1000), (900, 500))
    pen.qCurveTo((500, 0), (100, 500))
    pen.closePath()

    colr = {
        "Format": ot.PaintFormat.PaintGlyph,
        "Glyph": glyph_name,
        "Paint": {
            "Format": ot.PaintFormat.PaintSweepGradient,
            "ColorLine": {
                "ColorStop": [
                    (0.0, _cpal("red")),
                    (0.5, _cpal("yellow")),
                    (1.0, _cpal("red")),
                ]
            },
            "centerX": 400,  # TODO: looks off-center at 500
            "centerY": 500,
            "startAngle": 0,
            "endAngle": 360,
        },
    }

    return SampleGlyph(
        glyph_name=glyph_name, accessor="c", advance=_UPEM, glyph=pen.glyph(), colr=colr
    )


def _sample_colr_glyph():
    glyph_name = "transformed_sweep"
    # Paint the sweep shifted and rotated
    colr = {
        "Format": ot.PaintFormat.PaintTranslate,
        "dx": 250,
        "dy": 0,
        "Paint": {
            "Format": ot.PaintFormat.PaintRotate,
            "centerX": _UPEM / 2,
            "centerY": _UPEM / 2,
            "angle": 60,
            "Paint": {
                "Format": ot.PaintFormat.PaintColrGlyph,
                "Glyph": "sweep",
            },
        },
    }

    pen = TTGlyphPen(None)
    pen.moveTo((0, 0))
    pen.lineTo((_UPEM, _UPEM))
    pen.endPath()

    return SampleGlyph(
        glyph_name=glyph_name, accessor="t", advance=_UPEM, glyph=pen.glyph(), colr=colr
    )


def _sample_composite_colr_glyph():
    glyph_name = "composite_colr_glyph"
    # Scale down the sweep and use it to cut a hole in the sweep
    # Transforms combine f(g(x)); build up backwards
    t = Transform(dx=-400, dy=-500)  # move to origin
    print(t)
    t = Transform(xx=0.75, yy=0.75).transform(t)
    print(t)
    t = Transform(dx=400, dy=500).transform(t)
    print(t)
    t = tuple(t)

    colr = {
        "Format": ot.PaintFormat.PaintComposite,
        "CompositeMode": "SRC_OUT",
        "SourcePaint": {
            "Format": ot.PaintFormat.PaintColrGlyph,
            "Glyph": "sweep",
        },
        "BackdropPaint": {
            "Format": ot.PaintFormat.PaintTransform,
            "Paint": {
                "Format": ot.PaintFormat.PaintColrGlyph,
                "Glyph": "sweep",
            },
            "Transform": t,
        },
    }

    pen = TTGlyphPen(None)
    pen.moveTo((0, 0))
    pen.lineTo((_UPEM, _UPEM))
    pen.endPath()

    return SampleGlyph(
        glyph_name=glyph_name, accessor="o", advance=_UPEM, glyph=pen.glyph(), colr=colr
    )


def main():
    assert len(sys.argv) == 2
    build_dir = Path(sys.argv[1])
    build_dir.mkdir(exist_ok=True)

    out_file = (build_dir / _FAMILY.replace(" ", "")).with_suffix(".ttf")

    version = datetime.datetime.now().isoformat()
    names = {
        "familyName": _FAMILY,
        "styleName": _STYLE,
        "uniqueFontIdentifier": " ".join((_FAMILY, version)),
        "fullName": " ".join((_FAMILY, _STYLE)),
        "version": version,
        "psName": "-".join((_FAMILY.replace(" ", ""), _STYLE)),
    }

    glyphs = [
        SampleGlyph(glyph_name=".notdef", accessor="", advance=600, glyph=Glyph()),
        SampleGlyph(glyph_name=".null", accessor="", advance=0, glyph=Glyph()),
        _sample_sweep(),
        _sample_colr_glyph(),
        _sample_composite_colr_glyph(),
    ]

    fb = fontBuilder.FontBuilder(_UPEM)
    fb.setupGlyphOrder([g.glyph_name for g in glyphs])
    fb.setupCharacterMap(
        {ord(g.accessor): g.glyph_name for g in glyphs if len(g.accessor) == 1}
    )
    fb.setupGlyf({g.glyph_name: g.glyph for g in glyphs})
    fb.setupHorizontalMetrics({g.glyph_name: (_UPEM, 0) for g in glyphs})
    fb.setupHorizontalHeader(ascent=_ASCENT, descent=-_DESCENT)
    fb.setupOS2(sTypoAscender=_ASCENT, usWinAscent=_ASCENT, usWinDescent=_DESCENT)
    fb.setupNameTable(names)
    fb.setupPost()

    fb.font["head"].xMin = 0
    fb.font["head"].yMin = -_DESCENT
    fb.font["head"].xMax = _UPEM
    fb.font["head"].yMax = _ASCENT

    fb.font["OS/2"].fsType = 0
    fb.font["OS/2"].version = 4
    fb.font["OS/2"].fsSelection |= 1 << 7

    fb.font["hhea"].advanceWidthMax = _UPEM

    fb.font["COLR"] = colorBuilder.buildCOLR(
        {g.glyph_name: g.colr for g in glyphs if g.colr}
    )
    fb.font["CPAL"] = colorBuilder.buildCPAL([list(_PALETTE)])

    fb.save(out_file)
    print(f"Wrote {out_file}")


if __name__ == "__main__":
    main()
