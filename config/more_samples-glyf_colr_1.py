"""Generate a test font consisting of samples that provide wide coverage for
COLRv1 Paint* tables, including PaintVar* tables, including such samples that
are impossible to generate from SVG at this point, for example
PaintSweepGradient tests.
"""

import datetime
from pathlib import Path, PurePath
from fontTools import designspaceLib
from fontTools import fontBuilder
from fontTools import ttLib
from fontTools import varLib
from fontTools.colorLib import builder as colorBuilder
from fontTools.colorLib.builder import ColorPaletteType
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.ttLib.tables._g_l_y_f import Glyph
import sys
from typing import Any, Mapping, NamedTuple, Optional, Tuple, List
from fontTools.ttLib.tables import otTables as ot
from nanoemoji.colors import css_colors, Color
from fontTools.misc.transform import Transform
from string import ascii_letters, digits
from math import sqrt
import json
import argparse
import logging

_UPEM = 1000
_ASCENT = 950
_DESCENT = 250
_FAMILY = "More COLR v1 Samples"
_STYLE = "Regular"
_PALETTE = {}  # <3 mutable globals
_MAX_F2DOT14 = 2 - 1 / (2**14)
_MIN_F2DOT14 = -2
_MAX_F2DOT14_ANGLE = _MAX_F2DOT14 * 180 + 180
_MIN_F2DOT14_ANGLE = _MIN_F2DOT14 * 180 + 180

_CROSS_GLYPH = "cross_glyph"
_UPEM_BOX_GLYPH = "upem_box_glyph"


logger = logging.getLogger()


class SampleGlyph(NamedTuple):
    glyph_name: str
    accessor: str
    advance: int
    glyph: Glyph
    description: Optional[str] = None
    axes_effect: Optional[str] = None
    clip_box: Optional[Tuple[float, float, float, float]] = None
    colr: Optional[Mapping[str, Any]] = None
    colrv0: Optional[Mapping[str, List[Tuple[str, int]]]] = None


def _cpal(color_str, alpha=1.0):
    color = Color.fromstring(color_str).to_ufo_color()
    if color not in _PALETTE:
        _PALETTE[color] = len(_PALETTE)
    return (_PALETTE[color], alpha)


def _sample_sweep(
    start_angle, end_angle, extend_mode_arg, color_line_range, position, accessor
):

    extend_mode_map = {
        "reflect": ot.ExtendMode.REFLECT,
        "repeat": ot.ExtendMode.REPEAT,
        "pad": ot.ExtendMode.PAD,
    }

    if extend_mode_arg not in extend_mode_map:
        return None

    extend_mode = extend_mode_map[extend_mode_arg]

    # Preparation for allowing testing with a differently configured ColorLine
    # that has stops at < 0 and > 1.
    color_line_range_map = {
        "narrow": {
            "ColorStop": [
                (0.25, *_cpal("red")),
                (1 / 3 * 0.5 + 0.25, *_cpal("yellow")),
                (2 / 3 * 0.5 + 0.25, *_cpal("green")),
                (0.75, *_cpal("blue")),
            ]
        },
    }

    if color_line_range not in color_line_range_map:
        return None

    color_line = color_line_range_map[color_line_range]

    glyph_name = f"sweep_{start_angle}_{end_angle}_{extend_mode_arg}_{color_line_range}"

    start_angle_addition = position["SWPS"] if "SWPS" in position else 0
    end_angle_addition = position["SWPE"] if "SWPE" in position else 0
    end_angle = max(
        min(end_angle + end_angle_addition, _MAX_F2DOT14_ANGLE), _MIN_F2DOT14_ANGLE
    )
    start_angle = max(
        min(start_angle + start_angle_addition, _MAX_F2DOT14_ANGLE), _MIN_F2DOT14_ANGLE
    )
    colr = {
        "Format": ot.PaintFormat.PaintGlyph,
        "Glyph": "circle_r350",
        "Paint": {
            "Format": ot.PaintFormat.PaintSweepGradient,
            "ColorLine": {
                **color_line,
                "Extend": extend_mode,
            },
            "centerX": 500,
            "centerY": 600,
            "startAngle": start_angle,
            "endAngle": end_angle,
        },
    }

    return SampleGlyph(
        glyph_name=glyph_name,
        accessor=accessor,
        advance=_UPEM,
        glyph=_upem_box_pen().glyph(),
        clip_box=(0, 0, _UPEM, _UPEM),
        colr=colr,
        description="Tests `Paint(Var)SweepGradient`.",
        axes_effect="`SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle.",
    )


def _lin_rad_solid_alpha(position, accessor):
    glyph_name = "solid_colorline_alpha"

    solid_alpha = 1
    gradient_alphas = [1, 1]

    if "APH1" in position:
        solid_alpha += position["APH1"]
    if "APH2" in position:
        gradient_alphas[0] += position["APH2"]
    if "APH3" in position:
        gradient_alphas[1] += position["APH3"]

    color_solid = _cpal("green", solid_alpha)

    colr = {
        "Format": ot.PaintFormat.PaintColrLayers,
        "Layers": [
            {
                "Format": ot.PaintFormat.PaintTranslate,
                "dx": 150,
                "dy": 0,
                "Paint": {
                    "Format": ot.PaintFormat.PaintGlyph,
                    "Glyph": "circle_r350",
                    "Paint": {
                        "Format": ot.PaintFormat.PaintSolid,
                        "PaletteIndex": color_solid[0],
                        "Alpha": color_solid[1],
                    },
                },
            },
            {
                "Format": ot.PaintFormat.PaintTranslate,
                "dx": -150,
                "dy": 0,
                "Paint": {
                    "Format": ot.PaintFormat.PaintGlyph,
                    "Glyph": "circle_r350",
                    "Paint": {
                        "Format": ot.PaintFormat.PaintLinearGradient,
                        "x0": 500,
                        "y0": 250,
                        "x1": 500,
                        "y1": 950,
                        "x2": 600,
                        "y2": 250,
                        "ColorLine": {
                            "ColorStop": [
                                (0, *_cpal("red", gradient_alphas[0])),
                                (1, *_cpal("blue", gradient_alphas[1])),
                            ],
                            "Extend": ot.ExtendMode.REPEAT,
                        },
                    },
                },
            },
        ],
    }

    return SampleGlyph(
        glyph_name=glyph_name,
        accessor=accessor,
        advance=_UPEM,
        glyph=_upem_box_pen().glyph(),
        clip_box=(0, 0, _UPEM, _UPEM),
        colr=colr,
        description="Tests variable alpha in linear gradient color stops, and in PaintVarSolid.",
        axes_effect="`APH1` affects PaintVarSolid alpha, `APH2` and `APH3` modify linear gradient alpha values.",
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
                "Glyph": "sweep_-360_0_pad_narrow",
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
            "Glyph": "sweep_-360_0_pad_narrow",
        },
        "BackdropPaint": {
            "Format": ot.PaintFormat.PaintTransform,
            "Paint": {
                "Format": ot.PaintFormat.PaintColrGlyph,
                "Glyph": "sweep_-360_0_pad_narrow",
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
        description=f"Tests `PaintLinearGradient` repeat modes for color stops {first_stop}, {second_stop}.",
    )


def _gradient_p2_skewed(accessor_char):
    glyph_name = f"gradient_p2_skewed"

    pen = TTGlyphPen(None)
    pen.moveTo((100, 250))
    pen.lineTo((100, 950))
    pen.lineTo((1200, 950))
    pen.lineTo((1200, 250))
    pen.closePath()

    colr = {
        "Format": ot.PaintFormat.PaintGlyph,
        "Glyph": glyph_name,
        "Paint": {
            "Format": ot.PaintFormat.PaintLinearGradient,
            "ColorLine": {
                "ColorStop": [
                    (0, *_cpal("red")),
                    (0.5, *_cpal("blue")),
                    (1, *_cpal("yellow")),
                ],
                "Extend": ot.ExtendMode.PAD,
            },
            "x0": 100,
            "y0": 950,
            "x1": 2300,
            "y1": 950,
            "x2": -1000,
            "y2": 250,
        },
    }

    return SampleGlyph(
        glyph_name=glyph_name,
        accessor=accessor_char,
        # Larger advance required for this glyph as it is wider to test the
        # P2-skewed gradient.
        advance=1250,
        glyph=pen.glyph(),
        clip_box=(100, 250, 1200, 950),
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


def _paint_scale(scale_x, scale_y, center_x, center_y, position, accessor_char):
    glyph_name = f"scale_{scale_x}_{scale_y}_center_{center_x}_{center_y}"

    logger.debug(position)

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

    # Can't apply deltas before as the original values are used for determining
    # which Paint format to choose.
    description = ""
    if center_x or center_y:
        if scale_x != scale_y:
            scaled_colr = {
                "Format": ot.PaintFormat.PaintScaleAroundCenter,
                "scaleX": scale_x,
                "scaleY": scale_y,
                "centerX": center_x,
                "centerY": center_y,
            }
            description = "`Paint(Var)ScaleAroundCenter`"
        else:
            scaled_colr = {
                "Format": ot.PaintFormat.PaintScaleUniformAroundCenter,
                "scale": scale_x,
                "centerX": center_x,
                "centerY": center_y,
            }
            description = "`Paint(Var)ScaleUniformAroundCenter`"
    else:
        if scale_x != scale_y:
            scaled_colr = {
                "Format": ot.PaintFormat.PaintScale,
                "scaleX": scale_x,
                "scaleY": scale_y,
            }
            description = "`Paint(Var)Scale`"
        else:
            scaled_colr = {
                "Format": ot.PaintFormat.PaintScaleUniform,
                "scale": scale_x,
            }
            description = "`Paint(Var)ScaleUniform`"

    if "centerX" in scaled_colr:
        scaled_colr["centerX"] += position["SCOX"] if "SCOX" in position else 0
    if "centerY" in scaled_colr:
        scaled_colr["centerY"] += position["SCOY"] if "SCOY" in position else 0
    if "scale" in scaled_colr:
        scaled_colr["scale"] += position["SCSX"] if "SCSX" in position else 0
    if "scaleX" in scaled_colr:
        scaled_colr["scaleX"] += position["SCSX"] if "SCSX" in position else 0
    if "scaleY" in scaled_colr:
        scaled_colr["scaleY"] += position["SCSY"] if "SCSY" in position else 0

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
        description=f"Tests {description}.",
        axes_effect="`SCOX` shifts center x offset, `SCOY` shifts center Y offfset, `SCSX` changes x or uniform scale factor, `SCSY` changes y scale factor.",
    )


def _extend_modes(gradient_format, extend_mode, position, accessor_char):

    format_map = {
        "linear": ot.PaintFormat.PaintLinearGradient,
        "radial": ot.PaintFormat.PaintRadialGradient,
    }

    if gradient_format not in format_map:
        return None

    selected_format = format_map[gradient_format]

    description = (
        "`Paint(Var)LinearGradient`"
        if gradient_format == "linear"
        else "`Paint(Var)RadialGradient`"
    )

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

    color_stop_positions = [0.0, 0.5, 1.0]
    for i in range(0, 3):
        axis = f"COL{i+1}"
        if axis in position:
            color_stop_positions[i] += position[axis]

    # Gradient coordinates variations.
    coordinates = coordinates[selected_format]
    for key in coordinates.keys():
        axis_name = f"GR{key.upper()}"
        if axis_name in position:
            coordinates[key] += position[axis_name]

    colr = {
        "Format": ot.PaintFormat.PaintGlyph,
        "Glyph": _UPEM_BOX_GLYPH,
        "Paint": {
            "Format": selected_format,
            "ColorLine": {
                "ColorStop": [
                    (color_stop_positions[0], *_cpal("green")),
                    (color_stop_positions[1], *_cpal("white")),
                    (color_stop_positions[2], *_cpal("red")),
                ],
                "Extend": extend_mode_map[extend_mode],
            },
            **coordinates,
        },
    }

    return SampleGlyph(
        glyph_name=glyph_name,
        accessor=accessor_char,
        glyph=_upem_box_pen().glyph(),
        advance=_UPEM,
        clip_box=(0, 0, _UPEM, _UPEM),
        colr=colr,
        description=f"Tests {description} with variable gradient coordinates or variable color lines.",
        axes_effect="`GRX0`, `GRY0`, `GRX1`, `GRY1`, `GRX2`, `GRY2`, `GRR0`, `GRR1` affect respective gradient coordinates. `COL1`, `COL2`, `COLR` shift color stops.",
    )


def _paint_rotate(angle, center_x, center_y, position, accessor_char):
    glyph_name = f"rotate_{angle}_center_{center_x}_{center_y}"

    color_orange = _cpal("orange", 0.7)

    angle_addition = position["ROTA"] if "ROTA" in position else 0
    rotate_angle = min(angle + angle_addition, _MAX_F2DOT14_ANGLE)

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

    description = ""
    if center_x or center_y:
        rotated_colr = {
            "Format": ot.PaintFormat.PaintRotateAroundCenter,
            "centerX": center_x,
            "centerY": center_y,
            "angle": rotate_angle,
        }
        description = (
            f"`Paint(Var)RotateAroundCenter` with center at ({center_x}, {center_y})."
        )
    else:
        rotated_colr = {"Format": ot.PaintFormat.PaintRotate, "angle": rotate_angle}
        description = "`Paint(Var)Rotate`"

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
        description=f"Tests {description}.",
        axes_effect="`ROTA`: changes rotation angle.",
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
        description="Tests `PaintSkew*` for x angle {x_skew_angle}, y angle {y_skew_angle}, x center {center_x}, y center {center_y}.",
    )


def _paint_transform(xx, xy, yx, yy, dx, dy, position, accessor):
    glyph_name = f"transform_matrix_{xx}_{xy}_{yx}_{yy}_{dx}_{dy}"

    def deltaOrZero(axis):
        return position[axis] if axis in position else 0

    t = (
        xx + deltaOrZero("TRXX"),
        xy + deltaOrZero("TRXY"),
        yx + deltaOrZero("TRYX"),
        yy + deltaOrZero("TRYY"),
        dx + deltaOrZero("TRDX"),
        dy + deltaOrZero("TRDY"),
    )
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
        description="Tests `Paint(Var)Transform`.",
        axes_effect="`TRXX`, `TRXY`, `TRYX`, `TRYY`, `TRDX`, `TRDY` affect the individual transformation matrix coordinates.",
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
        description=f"Tests `PaintComposite` for mode {composite_mode}.",
    )


def _foreground_color(fill_type, foreground_alpha, accessor_char):

    FOREGROUND_PALETTE_INDEX = 0xFFFF

    fill_type_map = {
        "solid": {
            "Format": ot.PaintFormat.PaintSolid,
            "PaletteIndex": FOREGROUND_PALETTE_INDEX,
            "Alpha": foreground_alpha,
        },
        "linear": {
            "Format": ot.PaintFormat.PaintLinearGradient,
            "ColorLine": {
                "ColorStop": [
                    (0.0, *_cpal("orange")),
                    (0.5, FOREGROUND_PALETTE_INDEX, foreground_alpha),
                    (1.0, *_cpal("orange")),
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
                    (0.0, *_cpal("orange")),
                    (0.5, FOREGROUND_PALETTE_INDEX, foreground_alpha),
                    (1.0, *_cpal("orange")),
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
                    (0.0, *_cpal("orange")),
                    (0.5, FOREGROUND_PALETTE_INDEX, foreground_alpha),
                    (1.0, *_cpal("orange")),
                ]
            },
            "centerX": 500,
            "centerY": 600,
            "startAngle": -180,
            "endAngle": 270,
        },
    }

    glyph_name = f"foreground_color_{fill_type}_alpha_{foreground_alpha}"

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


def _colrv0_colored_circles(palette_test_colors, accessor_char):
    pen = _upem_box_pen()
    glyph_name = "colored_circles_v0"
    color_iter = iter(palette_test_colors)

    colrv0_layers = [
        ("circle_r350", next(color_iter)),
        ("circle_r300", next(color_iter)),
        ("circle_r250", next(color_iter)),
        ("circle_r200", next(color_iter)),
        ("circle_r150", next(color_iter)),
        ("circle_r100", next(color_iter)),
        ("circle_r50", next(color_iter)),
        ("zero", _cpal("black")[0]),
    ]

    return SampleGlyph(
        glyph_name=glyph_name,
        accessor=accessor_char,
        advance=_UPEM,
        glyph=pen.glyph(),
        colrv0=colrv0_layers,
    )


def _colrv1_colored_circles(palette_test_colors, accessor_char):
    pen = _upem_box_pen()
    glyph_name = "colored_circles_v1"

    def circle_reference(size, color_index):
        return {
            "Format": ot.PaintFormat.PaintGlyph,
            "Glyph": f"circle_r{size}",
            "Paint": {
                "Format": ot.PaintFormat.PaintSolid,
                "PaletteIndex": color_index,
                "Alpha": 1.0,
            },
        }

    color_iter = iter(palette_test_colors)

    colrv1 = {
        "Format": ot.PaintFormat.PaintColrLayers,
        "Layers": [
            circle_reference(350, next(color_iter)),
            circle_reference(300, next(color_iter)),
            circle_reference(250, next(color_iter)),
            circle_reference(200, next(color_iter)),
            circle_reference(150, next(color_iter)),
            circle_reference(100, next(color_iter)),
            circle_reference(50, next(color_iter)),
            {
                "Format": ot.PaintFormat.PaintGlyph,
                "Glyph": "one",
                "Paint": {
                    "Format": ot.PaintFormat.PaintSolid,
                    "PaletteIndex": _cpal("black")[0],
                    "Alpha": 1.0,
                },
            },
        ],
    }

    return SampleGlyph(
        glyph_name=glyph_name,
        accessor=accessor_char,
        advance=_UPEM,
        glyph=pen.glyph(),
        colr=colrv1,
    )


def _circle_of_size(upem_radius, accessor_char):
    glyph_name = f"circle_r{upem_radius}"

    center_x = 500
    center_y = 600
    size_x = upem_radius
    size_y = upem_radius

    # Drawing 4 quadrants of a circle.
    approx = 4 * (sqrt(2) - 1) / 3
    tt_pen = TTGlyphPen(None)
    pen = Cu2QuPen(other_pen=tt_pen, max_err=_UPEM / 1000)
    for direction in [(-1, 1), (1, 1), (1, -1), (-1, -1)]:
        pen.moveTo((center_x - (direction[0] * size_x), center_y))
        pen.curveTo(
            (
                center_x - direction[0] * size_x,
                center_y - approx * direction[1] * size_y,
            ),
            (
                center_x - approx * direction[0] * size_x,
                center_y - direction[1] * size_y,
            ),
            (center_x, center_y - direction[1] * size_y),
        )
        pen.lineTo((center_x, center_y))
        pen.closePath()

    return SampleGlyph(
        glyph_name=glyph_name,
        accessor=accessor_char,
        advance=_UPEM,
        glyph=tt_pen.glyph(),
    )


def _one_glyph(accessor_char):
    glyph_name = "one"

    draw_pen = TTGlyphPen(None)
    pen = draw_pen.transformPen(draw_pen, (0.2, 0, 0, 0.2, 150, 250))
    # 1 glyph taken from Roboto Regular.
    pen.moveTo((729, 1464))
    for line_point in [
        (729, 0),
        (544, 0),
        (544, 1233),
        (171, 1079),
        (171, 1264),
        (700, 1464),
    ]:
        pen.lineTo(line_point)
    pen.closePath()
    return SampleGlyph(
        glyph_name="one", accessor=accessor_char, advance=_UPEM, glyph=draw_pen.glyph()
    )


def _zero_glyph(accessor_char):
    glyph_name = "zero"
    draw_pen = TTGlyphPen(None)
    pen = draw_pen.transformPen(draw_pen, (0.2, 0, 0, 0.2, 150, 250))

    # 0 glyph taken from Roboto Regular
    pen.moveTo((1035, 622))
    pen.qCurveTo((1035, 264), (788, -20), (576, -20))
    pen.qCurveTo((367, -20), (115, 264), (115, 622))
    pen.lineTo((115, 844))
    pen.qCurveTo((115, 1201), (365, 1476), (574, 1476))
    pen.qCurveTo((786, 1476), (1035, 1201), (1035, 844))
    pen.closePath()

    pen.moveTo((849, 875))
    pen.qCurveTo((849, 1121), (709, 1325), (574, 1325))
    pen.qCurveTo((442, 1325), (301, 1121), (301, 875))
    pen.lineTo((301, 592))
    pen.qCurveTo((301, 348), (444, 132), (576, 132))
    pen.qCurveTo((712, 132), (849, 348), (849, 592))
    pen.closePath()

    return SampleGlyph(
        glyph_name="zero", accessor=accessor_char, advance=_UPEM, glyph=draw_pen.glyph()
    )


def _reserve_circle_colors():
    return [
        _cpal("red")[0],
        _cpal("orange")[0],
        _cpal("yellow")[0],
        _cpal("green")[0],
        _cpal("blue")[0],
        _cpal("indigo")[0],
        _cpal("violet")[0],
    ]


def _prepare_palette():
    dark_palette_sparse = [
        Color.fromstring(color_spec).to_ufo_color()
        for color_spec in [
            "#2a294a",
            "#244163",
            "#1b6388",
            "#157da3",
            "#0e9ac2",
            "#05bee8",
            "#00d4ff",
        ]
    ]
    light_palette_sparse = [
        Color.fromstring(color_spec).to_ufo_color()
        for color_spec in [
            "#fc7118",
            "#fb8115",
            "#fa9511",
            "#faa80d",
            "#f9be09",
            "#f8d304",
            "#f8e700",
        ]
    ]

    def _pad_palette(palette, expected_length):
        return palette + [Color.fromstring("gray").to_ufo_color()] * (
            expected_length - len(palette)
        )

    return {
        "palettes": [
            _PALETTE,
            _pad_palette(dark_palette_sparse, len(_PALETTE)),
            _pad_palette(light_palette_sparse, len(_PALETTE)),
        ],
        "paletteTypes": [
            0,
            ColorPaletteType.USABLE_WITH_DARK_BACKGROUND,
            ColorPaletteType.USABLE_WITH_LIGHT_BACKGROUND,
        ],
    }


def _get_glyph_definitions(position):
    # Place these first in the global primary palette.
    palette_test_colors = _reserve_circle_colors()

    access_chars_set = (
        ascii_letters
        + digits
        + "".join([chr(greek_letter) for greek_letter in range(0x03B1, 0x3C9)])
        + "".join([chr(greek_letter) for greek_letter in range(0x0391, 0x3A9)])
    )
    access_chars = iter(access_chars_set)
    glyphs = [
        SampleGlyph(glyph_name=".notdef", accessor="", advance=600, glyph=Glyph()),
        SampleGlyph(glyph_name=".null", accessor="", advance=0, glyph=Glyph()),
        _sample_sweep(-360, 0, "pad", "narrow", position, next(access_chars)),
        _sample_colr_glyph(next(access_chars)),
        _sample_composite_colr_glyph(next(access_chars)),
        _gradient_stops_repeat(0, 1, next(access_chars)),
        _gradient_stops_repeat(0.2, 0.8, next(access_chars)),
        _gradient_stops_repeat(0, 1.5, next(access_chars)),
        _gradient_stops_repeat(0.5, 1.5, next(access_chars)),
        _paint_scale(0.5, 1.5, _UPEM / 2, _UPEM / 2, position, next(access_chars)),
        _paint_scale(1.5, 1.5, _UPEM / 2, _UPEM / 2, position, next(access_chars)),
        _paint_scale(0.5, 1.5, 0, 0, position, next(access_chars)),
        _paint_scale(1.5, 1.5, 0, 0, position, next(access_chars)),
        _paint_scale(0.5, 1.5, _UPEM, _UPEM, position, next(access_chars)),
        _paint_scale(1.5, 1.5, _UPEM, _UPEM, position, next(access_chars)),
        _extend_modes("linear", "pad", position, next(access_chars)),
        _extend_modes("linear", "repeat", position, next(access_chars)),
        _extend_modes("linear", "reflect", position, next(access_chars)),
        _extend_modes("radial", "pad", position, next(access_chars)),
        _extend_modes("radial", "repeat", position, next(access_chars)),
        _extend_modes("radial", "reflect", position, next(access_chars)),
        _paint_rotate(10, 0, 0, position, next(access_chars)),
        _paint_rotate(-10, _UPEM, _UPEM, position, next(access_chars)),
        _paint_rotate(25, _UPEM / 2, _UPEM / 2, position, next(access_chars)),
        _paint_rotate(-15, _UPEM / 2, _UPEM / 2, position, next(access_chars)),
        _paint_skew(25, 0, 0, 0, next(access_chars)),
        _paint_skew(25, 0, _UPEM / 2, _UPEM / 2, next(access_chars)),
        _paint_skew(0, 15, 0, 0, next(access_chars)),
        _paint_skew(0, 15, _UPEM / 2, _UPEM / 2, next(access_chars)),
        _paint_skew(-10, 20, _UPEM / 2, _UPEM / 2, next(access_chars)),
        _paint_skew(-10, 20, _UPEM, _UPEM, next(access_chars)),
        _paint_transform(1, 0, 0, 1, 125, 125, position, next(access_chars)),
        _paint_transform(1.5, 0, 0, 1.5, 0, 0, position, next(access_chars)),
        _paint_transform(
            0.9659, 0.2588, -0.2588, 0.9659, 0, 0, position, next(access_chars)
        ),  # Rotation 15 degrees counterclockwise
        _paint_transform(
            1.0, 0.0, 0.6, 1.0, -300.0, 0.0, position, next(access_chars)
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
        _foreground_color("linear", 1, next(access_chars)),
        _foreground_color("radial", 1, next(access_chars)),
        _foreground_color("sweep", 1, next(access_chars)),
        _foreground_color("solid", 1, next(access_chars)),
        _foreground_color("linear", 0.3, next(access_chars)),
        _foreground_color("radial", 0.3, next(access_chars)),
        _foreground_color("sweep", 0.3, next(access_chars)),
        _foreground_color("solid", 0.3, next(access_chars)),
        _gradient_p2_skewed(next(access_chars)),
        _colrv0_colored_circles(palette_test_colors, next(access_chars)),
        _colrv1_colored_circles(palette_test_colors, next(access_chars)),
        # Sweep with repeat mode pad
        _sample_sweep(0, 90, "pad", "narrow", position, next(access_chars)),
        _sample_sweep(45, 90, "pad", "narrow", position, next(access_chars)),
        _sample_sweep(247.5, 292.5, "pad", "narrow", position, next(access_chars)),
        _sample_sweep(90, 270, "pad", "narrow", position, next(access_chars)),
        _sample_sweep(-270, 270, "pad", "narrow", position, next(access_chars)),
        _sample_sweep(-45, 45, "pad", "narrow", position, next(access_chars)),
        _sample_sweep(315, 45, "pad", "narrow", position, next(access_chars)),
        # Sweep with repeat mode reflect
        _sample_sweep(-360, 0, "reflect", "narrow", position, next(access_chars)),
        _sample_sweep(0, 90, "reflect", "narrow", position, next(access_chars)),
        _sample_sweep(45, 90, "reflect", "narrow", position, next(access_chars)),
        _sample_sweep(247.5, 292.5, "reflect", "narrow", position, next(access_chars)),
        _sample_sweep(90, 270, "reflect", "narrow", position, next(access_chars)),
        _sample_sweep(-270, 270, "reflect", "narrow", position, next(access_chars)),
        _sample_sweep(-45, 45, "reflect", "narrow", position, next(access_chars)),
        _sample_sweep(315, 45, "reflect", "narrow", position, next(access_chars)),
        # Sweep with repeat mode repeat
        _sample_sweep(-360, 0, "repeat", "narrow", position, next(access_chars)),
        _sample_sweep(0, 90, "repeat", "narrow", position, next(access_chars)),
        _sample_sweep(45, 90, "repeat", "narrow", position, next(access_chars)),
        _sample_sweep(247.5, 292.5, "repeat", "narrow", position, next(access_chars)),
        _sample_sweep(90, 270, "repeat", "narrow", position, next(access_chars)),
        _sample_sweep(-270, 270, "repeat", "narrow", position, next(access_chars)),
        _sample_sweep(-45, 45, "repeat", "narrow", position, next(access_chars)),
        _sample_sweep(315, 45, "repeat", "narrow", position, next(access_chars)),
        _lin_rad_solid_alpha(position, next(access_chars)),
        # Non COLR helper glyphs below here.
        _cross_glyph(),
        _upem_box_glyph(),
        _clip_shade_glyph("center", next(access_chars)),
        _clip_shade_glyph("top_left", next(access_chars)),
        _clip_shade_glyph("bottom_left", next(access_chars)),
        _clip_shade_glyph("bottom_right", next(access_chars)),
        _clip_shade_glyph("top_right", next(access_chars)),
        _inset_clipped_radial_reflect(next(access_chars)),
        _circle_of_size(50, next(access_chars)),
        _circle_of_size(100, next(access_chars)),
        _circle_of_size(150, next(access_chars)),
        _circle_of_size(200, next(access_chars)),
        _circle_of_size(250, next(access_chars)),
        _circle_of_size(300, next(access_chars)),
        _circle_of_size(350, next(access_chars)),
        _one_glyph(next(access_chars)),
        _zero_glyph(next(access_chars)),
    ]
    return glyphs


def _build_font(names, position):
    glyphs = _get_glyph_definitions(position)
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

    colr_v0_glyphs = {g.glyph_name: g.colrv0 for g in glyphs if g.colrv0}
    colr_v1_glyphs = {g.glyph_name: g.colr for g in glyphs if g.colr}
    fb.font["COLR"] = colorBuilder.buildCOLR(
        {**colr_v0_glyphs, **colr_v1_glyphs},
        clipBoxes={g.glyph_name: g.clip_box for g in glyphs if g.clip_box},
    )
    fb.font["CPAL"] = colorBuilder.buildCPAL(**_prepare_palette())
    return fb


def build_descriptions_(font):
    glyphs = _get_glyph_definitions({})
    reverse_glyph_map = font.getReverseGlyphMap()

    def find_description(glyph_name):
        for glyph in glyphs:
            if glyph.glyph_name == glyph_name:
                return (glyph.description, glyph.axes_effect, glyph.accessor)

    description_map = {}
    for glyph_name, glyph_id in reverse_glyph_map.items():
        description_effect = find_description(glyph_name)
        description_map[glyph_name] = {
            "glyph_id": glyph_id,
            "character": description_effect[2],
            "description": description_effect[0],
            "axes_effect": description_effect[1],
        }
    with open("glyph_descriptions.md", "w", encoding="utf-8") as md_file:
        md_file.write(
            "| Id | Char | Glyph name | Description | Variable Axes effect |\n"
        )
        md_file.write("|-|-|-|-|-|\n")
        for glyph_name, glyph in description_map.items():
            md_file.write(
                f'| {glyph["glyph_id"]} | {glyph["character"]} | `{glyph_name}` | {glyph["description"]} | {glyph["axes_effect"]} |\n'
            )


def main(args=None):

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="More verbose output, repeat option for higher verbosity.",
        action="count",
        default=0,
    )
    parser.add_argument(
        "--generate-descriptions",
        help="Generate Markdown glyph descriptions.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "build_dir",
        type=str,
        default="",
        help="Output directory",
        nargs=1,
        metavar="BUILD_DIR",
    )
    options = parser.parse_args(args)

    if not options.verbose:
        level = "WARNING"
    elif options.verbose == 1:
        level = "INFO"
    else:
        level = "DEBUG"
    logging.basicConfig(level=level, format="%(message)s")

    build_dir = Path(options.build_dir[0]) or None
    if not build_dir:
        parser.error("No output directory specified.")
    build_dir.mkdir(exist_ok=True)

    logger.info(f"Output directory: {build_dir}")

    generate_descriptions = options.generate_descriptions

    version = datetime.datetime.now().isoformat()
    names = {
        "familyName": _FAMILY,
        "styleName": _STYLE,
        "uniqueFontIdentifier": " ".join((_FAMILY, version)),
        "fullName": " ".join((_FAMILY, _STYLE)),
        "version": version,
        "psName": "-".join((_FAMILY.replace(" ", ""), _STYLE)),
    }

    designspace = designspaceLib.DesignSpaceDocument()

    axis_defs = [
        dict(
            tag="SWPS",
            name="Sweep Start Angle Offset",
            minimum=-90,
            default=0,
            maximum=90,
        ),
        dict(
            tag="SWPE",
            name="Sweep End Angle Offset",
            minimum=-90,
            default=0,
            maximum=90,
        ),
        dict(
            tag="ROTA",
            name="Var Rotate Angle Offset",
            minimum=0,
            default=0,
            maximum=_MAX_F2DOT14_ANGLE,
        ),
        dict(
            tag="COL1",
            name="Extend tests color stop offset 1",
            minimum=-2,
            default=0,
            maximum=2,
        ),
        dict(
            tag="COL2",
            name="Extend tests color stop offset 2",
            minimum=-2,
            default=0,
            maximum=2,
        ),
        dict(
            tag="COL3",
            name="Extend tests color stop offset 3",
            minimum=-2,
            default=0,
            maximum=2,
        ),
        dict(
            tag="SCOX",
            name="Scale tests, center x offset",
            minimum=-200,
            default=0,
            maximum=200,
        ),
        dict(
            tag="SCOY",
            name="Scale tests, center y offset",
            minimum=-200,
            default=0,
            maximum=200,
        ),
        dict(
            tag="SCSX",
            name="Scale tests, x or uniform scale",
            minimum=_MIN_F2DOT14,
            default=0,
            maximum=_MAX_F2DOT14,
        ),
        dict(
            tag="SCSY",
            name="Scale tests, y scale",
            minimum=_MIN_F2DOT14,
            default=0,
            maximum=_MAX_F2DOT14,
        ),
        dict(
            tag="APH1", name="Alpha axis, PaintSolid", minimum=-1, default=0, maximum=0
        ),
        dict(
            tag="APH2", name="Alpha axis, ColorStop 0", minimum=-1, default=0, maximum=0
        ),
        dict(
            tag="APH3", name="Alpha axis, ColorStop 1", minimum=-1, default=0, maximum=0
        ),
    ]

    gradient_coords = ["x0", "y0", "x1", "y1", "x2", "y2", "r0", "r1"]
    for coord in gradient_coords:
        axis_defs.append(
            dict(
                tag=f"GR{coord.upper()}",
                name=f"Gradient coords, {coord}",
                minimum=-1000,
                default=0,
                maximum=1000,
            )
        )

    transform_matrix = ["xx", "yx", "xy", "yy", "dx", "dy"]
    for transform_scalar in transform_matrix:
        axis_defs.append(
            dict(
                tag=f"TR{transform_scalar.upper()}",
                name=f"Transform scalars, {transform_scalar}",
                minimum=-2 if not "d" in transform_scalar else -500,
                default=0,
                maximum=2 if not "d" in transform_scalar else 500,
            )
        )

    logger.debug(json.dumps(axis_defs))

    # For each axis, if differing from default, add the minimum and maximum axis positions as one master.
    all_default_positions = {}
    all_default_locations = {}
    for axis_def in axis_defs:
        designspace.addAxisDescriptor(**axis_def)
        all_default_positions[axis_def["tag"]] = axis_def["default"]
        all_default_locations[axis_def["name"]] = axis_def["default"]

    # Start with the master of all default positions.
    variation_positions = [all_default_positions]

    default_font_builder = _build_font(names, all_default_positions)

    if generate_descriptions:
        logger.info("Building descriptions.")
        build_descriptions_(default_font_builder.font)

    script_name = Path(__file__).name
    variable_name = PurePath(__file__).stem + "_variable"
    static_out_file = (build_dir / script_name).with_suffix(".ttf")
    variable_out_file = (build_dir / variable_name).with_suffix(".ttf")

    default_font_builder.save(static_out_file)
    logger.info(f"Static font {static_out_file} written.")

    designspace.addSourceDescriptor(
        name="All Default",
        location=all_default_locations,
        font=default_font_builder.font,
    )

    # Append the minimum and maximum for each axis as masters, if differing from default.
    for change_axis in axis_defs:
        for change_key in ["minimum", "maximum"]:
            axis_value = change_axis[change_key]
            if axis_value == change_axis["default"]:
                continue
            position_dict = all_default_positions.copy()
            position_dict[change_axis["tag"]] = axis_value
            location_dict = all_default_locations.copy()
            location_dict[change_axis["name"]] = axis_value
            master_name = f'Master {change_axis["name"]} {change_key.capitalize()}'
            designspace.addSourceDescriptor(
                name=master_name,
                location=location_dict,
                font=_build_font(names, position_dict).font,
            )

    # Build the variable font.
    # varLib.build returns a (vf, model, master_ttfs) tuple but I only care about the first.
    vf = varLib.build(
        designspace,
    )[0]
    vf.save(variable_out_file)
    logger.info(f"Variable font {variable_out_file} written.")


if __name__ == "__main__":
    main()
