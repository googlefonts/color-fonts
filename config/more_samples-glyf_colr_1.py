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

_CROSS_GLYPH = "cross_glyph"


class SampleGlyph(NamedTuple):
    glyph_name: str
    accessor: str
    advance: int
    glyph: Glyph
    colr: Optional[Mapping[str, Any]] = None


def _cpal(color_str, alpha=1.0):
    color = Color.fromstring(color_str, alpha).to_ufo_color()
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
            "centerX": 500,
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
            "Format": ot.PaintFormat.PaintRotateAroundCenter,
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
    t = Transform(dx=-500, dy=-500)  # move to origin
    t = Transform(xx=0.75, yy=0.75).transform(t)
    t = Transform(dx=500, dy=500).transform(t)
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


def _gradient_stops_repeat(first_stop, second_stop, accessor_char):
    glyph_name = f"linear_repeat_{first_stop}_{second_stop}"

    pen = TTGlyphPen(None)
    pen.moveTo((100, 250))
    pen.lineTo((100, 950))
    pen.lineTo((900, 950))
    pen.lineTo((900, 250))
    pen.closePath()

    colr = {
        "Format": ot.PaintFormat.PaintGlyph,
        "Glyph": glyph_name,
        "Paint": {
            "Format": ot.PaintFormat.PaintLinearGradient,
            "ColorLine": {
                "ColorStop": [
                    (first_stop, _cpal("red")),
                    (second_stop, _cpal("blue")),
                ],
                "Extend": ot.ExtendMode.REPEAT,
            },
            "x0": 100,
            "y0": 250,
            "x1": 900,
            "y1": 250,
            "x2": 100,
            "y2": 300,
        },
    }

    return SampleGlyph(
        glyph_name=glyph_name,
        accessor=accessor_char,
        advance=_UPEM,
        glyph=pen.glyph(),
        colr=colr,
    )


def _cross_glyph():

    pen = TTGlyphPen(None)
    pen.moveTo((475, 500))
    pen.lineTo((475, 725))
    pen.lineTo((525, 725))
    pen.lineTo((525, 500))
    pen.lineTo((750, 500))
    pen.lineTo((750, 450))
    pen.lineTo((525, 450))
    pen.lineTo((525, 225))
    pen.lineTo((475, 225))
    pen.lineTo((475, 450))
    pen.lineTo((250, 450))
    pen.lineTo((250, 500))
    pen.endPath()

    return SampleGlyph(
        glyph_name=_CROSS_GLYPH,
        advance=_UPEM,
        glyph=pen.glyph(),
        accessor="+",
    )


def _paint_scale(scale_x, scale_y, center_x, center_y, accessor_char):
    glyph_name = f"scale_{scale_x}_{scale_y}_center_{center_x}_{center_y}"

    pen = TTGlyphPen(None)
    pen.moveTo((0, 0))
    pen.lineTo((0, _UPEM))
    pen.lineTo((_UPEM, _UPEM))
    pen.lineTo((_UPEM, 0))
    pen.closePath()

    glyph_paint = {
        "Paint": {
            "Format": ot.PaintFormat.PaintGlyph,
            "Glyph": _CROSS_GLYPH,
            "Paint": {
                "Format": ot.PaintFormat.PaintSolid,
                "Color": _cpal("orange", 0.7),
            },
        },
    }

    if center_x or center_y:
        if scale_x != scale_y:
            scaled_colr = {
                "Format": ot.PaintFormat.PaintScaleAroundCenter,
                "scaleX": scale_x,
                "scaleY": scale_y,
                "centerX": center_x,
                "centerY": center_y,
            }
        else:
            scaled_colr = {
                "Format": ot.PaintFormat.PaintScaleUniformAroundCenter,
                "scale": scale_x,
                "centerX": center_x,
                "centerY": center_y,
            }
    else:
        if scale_x != scale_y:
            scaled_colr = {
                "Format": ot.PaintFormat.PaintScale,
                "scaleX": scale_x,
                "scaleY": scale_y,
            }
        else:
            scaled_colr = {
                "Format": ot.PaintFormat.PaintScaleUniform,
                "scale": scale_x,
            }

    scaled_colr = {**scaled_colr, **glyph_paint}

    colr = {
        "Format": ot.PaintFormat.PaintComposite,
        "CompositeMode": "DEST_OVER",
        "SourcePaint": scaled_colr,
        "BackdropPaint": {
            "Format": ot.PaintFormat.PaintGlyph,
            "Glyph": _CROSS_GLYPH,
            "Paint": {"Format": ot.PaintFormat.PaintSolid, "Color": _cpal("blue", 0.5)},
        },
    }

    return SampleGlyph(
        glyph_name=glyph_name,
        accessor=accessor_char,
        advance=_UPEM,
        glyph=pen.glyph(),
        colr=colr,
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
        _gradient_stops_repeat(0, 1, "p"),
        _gradient_stops_repeat(0.2, 0.8, "q"),
        _gradient_stops_repeat(0, 1.5, "r"),
        _gradient_stops_repeat(0.5, 1.5, "s"),
        _paint_scale(0.5, 1.5, 500, 475, "t"),
        _paint_scale(1.5, 1.5, 500, 475, "u"),
        _paint_scale(0.5, 1.5, 0, 0, "v"),
        _paint_scale(1.5, 1.5, 0, 0, "w"),
        _paint_scale(0.5, 1.5, _UPEM, _UPEM, "v"),
        _paint_scale(1.5, 1.5, _UPEM, _UPEM, "w"),
        _cross_glyph(),
    ]

    fb = fontBuilder.FontBuilder(_UPEM)
    fb.setupGlyphOrder([g.glyph_name for g in glyphs])
    fb.setupCharacterMap(
        {ord(g.accessor): g.glyph_name for g in glyphs if len(g.accessor) == 1}
    )
    fb.setupGlyf({g.glyph_name: g.glyph for g in glyphs})
    fb.setupHorizontalMetrics({g.glyph_name: (_UPEM, g.glyph.xMin) for g in glyphs})
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
