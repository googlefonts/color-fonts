#!/usr/bin/env python3

import fontTools.ttLib.ttFont as ttFont
import fontTools.ttLib.tables.C_O_L_R_ as C_O_L_R_

SRC_FONT = "fonts/noto-glyf_colr_1.ttf"
SAMPLES_FONT = "fonts/more_samples-glyf_colr_1.ttf"
NUM_TOP_BUSY_PAINTS = 90

ttfont = ttFont.TTFont(SRC_FONT)

glyphs_paintcount = []
for g in ttfont["COLR"].table.BaseGlyphList.BaseGlyphPaintRecord:
    counter = 0

    def traversePaint(paint):
        global counter
        counter += 1

    g.Paint.traverse(ttfont["COLR"].table, traversePaint)
    glyphs_paintcount.append((ttfont.getGlyphID(g.BaseGlyph), counter))

glyphs_paintcount = sorted(glyphs_paintcount, key=lambda x: x[1], reverse=True)

high_paint_count_glyphs = [g[1] for g in glyphs_paintcount[0:NUM_TOP_BUSY_PAINTS]]


def chunks_of_three(gid_list):
    chunksize = 3
    for i in range(0, len(gid_list), chunksize):
        yield gid_list[i : i + chunksize]


for count, chunk in enumerate(chunks_of_three(high_paint_count_glyphs)):
    gids = ",".join([str(item) for item in chunk])
    print(
        f"pyftsubset {SRC_FONT} --gids={gids} --output-file=noto_complex_glyphs_colrv1_{str(count)}.ttf"
    )

ttfont = ttFont.TTFont(SAMPLES_FONT)
samples_gids = [
    ttfont.getGlyphID(glyph_name.BaseGlyph)
    for glyph_name in ttfont["COLR"].table.BaseGlyphList.BaseGlyphPaintRecord
]

for count, chunk in enumerate(chunks_of_three(samples_gids)):
    gids = ",".join([str(item) for item in chunk])
    print(
        f"pyftsubset {SAMPLES_FONT} --gids={gids} --output-file=more_samples-glyf_colrv1_{str(count)}.ttf"
    )
