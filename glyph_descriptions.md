| Id | Char | Glyph name | Description | Variable Axes effect |
|-|-|-|-|-|
| 0 |  | `.notdef` | None | None |
| 1 |  | `.null` | None | None |
| 2 | a | `sweep_-360_0_pad_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 3 | b | `transformed_sweep` | None | None |
| 4 | c | `composite_colr_glyph` | None | None |
| 5 | d | `linear_repeat_0_1` | Tests `PaintLinearGradient` repeat modes for color stops 0, 1. | None |
| 6 | e | `linear_repeat_0.2_0.8` | Tests `PaintLinearGradient` repeat modes for color stops 0.2, 0.8. | None |
| 7 | f | `linear_repeat_0_1.5` | Tests `PaintLinearGradient` repeat modes for color stops 0, 1.5. | None |
| 8 | g | `linear_repeat_0.5_1.5` | Tests `PaintLinearGradient` repeat modes for color stops 0.5, 1.5. | None |
| 9 | h | `scale_0.5_1.5_center_500.0_500.0` | Tests `Paint(Var)ScaleAroundCenter`. | `SCOX` shifts center x offset, `SCOY` shifts center Y offfset, `SCSX` changes x or uniform scale factor, `SCSY` changes y scale factor. |
| 10 | i | `scale_1.5_1.5_center_500.0_500.0` | Tests `Paint(Var)ScaleUniformAroundCenter`. | `SCOX` shifts center x offset, `SCOY` shifts center Y offfset, `SCSX` changes x or uniform scale factor, `SCSY` changes y scale factor. |
| 11 | j | `scale_0.5_1.5_center_0_0` | Tests `Paint(Var)Scale`. | `SCOX` shifts center x offset, `SCOY` shifts center Y offfset, `SCSX` changes x or uniform scale factor, `SCSY` changes y scale factor. |
| 12 | k | `scale_1.5_1.5_center_0_0` | Tests `Paint(Var)ScaleUniform`. | `SCOX` shifts center x offset, `SCOY` shifts center Y offfset, `SCSX` changes x or uniform scale factor, `SCSY` changes y scale factor. |
| 13 | l | `scale_0.5_1.5_center_1000_1000` | Tests `Paint(Var)ScaleAroundCenter`. | `SCOX` shifts center x offset, `SCOY` shifts center Y offfset, `SCSX` changes x or uniform scale factor, `SCSY` changes y scale factor. |
| 14 | m | `scale_1.5_1.5_center_1000_1000` | Tests `Paint(Var)ScaleUniformAroundCenter`. | `SCOX` shifts center x offset, `SCOY` shifts center Y offfset, `SCSX` changes x or uniform scale factor, `SCSY` changes y scale factor. |
| 15 | n | `linear_gradient_extend_mode_pad` | Tests `Paint(Var)LinearGradient` with variable gradient coordinates or variable color lines. | `GRX0`, `GRY0`, `GRX1`, `GRY1`, `GRX2`, `GRY2`, `GRR0`, `GRR1` affect respective gradient coordinates. `COL1`, `COL2`, `COLR` shift color stops. |
| 16 | o | `linear_gradient_extend_mode_repeat` | Tests `Paint(Var)LinearGradient` with variable gradient coordinates or variable color lines. | `GRX0`, `GRY0`, `GRX1`, `GRY1`, `GRX2`, `GRY2`, `GRR0`, `GRR1` affect respective gradient coordinates. `COL1`, `COL2`, `COLR` shift color stops. |
| 17 | p | `linear_gradient_extend_mode_reflect` | Tests `Paint(Var)LinearGradient` with variable gradient coordinates or variable color lines. | `GRX0`, `GRY0`, `GRX1`, `GRY1`, `GRX2`, `GRY2`, `GRR0`, `GRR1` affect respective gradient coordinates. `COL1`, `COL2`, `COLR` shift color stops. |
| 18 | q | `radial_gradient_extend_mode_pad` | Tests `Paint(Var)RadialGradient` with variable gradient coordinates or variable color lines. | `GRX0`, `GRY0`, `GRX1`, `GRY1`, `GRX2`, `GRY2`, `GRR0`, `GRR1` affect respective gradient coordinates. `COL1`, `COL2`, `COLR` shift color stops. |
| 19 | r | `radial_gradient_extend_mode_repeat` | Tests `Paint(Var)RadialGradient` with variable gradient coordinates or variable color lines. | `GRX0`, `GRY0`, `GRX1`, `GRY1`, `GRX2`, `GRY2`, `GRR0`, `GRR1` affect respective gradient coordinates. `COL1`, `COL2`, `COLR` shift color stops. |
| 20 | s | `radial_gradient_extend_mode_reflect` | Tests `Paint(Var)RadialGradient` with variable gradient coordinates or variable color lines. | `GRX0`, `GRY0`, `GRX1`, `GRY1`, `GRX2`, `GRY2`, `GRR0`, `GRR1` affect respective gradient coordinates. `COL1`, `COL2`, `COLR` shift color stops. |
| 21 | t | `rotate_10_center_0_0` | Tests `Paint(Var)Rotate`. | `ROTA`: changes rotation angle. |
| 22 | u | `rotate_-10_center_1000_1000` | Tests `Paint(Var)RotateAroundCenter` with center at (1000, 1000).. | `ROTA`: changes rotation angle. |
| 23 | v | `rotate_25_center_500.0_500.0` | Tests `Paint(Var)RotateAroundCenter` with center at (500.0, 500.0).. | `ROTA`: changes rotation angle. |
| 24 | w | `rotate_-15_center_500.0_500.0` | Tests `Paint(Var)RotateAroundCenter` with center at (500.0, 500.0).. | `ROTA`: changes rotation angle. |
| 25 | x | `skew_25_0_center_0_0` | Tests `PaintSkew*` for x angle {x_skew_angle}, y angle {y_skew_angle}, x center {center_x}, y center {center_y}. | None |
| 26 | y | `skew_25_0_center_500.0_500.0` | Tests `PaintSkew*` for x angle {x_skew_angle}, y angle {y_skew_angle}, x center {center_x}, y center {center_y}. | None |
| 27 | z | `skew_0_15_center_0_0` | Tests `PaintSkew*` for x angle {x_skew_angle}, y angle {y_skew_angle}, x center {center_x}, y center {center_y}. | None |
| 28 | A | `skew_0_15_center_500.0_500.0` | Tests `PaintSkew*` for x angle {x_skew_angle}, y angle {y_skew_angle}, x center {center_x}, y center {center_y}. | None |
| 29 | B | `skew_-10_20_center_500.0_500.0` | Tests `PaintSkew*` for x angle {x_skew_angle}, y angle {y_skew_angle}, x center {center_x}, y center {center_y}. | None |
| 30 | C | `skew_-10_20_center_1000_1000` | Tests `PaintSkew*` for x angle {x_skew_angle}, y angle {y_skew_angle}, x center {center_x}, y center {center_y}. | None |
| 31 | D | `transform_matrix_1_0_0_1_125_125` | Tests `Paint(Var)Transform`. | `TRXX`, `TRXY`, `TRYX`, `TRYY`, `TRDX`, `TRDY` affect the individual transformation matrix coordinates. |
| 32 | E | `transform_matrix_1.5_0_0_1.5_0_0` | Tests `Paint(Var)Transform`. | `TRXX`, `TRXY`, `TRYX`, `TRYY`, `TRDX`, `TRDY` affect the individual transformation matrix coordinates. |
| 33 | F | `transform_matrix_0.9659_0.2588_-0.2588_0.9659_0_0` | Tests `Paint(Var)Transform`. | `TRXX`, `TRXY`, `TRYX`, `TRYY`, `TRDX`, `TRDY` affect the individual transformation matrix coordinates. |
| 34 | G | `transform_matrix_1.0_0.0_0.6_1.0_-300.0_0.0` | Tests `Paint(Var)Transform`. | `TRXX`, `TRXY`, `TRYX`, `TRYY`, `TRDX`, `TRDY` affect the individual transformation matrix coordinates. |
| 35 | H | `clip_box_top_left` | None | None |
| 36 | I | `clip_box_bottom_left` | None | None |
| 37 | J | `clip_box_bottom_right` | None | None |
| 38 | K | `clip_box_top_right` | None | None |
| 39 | L | `clip_box_center` | None | None |
| 40 | M | `composite_DEST_OVER` | Tests `PaintComposite` for mode DEST_OVER. | None |
| 41 | N | `composite_XOR` | Tests `PaintComposite` for mode XOR. | None |
| 42 | O | `composite_OVERLAY` | Tests `PaintComposite` for mode OVERLAY. | None |
| 43 | P | `composite_SRC_IN` | Tests `PaintComposite` for mode SRC_IN. | None |
| 44 | Q | `composite_PLUS` | Tests `PaintComposite` for mode PLUS. | None |
| 45 | R | `composite_LIGHTEN` | Tests `PaintComposite` for mode LIGHTEN. | None |
| 46 | S | `composite_MULTIPLY` | Tests `PaintComposite` for mode MULTIPLY. | None |
| 47 | T | `foreground_color_linear_alpha_1` | None | None |
| 48 | U | `foreground_color_radial_alpha_1` | None | None |
| 49 | V | `foreground_color_sweep_alpha_1` | None | None |
| 50 | W | `foreground_color_solid_alpha_1` | None | None |
| 51 | X | `foreground_color_linear_alpha_0.3` | None | None |
| 52 | Y | `foreground_color_radial_alpha_0.3` | None | None |
| 53 | Z | `foreground_color_sweep_alpha_0.3` | None | None |
| 54 | 0 | `foreground_color_solid_alpha_0.3` | None | None |
| 55 | 1 | `gradient_p2_skewed` | None | None |
| 56 | 2 | `colored_circles_v0` | None | None |
| 57 | 3 | `colored_circles_v1` | None | None |
| 58 | 4 | `sweep_0_90_pad_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 59 | 5 | `sweep_45_90_pad_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 60 | 6 | `sweep_247.5_292.5_pad_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 61 | 7 | `sweep_90_270_pad_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 62 | 8 | `sweep_-270_270_pad_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 63 | 9 | `sweep_-45_45_pad_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 64 | α | `sweep_315_45_pad_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 65 | β | `sweep_-360_0_reflect_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 66 | γ | `sweep_0_90_reflect_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 67 | δ | `sweep_45_90_reflect_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 68 | ε | `sweep_247.5_292.5_reflect_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 69 | ζ | `sweep_90_270_reflect_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 70 | η | `sweep_-270_270_reflect_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 71 | θ | `sweep_-45_45_reflect_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 72 | ι | `sweep_315_45_reflect_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 73 | κ | `sweep_-360_0_repeat_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 74 | λ | `sweep_0_90_repeat_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 75 | μ | `sweep_45_90_repeat_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 76 | ν | `sweep_247.5_292.5_repeat_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 77 | ξ | `sweep_90_270_repeat_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 78 | ο | `sweep_-270_270_repeat_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 79 | π | `sweep_-45_45_repeat_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 80 | ρ | `sweep_315_45_repeat_narrow` | Tests `Paint(Var)SweepGradient`. | `SWPS` shifts sweep start angle, `SWPE` shifts sweep end angle. |
| 81 | ς | `solid_colorline_alpha` | Tests variable alpha in linear gradient color stops, and in PaintVarSolid. | `APH1` affects PaintVarSolid alpha, `APH2` and `APH3` modify linear gradient alpha values. |
| 82 | + | `cross_glyph` | None | None |
| 83 | ▀ | `upem_box_glyph` | None | None |
| 84 | σ | `clip_shade_center` | None | None |
| 85 | τ | `clip_shade_top_left` | None | None |
| 86 | υ | `clip_shade_bottom_left` | None | None |
| 87 | φ | `clip_shade_bottom_right` | None | None |
| 88 | χ | `clip_shade_top_right` | None | None |
| 89 | ψ | `inset_clipped_radial_reflect` | None | None |
| 90 | Α | `circle_r50` | None | None |
| 91 | Β | `circle_r100` | None | None |
| 92 | Γ | `circle_r150` | None | None |
| 93 | Δ | `circle_r200` | None | None |
| 94 | Ε | `circle_r250` | None | None |
| 95 | Ζ | `circle_r300` | None | None |
| 96 | Η | `circle_r350` | None | None |
| 97 | Θ | `one` | None | None |
| 98 | Ι | `zero` | None | None |
