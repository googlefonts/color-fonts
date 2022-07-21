| Id | Char | U+hex | Name | Description | Variable Axes effect |
|-|-|-|-|-|-|
| 0 |  |  | `.notdef` | None | None |
| 1 |  |  | `.null` | None | None |
| 2 | 󰀀 | U+F0000 | `sweep_-360_0_pad_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 3 | 󰀁 | U+F0001 | `transformed_sweep` | None | None |
| 4 | 󰀂 | U+F0002 | `composite_colr_glyph` | None | None |
| 5 | 󰀃 | U+F0003 | `linear_repeat_0_1` | Tests `PaintLinearGradient` repeat modes for color stops 0, 1. | None |
| 6 | 󰀄 | U+F0004 | `linear_repeat_0.2_0.8` | Tests `PaintLinearGradient` repeat modes for color stops 0.2, 0.8. | None |
| 7 | 󰀅 | U+F0005 | `linear_repeat_0_1.5` | Tests `PaintLinearGradient` repeat modes for color stops 0, 1.5. | None |
| 8 | 󰀆 | U+F0006 | `linear_repeat_0.5_1.5` | Tests `PaintLinearGradient` repeat modes for color stops 0.5, 1.5. | None |
| 9 | 󰀇 | U+F0007 | `scale_0.5_1.5_center_500.0_500.0` | Tests `Paint(Var)ScaleAroundCenter`. | `SCOX` shifts center x offset, `SCOY` shifts center Y offfset, `SCSX` changes x or uniform scale factor, `SCSY` changes y scale factor. |
| 10 | 󰀈 | U+F0008 | `scale_1.5_1.5_center_500.0_500.0` | Tests `Paint(Var)ScaleUniformAroundCenter`. | `SCOX` shifts center x offset, `SCOY` shifts center Y offfset, `SCSX` changes x or uniform scale factor, `SCSY` changes y scale factor. |
| 11 | 󰀉 | U+F0009 | `scale_0.5_1.5_center_0_0` | Tests `Paint(Var)Scale`. | `SCOX` shifts center x offset, `SCOY` shifts center Y offfset, `SCSX` changes x or uniform scale factor, `SCSY` changes y scale factor. |
| 12 | 󰀊 | U+F000A | `scale_1.5_1.5_center_0_0` | Tests `Paint(Var)ScaleUniform`. | `SCOX` shifts center x offset, `SCOY` shifts center Y offfset, `SCSX` changes x or uniform scale factor, `SCSY` changes y scale factor. |
| 13 | 󰀋 | U+F000B | `scale_0.5_1.5_center_1000_1000` | Tests `Paint(Var)ScaleAroundCenter`. | `SCOX` shifts center x offset, `SCOY` shifts center Y offfset, `SCSX` changes x or uniform scale factor, `SCSY` changes y scale factor. |
| 14 | 󰀌 | U+F000C | `scale_1.5_1.5_center_1000_1000` | Tests `Paint(Var)ScaleUniformAroundCenter`. | `SCOX` shifts center x offset, `SCOY` shifts center Y offfset, `SCSX` changes x or uniform scale factor, `SCSY` changes y scale factor. |
| 15 | 󰀍 | U+F000D | `linear_gradient_extend_mode_pad` | Tests `Paint(Var)LinearGradient` with variable gradient coordinates or variable color lines. | `GRX0`, `GRY0`, `GRX1`, `GRY1`, `GRX2`, `GRY2`, `GRR0`, `GRR1` affect respective gradient coordinates. `COL1`, `COL2`, `COLR` shift color stops. |
| 16 | 󰀎 | U+F000E | `linear_gradient_extend_mode_repeat` | Tests `Paint(Var)LinearGradient` with variable gradient coordinates or variable color lines. | `GRX0`, `GRY0`, `GRX1`, `GRY1`, `GRX2`, `GRY2`, `GRR0`, `GRR1` affect respective gradient coordinates. `COL1`, `COL2`, `COLR` shift color stops. |
| 17 | 󰀏 | U+F000F | `linear_gradient_extend_mode_reflect` | Tests `Paint(Var)LinearGradient` with variable gradient coordinates or variable color lines. | `GRX0`, `GRY0`, `GRX1`, `GRY1`, `GRX2`, `GRY2`, `GRR0`, `GRR1` affect respective gradient coordinates. `COL1`, `COL2`, `COLR` shift color stops. |
| 18 | 󰀐 | U+F0010 | `radial_gradient_extend_mode_pad` | Tests `Paint(Var)RadialGradient` with variable gradient coordinates or variable color lines. | `GRX0`, `GRY0`, `GRX1`, `GRY1`, `GRX2`, `GRY2`, `GRR0`, `GRR1` affect respective gradient coordinates. `COL1`, `COL2`, `COLR` shift color stops. |
| 19 | 󰀑 | U+F0011 | `radial_gradient_extend_mode_repeat` | Tests `Paint(Var)RadialGradient` with variable gradient coordinates or variable color lines. | `GRX0`, `GRY0`, `GRX1`, `GRY1`, `GRX2`, `GRY2`, `GRR0`, `GRR1` affect respective gradient coordinates. `COL1`, `COL2`, `COLR` shift color stops. |
| 20 | 󰀒 | U+F0012 | `radial_gradient_extend_mode_reflect` | Tests `Paint(Var)RadialGradient` with variable gradient coordinates or variable color lines. | `GRX0`, `GRY0`, `GRX1`, `GRY1`, `GRX2`, `GRY2`, `GRR0`, `GRR1` affect respective gradient coordinates. `COL1`, `COL2`, `COLR` shift color stops. |
| 21 | 󰀓 | U+F0013 | `rotate_10_center_0_0` | Tests `Paint(Var)Rotate`. | `ROTA`: changes rotation angle. |
| 22 | 󰀔 | U+F0014 | `rotate_-10_center_1000_1000` | Tests `Paint(Var)RotateAroundCenter` with center at (1000, 1000).. | `ROTA`: changes rotation angle. |
| 23 | 󰀕 | U+F0015 | `rotate_25_center_500.0_500.0` | Tests `Paint(Var)RotateAroundCenter` with center at (500.0, 500.0).. | `ROTA`: changes rotation angle. |
| 24 | 󰀖 | U+F0016 | `rotate_-15_center_500.0_500.0` | Tests `Paint(Var)RotateAroundCenter` with center at (500.0, 500.0).. | `ROTA`: changes rotation angle. |
| 25 | 󰀗 | U+F0017 | `skew_25_0_center_0_0` | Tests `PaintSkew*` for x angle {x_skew_angle}, y angle {y_skew_angle}, x center {center_x}, y center {center_y}. | None |
| 26 | 󰀘 | U+F0018 | `skew_25_0_center_500.0_500.0` | Tests `PaintSkew*` for x angle {x_skew_angle}, y angle {y_skew_angle}, x center {center_x}, y center {center_y}. | None |
| 27 | 󰀙 | U+F0019 | `skew_0_15_center_0_0` | Tests `PaintSkew*` for x angle {x_skew_angle}, y angle {y_skew_angle}, x center {center_x}, y center {center_y}. | None |
| 28 | 󰀚 | U+F001A | `skew_0_15_center_500.0_500.0` | Tests `PaintSkew*` for x angle {x_skew_angle}, y angle {y_skew_angle}, x center {center_x}, y center {center_y}. | None |
| 29 | 󰀛 | U+F001B | `skew_-10_20_center_500.0_500.0` | Tests `PaintSkew*` for x angle {x_skew_angle}, y angle {y_skew_angle}, x center {center_x}, y center {center_y}. | None |
| 30 | 󰀜 | U+F001C | `skew_-10_20_center_1000_1000` | Tests `PaintSkew*` for x angle {x_skew_angle}, y angle {y_skew_angle}, x center {center_x}, y center {center_y}. | None |
| 31 | 󰀝 | U+F001D | `transform_matrix_1_0_0_1_125_125` | Tests `Paint(Var)Transform`. | `TRXX`, `TRXY`, `TRYX`, `TRYY`, `TRDX`, `TRDY` affect the individual transformation matrix coordinates. |
| 32 | 󰀞 | U+F001E | `transform_matrix_1.5_0_0_1.5_0_0` | Tests `Paint(Var)Transform`. | `TRXX`, `TRXY`, `TRYX`, `TRYY`, `TRDX`, `TRDY` affect the individual transformation matrix coordinates. |
| 33 | 󰀟 | U+F001F | `transform_matrix_0.9659_0.2588_-0.2588_0.9659_0_0` | Tests `Paint(Var)Transform`. | `TRXX`, `TRXY`, `TRYX`, `TRYY`, `TRDX`, `TRDY` affect the individual transformation matrix coordinates. |
| 34 | 󰀠 | U+F0020 | `transform_matrix_1.0_0.0_0.6_1.0_-300.0_0.0` | Tests `Paint(Var)Transform`. | `TRXX`, `TRXY`, `TRYX`, `TRYY`, `TRDX`, `TRDY` affect the individual transformation matrix coordinates. |
| 35 | 󰀡 | U+F0021 | `clip_box_top_left` | None | None |
| 36 | 󰀢 | U+F0022 | `clip_box_bottom_left` | None | None |
| 37 | 󰀣 | U+F0023 | `clip_box_bottom_right` | None | None |
| 38 | 󰀤 | U+F0024 | `clip_box_top_right` | None | None |
| 39 | 󰀥 | U+F0025 | `clip_box_center` | None | None |
| 40 | 󰀦 | U+F0026 | `composite_DEST_OVER` | Tests `PaintComposite` for mode DEST_OVER. | None |
| 41 | 󰀧 | U+F0027 | `composite_XOR` | Tests `PaintComposite` for mode XOR. | None |
| 42 | 󰀨 | U+F0028 | `composite_OVERLAY` | Tests `PaintComposite` for mode OVERLAY. | None |
| 43 | 󰀩 | U+F0029 | `composite_SRC_IN` | Tests `PaintComposite` for mode SRC_IN. | None |
| 44 | 󰀪 | U+F002A | `composite_PLUS` | Tests `PaintComposite` for mode PLUS. | None |
| 45 | 󰀫 | U+F002B | `composite_LIGHTEN` | Tests `PaintComposite` for mode LIGHTEN. | None |
| 46 | 󰀬 | U+F002C | `composite_MULTIPLY` | Tests `PaintComposite` for mode MULTIPLY. | None |
| 47 | 󰀭 | U+F002D | `foreground_color_linear_alpha_1` | None | None |
| 48 | 󰀮 | U+F002E | `foreground_color_radial_alpha_1` | None | None |
| 49 | 󰀯 | U+F002F | `foreground_color_sweep_alpha_1` | None | None |
| 50 | 󰀰 | U+F0030 | `foreground_color_solid_alpha_1` | None | None |
| 51 | 󰀱 | U+F0031 | `foreground_color_linear_alpha_0.3` | None | None |
| 52 | 󰀲 | U+F0032 | `foreground_color_radial_alpha_0.3` | None | None |
| 53 | 󰀳 | U+F0033 | `foreground_color_sweep_alpha_0.3` | None | None |
| 54 | 󰀴 | U+F0034 | `foreground_color_solid_alpha_0.3` | None | None |
| 55 | 󰀵 | U+F0035 | `gradient_p2_skewed` | None | None |
| 56 | 󰀶 | U+F0036 | `colored_circles_v0` | None | None |
| 57 | 󰀷 | U+F0037 | `colored_circles_v1` | None | None |
| 58 | 󰀸 | U+F0038 | `sweep_0_90_pad_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 59 | 󰀹 | U+F0039 | `sweep_45_90_pad_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 60 | 󰀺 | U+F003A | `sweep_247.5_292.5_pad_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 61 | 󰀻 | U+F003B | `sweep_90_270_pad_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 62 | 󰀼 | U+F003C | `sweep_-270_270_pad_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 63 | 󰀽 | U+F003D | `sweep_-45_45_pad_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 64 | 󰀾 | U+F003E | `sweep_315_45_pad_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 65 | 󰀿 | U+F003F | `sweep_-360_0_reflect_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 66 | 󰁀 | U+F0040 | `sweep_0_90_reflect_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 67 | 󰁁 | U+F0041 | `sweep_45_90_reflect_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 68 | 󰁂 | U+F0042 | `sweep_247.5_292.5_reflect_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 69 | 󰁃 | U+F0043 | `sweep_90_270_reflect_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 70 | 󰁄 | U+F0044 | `sweep_-270_270_reflect_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 71 | 󰁅 | U+F0045 | `sweep_-45_45_reflect_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 72 | 󰁆 | U+F0046 | `sweep_315_45_reflect_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 73 | 󰁇 | U+F0047 | `sweep_-360_0_repeat_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 74 | 󰁈 | U+F0048 | `sweep_0_90_repeat_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 75 | 󰁉 | U+F0049 | `sweep_45_90_repeat_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 76 | 󰁊 | U+F004A | `sweep_247.5_292.5_repeat_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 77 | 󰁋 | U+F004B | `sweep_90_270_repeat_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 78 | 󰁌 | U+F004C | `sweep_-270_270_repeat_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 79 | 󰁍 | U+F004D | `sweep_-45_45_repeat_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 80 | 󰁎 | U+F004E | `sweep_315_45_repeat_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 81 | 󰁏 | U+F004F | `solid_colorline_alpha` | Tests variable alpha in linear gradient color stops, and in PaintVarSolid. | `APH1` affects PaintVarSolid alpha, `APH2` and `APH3` modify linear gradient alpha values. |
| 82 | + | U+2B | `cross_glyph` | None | None |
| 83 | ▀ | U+2580 | `upem_box_glyph` | None | None |
| 84 | 󰁐 | U+F0050 | `clip_shade_center` | None | None |
| 85 | 󰁑 | U+F0051 | `clip_shade_top_left` | None | None |
| 86 | 󰁒 | U+F0052 | `clip_shade_bottom_left` | None | None |
| 87 | 󰁓 | U+F0053 | `clip_shade_bottom_right` | None | None |
| 88 | 󰁔 | U+F0054 | `clip_shade_top_right` | None | None |
| 89 | 󰁕 | U+F0055 | `inset_clipped_radial_reflect` | None | None |
| 90 | 󰁖 | U+F0056 | `circle_r50` | None | None |
| 91 | 󰁗 | U+F0057 | `circle_r100` | None | None |
| 92 | 󰁘 | U+F0058 | `circle_r150` | None | None |
| 93 | 󰁙 | U+F0059 | `circle_r200` | None | None |
| 94 | 󰁚 | U+F005A | `circle_r250` | None | None |
| 95 | 󰁛 | U+F005B | `circle_r300` | None | None |
| 96 | 󰁜 | U+F005C | `circle_r350` | None | None |
| 97 | 󰁝 | U+F005D | `one` | None | None |
| 98 | 󰁞 | U+F005E | `zero` | None | None |
