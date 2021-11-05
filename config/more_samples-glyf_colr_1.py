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
from typing import Any, Mapping, NamedTuple, Optional, Tuple
from fontTools.ttLib.tables import otTables as ot
from nanoemoji.colors import css_colors, Color
from fontTools.misc.transform import Transform
from string import ascii_letters, digits

_UPEM = 1000
_ASCENT = 950
_DESCENT = 250
_FAMILY = "More COLR v1 Samples"
_STYLE = "Regular"
_PALETTE = {}  # <3 mutable globals

_CROSS_GLYPH = "cross_glyph"
_UPEM_BOX_GLYPH = "upem_box_glyph"


class SampleGlyph(NamedTuple):
    glyph_name: str
    accessor: str
    advance: int
    glyph: Glyph
    clip_box: Optional[Tuple[float, float, float, float]] = None
    colr: Optional[Mapping[str, Any]] = None


def _cpal(color_str, alpha=1.0):
    color = Color.fromstring(color_str).to_ufo_color()
    if color not in _PALETTE:
        _PALETTE[color] = len(_PALETTE)
    return (_PALETTE[color], alpha)


def _sample_sweep(accessor):
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
                    (0.0, *_cpal("red")),
                    (0.5, *_cpal("yellow")),
                    (1.0, *_cpal("red")),
                ]
            },
            "centerX": 500,
            "centerY": 500,
            "startAngle": -360,
            "endAngle": 0,
        },
    }

    return SampleGlyph(
        glyph_name=glyph_name,
        accessor=accessor,
        advance=_UPEM,
        glyph=pen.glyph(),
        clip_box=(100, 0, 900, 1000),
        colr=colr,
    )


def _sample_colr_glyph(accessor):
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

    return SampleGlyph(
        glyph_name=glyph_name,
        accessor=accessor,
        advance=_UPEM,
        glyph=_upem_box_pen().glyph(),
        clip_box=(0, 0, _UPEM, _UPEM),
        colr=colr,
    )


def _sample_composite_colr_glyph(accessor):
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

    return SampleGlyph(
        glyph_name=glyph_name,
        advance=_UPEM,
        accessor=accessor,
        glyph=_upem_box_pen().glyph(),
        colr=colr,
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
                    (first_stop, *_cpal("red")),
                    (second_stop, *_cpal("blue")),
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
        clip_box=(100, 250, 900, 950),
        colr=colr,
    )


def _cross_glyph():

    pen = TTGlyphPen(None)
    pen.moveTo((475, 525))
    pen.lineTo((475, 750))
    pen.lineTo((525, 750))
    pen.lineTo((525, 525))
    pen.lineTo((750, 525))
    pen.lineTo((750, 475))
    pen.lineTo((525, 475))
    pen.lineTo((525, 250))
    pen.lineTo((475, 250))
    pen.lineTo((475, 475))
    pen.lineTo((250, 475))
    pen.lineTo((250, 525))
    pen.endPath()

    return SampleGlyph(
        glyph_name=_CROSS_GLYPH,
        advance=_UPEM,
        glyph=pen.glyph(),
        accessor="+",
    )


def _upem_box_pen():
    pen = TTGlyphPen(None)
    pen.moveTo((0, 0))
    pen.lineTo((0, _UPEM))
    pen.lineTo((_UPEM, _UPEM))
    pen.lineTo((_UPEM, 0))
    pen.closePath()

    return pen


def _upem_box_glyph():
    return SampleGlyph(
        glyph_name=_UPEM_BOX_GLYPH,
        advance=_UPEM,
        glyph=_upem_box_pen().glyph(),
        accessor="▀",
    )


def _paint_scale(scale_x, scale_y, center_x, center_y, accessor_char):
    glyph_name = f"scale_{scale_x}_{scale_y}_center_{center_x}_{center_y}"

    color_orange = _cpal("orange", 0.7)
    glyph_paint = {
        "Paint": {
            "Format": ot.PaintFormat.PaintGlyph,
            "Glyph": _CROSS_GLYPH,
            "Paint": {
                "Format": ot.PaintFormat.PaintSolid,
                "PaletteIndex": color_orange[0],
                "Alpha": color_orange[1],
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

    scaled_colr.update(glyph_paint)

    color_blue = _cpal("blue", 0.5)

    colr = {
        "Format": ot.PaintFormat.PaintComposite,
        "CompositeMode": "DEST_OVER",
        "SourcePaint": scaled_colr,
        "BackdropPaint": {
            "Format": ot.PaintFormat.PaintGlyph,
            "Glyph": _CROSS_GLYPH,
            "Paint": {
                "Format": ot.PaintFormat.PaintSolid,
                "PaletteIndex": color_blue[0],
                "Alpha": color_blue[1],
            },
        },
    }

    return SampleGlyph(
        glyph_name=glyph_name,
        accessor=accessor_char,
        advance=_UPEM,
        glyph=_upem_box_pen().glyph(),
        colr=colr,
    )


def _extend_modes(gradient_format, extend_mode, accessor_char):

    format_map = {
        "linear": ot.PaintFormat.PaintLinearGradient,
        "radial": ot.PaintFormat.PaintRadialGradient,
    }

    if gradient_format not in format_map:
        return None

    selected_format = format_map[gradient_format]

    extend_mode_map = {
        "reflect": ot.ExtendMode.REFLECT,
        "repeat": ot.ExtendMode.REPEAT,
        "pad": ot.ExtendMode.PAD,
    }

    if extend_mode not in extend_mode_map:
        return None

    coordinates = {
        ot.PaintFormat.PaintLinearGradient: {
            "x0": 0,
            "y0": 1024,
            "x1": 307,
            "y1": 1024,
            "x2": 0,
            "y2": 717,
        },
        ot.PaintFormat.PaintRadialGradient: {
            "x0": 166,
            "y0": 768,
            "r0": 0,
            "x1": 166,
            "y1": 768,
            "r1": 256,
        },
    }

    glyph_name = f"{gradient_format}_gradient_extend_mode_{extend_mode}"

    colr = {
        "Format": ot.PaintFormat.PaintGlyph,
        "Glyph": _UPEM_BOX_GLYPH,
        "Paint": {
            "Format": selected_format,
            "ColorLine": {
                "ColorStop": [
                    (0.0, *_cpal("green")),
                    (0.5, *_cpal("white")),
                    (1.0, *_cpal("red")),
                ],
                "Extend": extend_mode_map[extend_mode],
            },
            **coordinates[selected_format],
        },
    }

    return SampleGlyph(
        glyph_name=glyph_name,
        accessor=accessor_char,
        glyph=_upem_box_pen().glyph(),
        advance=_UPEM,
        clip_box=(0, 0, _UPEM, _UPEM),
        colr=colr,
    )


def _paint_rotate(angle, center_x, center_y, accessor_char):
    glyph_name = f"rotate_{angle}_center_{center_x}_{center_y}"

    color_orange = _cpal("orange", 0.7)

    glyph_paint = {
        "Paint": {
            "Format": ot.PaintFormat.PaintGlyph,
            "Glyph": _CROSS_GLYPH,
            "Paint": {
                "Format": ot.PaintFormat.PaintSolid,
                "PaletteIndex": color_orange[0],
                "Alpha": color_orange[1],
            },
        },
    }

    if center_x or center_y:
        rotated_colr = {
            "Format": ot.PaintFormat.PaintRotateAroundCenter,
            "centerX": center_x,
            "centerY": center_y,
            "angle": angle,
        }
    else:
        rotated_colr = {"Format": ot.PaintFormat.PaintRotate, "angle": angle}

    rotated_colr.update(glyph_paint)

    color_blue = _cpal("blue", 0.5)

    colr = {
        "Format": ot.PaintFormat.PaintComposite,
        "CompositeMode": "DEST_OVER",
        "SourcePaint": rotated_colr,
        "BackdropPaint": {
            "Format": ot.PaintFormat.PaintGlyph,
            "Glyph": _CROSS_GLYPH,
            "Paint": {
                "Format": ot.PaintFormat.PaintSolid,
                "PaletteIndex": color_blue[0],
                "Alpha": color_blue[1],
            },
        },
    }

    return SampleGlyph(
        glyph_name=glyph_name,
        accessor=accessor_char,
        advance=_UPEM,
        glyph=_upem_box_pen().glyph(),
        colr=colr,
    )


def _paint_skew(x_skew_angle, y_skew_angle, center_x, center_y, accessor_char):
    glyph_name = f"skew_{x_skew_angle}_{y_skew_angle}_center_{center_x}_{center_y}"

    color_orange = _cpal("orange", 0.7)

    glyph_paint = {
        "Paint": {
            "Format": ot.PaintFormat.PaintGlyph,
            "Glyph": _CROSS_GLYPH,
            "Paint": {
                "Format": ot.PaintFormat.PaintSolid,
                "PaletteIndex": color_orange[0],
                "Alpha": color_orange[1],
            },
        },
    }

    skewed_colr = {
        "xSkewAngle": x_skew_angle,
        "ySkewAngle": y_skew_angle,
    }

    if center_x or center_y:
        skewed_colr["Format"] = ot.PaintFormat.PaintSkewAroundCenter
        skewed_colr["centerX"] = center_x
        skewed_colr["centerY"] = center_y

    else:
        skewed_colr["Format"] = ot.PaintFormat.PaintSkew

    skewed_colr = {**skewed_colr, **glyph_paint}

    color_blue = _cpal("blue", 0.5)

    colr = {
        "Format": ot.PaintFormat.PaintComposite,
        "CompositeMode": "DEST_OVER",
        "SourcePaint": skewed_colr,
        "BackdropPaint": {
            "Format": ot.PaintFormat.PaintGlyph,
            "Glyph": _CROSS_GLYPH,
            "Paint": {
                "Format": ot.PaintFormat.PaintSolid,
                "PaletteIndex": color_blue[0],
                "Alpha": color_blue[1],
            },
        },
    }

    return SampleGlyph(
        glyph_name=glyph_name,
        accessor=accessor_char,
        advance=_UPEM,
        glyph=_upem_box_pen().glyph(),
        colr=colr,
    )


def _paint_transform(xx, xy, yx, yy, dx, dy, accessor):
    glyph_name = f"transform_matrix_{xx}_{xy}_{yx}_{yy}_{dx}_{dy}"

    t = (xx, xy, yx, yy, dx, dy)
    color_orange = _cpal("orange", 0.7)

    transformed_colr = {
        "Format": ot.PaintFormat.PaintTransform,
        "Paint": {
            "Format": ot.PaintFormat.PaintGlyph,
            "Glyph": _CROSS_GLYPH,
            "Paint": {
                "Format": ot.PaintFormat.PaintSolid,
                "PaletteIndex": color_orange[0],
                "Alpha": color_orange[1],
            },
        },
        "Transform": t,
    }

    color_blue = _cpal("blue", 0.5)

    colr = {
        "Format": ot.PaintFormat.PaintComposite,
        "CompositeMode": "DEST_OVER",
        "SourcePaint": transformed_colr,
        "BackdropPaint": {
            "Format": ot.PaintFormat.PaintGlyph,
            "Glyph": _CROSS_GLYPH,
            "Paint": {
                "Format": ot.PaintFormat.PaintSolid,
                "PaletteIndex": color_blue[0],
                "Alpha": color_blue[1],
            },
        },
    }

    return SampleGlyph(
        glyph_name=glyph_name,
        advance=_UPEM,
        accessor=accessor,
        glyph=_upem_box_pen().glyph(),
        colr=colr,
    )


clip_position_map = {
    "top_left": (0, _UPEM / 2, _UPEM / 2, _UPEM),
    "bottom_left": (0, 0, _UPEM / 2, _UPEM / 2),
    "bottom_right": (_UPEM / 2, 0, _UPEM, _UPEM / 2),
    "top_right": (_UPEM / 2, _UPEM / 2, _UPEM, _UPEM),
    "center": (_UPEM / 4, _UPEM / 4, _UPEM / 4 * 3, _UPEM / 4 * 3),
}


# A composited glyph which shades the intended clip box without
# defining a clip box for itself. Useful in testing ClipBoxes to see whether
# only the shaded portion is drawn or other parts of the glyph peek out.
def _clip_shade_glyph(position, accessor_char):
    if not position in clip_position_map:
        return None

    (x_min, y_min, x_max, y_max) = clip_position_map[position]

    clip_pen = TTGlyphPen(None)
    clip_pen.moveTo((x_min, y_min))
    clip_pen.lineTo((x_min, y_max))
    clip_pen.lineTo((x_max, y_max))
    clip_pen.lineTo((x_max, y_min))
    clip_pen.closePath()

    return SampleGlyph(
        glyph_name=f"clip_shade_{position}",
        advance=_UPEM,
        glyph=clip_pen.glyph(),
        accessor=accessor_char,
    )


# A clone (PaintColrGlyph) of the radial_gradient_extend_mode_reflect glyph,
# clipped with a smaller clip box in order to test nested clip boxes.
def _inset_clipped_radial_reflect(accessor_char):
    colr = {
        "Format": ot.PaintFormat.PaintColrGlyph,
        "Glyph": "radial_gradient_extend_mode_reflect",
    }

    return SampleGlyph(
        glyph_name="inset_clipped_radial_reflect",
        accessor=accessor_char,
        glyph=_upem_box_pen().glyph(),
        advance=_UPEM,
        clip_box=(_UPEM / 10, _UPEM / 10, _UPEM - _UPEM / 10, _UPEM - _UPEM / 10),
        colr=colr,
    )


def _clip_box(position, accessor_char):

    other_glyph_colr = {
        "Format": ot.PaintFormat.PaintColrGlyph,
        "Glyph": "inset_clipped_radial_reflect",
    }

    shade_color = _cpal("gray", 0.4)

    colr = {
        "Format": ot.PaintFormat.PaintComposite,
        "CompositeMode": "SRC_OVER",
        "SourcePaint": {
            "Format": ot.PaintFormat.PaintGlyph,
            "Glyph": f"clip_shade_{position}",
            "Paint": {
                "Format": ot.PaintFormat.PaintSolid,
                "PaletteIndex": shade_color[0],
                "Alpha": shade_color[1],
            },
        },
        "BackdropPaint": other_glyph_colr,
    }

    (x_min, y_min, x_max, y_max) = clip_position_map[position]

    return SampleGlyph(
        glyph_name=f"clip_box_{position}",
        accessor=accessor_char,
        advance=_UPEM,
        glyph=_upem_box_pen().glyph(),
        clip_box=(x_min, y_min, x_max, y_max),
        colr=colr,
    )


def _composite(composite_mode, accessor_char):

    color_black = _cpal("black", 1)
    color_blue = _cpal("#68c7e8", 1)
    color_yellow = _cpal("#ffdc01", 1)

    colr = {
        "Format": ot.PaintFormat.PaintColrLayers,
        "Layers": [
            {
                "Format": ot.PaintFormat.PaintGlyph,
                "Glyph": _CROSS_GLYPH,
                "Paint": {
                    "Format": ot.PaintFormat.PaintSolid,
                    "PaletteIndex": color_black[0],
                    "Alpha": color_black[1],
                },
            },
            {
                "Format": ot.PaintFormat.PaintComposite,
                "CompositeMode": composite_mode,
                "SourcePaint": {
                    "Format": ot.PaintFormat.PaintScaleUniformAroundCenter,
                    "centerX": _UPEM / 3 * 2,
                    "centerY": _UPEM / 3,
                    "scale": 1 / 2,
                    "Paint": {
                        "Format": ot.PaintFormat.PaintGlyph,
                        "Glyph": _UPEM_BOX_GLYPH,
                        "Paint": {
                            "Format": ot.PaintFormat.PaintSolid,
                            "PaletteIndex": color_blue[0],
                            "Alpha": color_blue[1],
                        },
                    },
                },
                "BackdropPaint": {
                    "Format": ot.PaintFormat.PaintScaleUniformAroundCenter,
                    "centerX": _UPEM / 3,
                    "centerY": _UPEM / 3 * 2,
                    "scale": 1 / 2,
                    "Paint": {
                        "Format": ot.PaintFormat.PaintGlyph,
                        "Glyph": _UPEM_BOX_GLYPH,
                        "Paint": {
                            "Format": ot.PaintFormat.PaintSolid,
                            "PaletteIndex": color_yellow[0],
                            "Alpha": color_yellow[1],
                        },
                    },
                },
            },
        ],
    }

    return SampleGlyph(
        glyph_name=f"composite_{composite_mode}",
        accessor=accessor_char,
        advance=_UPEM,
        glyph=_upem_box_pen().glyph(),
        clip_box=(0, 0, _UPEM, _UPEM),
        colr=colr,
    )


def _foreground_color(fill_type, accessor_char):

    fill_type_map = {
        "solid": {
            "Format": ot.PaintFormat.PaintSolid,
            "PaletteIndex": 0xFFFF,
            "Alpha": 1,
        },
        "linear": {
            "Format": ot.PaintFormat.PaintLinearGradient,
            "ColorLine": {
                "ColorStop": [
                    (0.0, *_cpal("white")),
                    (0.5, 0xFFFF, 1),
                    (1.0, *_cpal("white")),
                ]
            },
            "x0": 100,
            "y0": 250,
            "x1": 900,
            "y1": 250,
            "x2": 100,
            "y2": 300,
        },
        "radial": {
            "Format": ot.PaintFormat.PaintRadialGradient,
            "ColorLine": {
                "ColorStop": [
                    (0.0, *_cpal("white")),
                    (0.5, 0xFFFF, 1),
                    (1.0, *_cpal("white")),
                ]
            },
            "x0": 500,
            "y0": 600,
            "r0": 50,
            "x1": 500,
            "y1": 600,
            "r1": 450,
        },
        "sweep": {
            "Format": ot.PaintFormat.PaintSweepGradient,
            "ColorLine": {
                "ColorStop": [
                    (0.0, *_cpal("white")),
                    (0.5, 0xFFFF, 1),
                    (1.0, *_cpal("white")),
                ]
            },
            "centerX": 500,
            "centerY": 600,
            "startAngle": -360,
            "endAngle": 270,
        },
    }

    if not fill_type in fill_type_map:
        return

    glyph_name = f"foreground_color_{fill_type}"

    pen = _upem_box_pen()

    colr = {
        "Format": ot.PaintFormat.PaintGlyph,
        "Glyph": glyph_name,
        "Paint": fill_type_map[fill_type],
    }

    return SampleGlyph(
        glyph_name=glyph_name,
        accessor=accessor_char,
        advance=_UPEM,
        glyph=pen.glyph(),
        clip_box=(100, 250, 900, 950),
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

    access_chars = iter(ascii_letters + digits)
    glyphs = [
        SampleGlyph(glyph_name=".notdef", accessor="", advance=600, glyph=Glyph()),
        SampleGlyph(glyph_name=".null", accessor="", advance=0, glyph=Glyph()),
        _sample_sweep(next(access_chars)),
        _sample_colr_glyph(next(access_chars)),
        _sample_composite_colr_glyph(next(access_chars)),
        _gradient_stops_repeat(0, 1, next(access_chars)),
        _gradient_stops_repeat(0.2, 0.8, next(access_chars)),
        _gradient_stops_repeat(0, 1.5, next(access_chars)),
        _gradient_stops_repeat(0.5, 1.5, next(access_chars)),
        _paint_scale(0.5, 1.5, _UPEM / 2, _UPEM / 2, next(access_chars)),
        _paint_scale(1.5, 1.5, _UPEM / 2, _UPEM / 2, next(access_chars)),
        _paint_scale(0.5, 1.5, 0, 0, next(access_chars)),
        _paint_scale(1.5, 1.5, 0, 0, next(access_chars)),
        _paint_scale(0.5, 1.5, _UPEM, _UPEM, next(access_chars)),
        _paint_scale(1.5, 1.5, _UPEM, _UPEM, next(access_chars)),
        _extend_modes("linear", "pad", next(access_chars)),
        _extend_modes("linear", "repeat", next(access_chars)),
        _extend_modes("linear", "reflect", next(access_chars)),
        _extend_modes("radial", "pad", next(access_chars)),
        _extend_modes("radial", "repeat", next(access_chars)),
        _extend_modes("radial", "reflect", next(access_chars)),
        _paint_rotate(10, 0, 0, next(access_chars)),
        _paint_rotate(-10, _UPEM, _UPEM, next(access_chars)),
        _paint_rotate(25, _UPEM / 2, _UPEM / 2, next(access_chars)),
        _paint_rotate(-15, _UPEM / 2, _UPEM / 2, next(access_chars)),
        _paint_skew(25, 0, 0, 0, next(access_chars)),
        _paint_skew(25, 0, _UPEM / 2, _UPEM / 2, next(access_chars)),
        _paint_skew(0, 15, 0, 0, next(access_chars)),
        _paint_skew(0, 15, _UPEM / 2, _UPEM / 2, next(access_chars)),
        _paint_skew(-10, 20, _UPEM / 2, _UPEM / 2, next(access_chars)),
        _paint_skew(-10, 20, _UPEM, _UPEM, next(access_chars)),
        _paint_transform(1, 0, 0, 1, 125, 125, next(access_chars)),
        _paint_transform(1.5, 0, 0, 1.5, 0, 0, next(access_chars)),
        _paint_transform(
            0.9659, 0.2588, -0.2588, 0.9659, 0, 0, next(access_chars)
        ),  # Rotation 15 degrees counterclockwise
        _paint_transform(
            1.0, 0.0, 0.6, 1.0, -300.0, 0.0, next(access_chars)
        ),  # y-shear around center pivot point
        _clip_box("top_left", next(access_chars)),
        _clip_box("bottom_left", next(access_chars)),
        _clip_box("bottom_right", next(access_chars)),
        _clip_box("top_right", next(access_chars)),
        _clip_box("center", next(access_chars)),
        _composite("DEST_OVER", next(access_chars)),
        _composite("XOR", next(access_chars)),
        _composite("OVERLAY", next(access_chars)),
        _composite("SRC_IN", next(access_chars)),
        _composite("PLUS", next(access_chars)),
        _composite("LIGHTEN", next(access_chars)),
        _composite("MULTIPLY", next(access_chars)),
        _foreground_color("linear", next(access_chars)),
        _foreground_color("radial", next(access_chars)),
        _foreground_color("sweep", next(access_chars)),
        _foreground_color("solid", next(access_chars)),
        _cross_glyph(),
        _upem_box_glyph(),
        _clip_shade_glyph("center", next(access_chars)),
        _clip_shade_glyph("top_left", next(access_chars)),
        _clip_shade_glyph("bottom_left", next(access_chars)),
        _clip_shade_glyph("bottom_right", next(access_chars)),
        _clip_shade_glyph("top_right", next(access_chars)),
        _inset_clipped_radial_reflect(next(access_chars)),
    ]

    fb = fontBuilder.FontBuilder(_UPEM)
    fb.setupGlyphOrder([g.glyph_name for g in glyphs])
    fb.setupCharacterMap(
        {ord(g.accessor): g.glyph_name for g in glyphs if len(g.accessor) == 1}
    )
    fb.setupGlyf({g.glyph_name: g.glyph for g in glyphs if g.glyph})

    def find_xmin(g):
        if g.clip_box:
            return g.clip_box[0]
        if g.glyph:
            return g.glyph.xMin
        return 0

    fb.setupHorizontalMetrics({g.glyph_name: (g.advance, find_xmin(g)) for g in glyphs})
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
        {g.glyph_name: g.colr for g in glyphs if g.colr},
        clipBoxes={g.glyph_name: g.clip_box for g in glyphs if g.clip_box},
    )
    fb.font["CPAL"] = colorBuilder.buildCPAL([list(_PALETTE)])

    fb.save(out_file)
    print(f"Wrote {out_file}")


if __name__ == "__main__":
    main()
