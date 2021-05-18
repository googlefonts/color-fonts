#!/usr/bin/env python3

from pathlib import Path
import csv
import fontTools.ttLib.woff2
import functools
import io
import itertools
import logging
import math
import multiprocessing
import sys
import argparse

FONT_BASE_NAMES = {
    "noto": "Noto Color Emoji",
    "noto_flags": "Noto Color Emoji Flags only",
    "noto_handwriting": "Noto Color single Handwriting emoji",
    "twemoji": "Twemoji",
    "twemoji_smiley": "Twemoji single Smiley Emoji",
    "samples": "Samples test font",
}
FORMAT_DICT = {
    "cff2_colr_1": "binary vectors (cff2)",
    "cff_colr_1": "binary vectors (cff)",
    "glyf_colr_1": "binary vectors (glyf)",
    "picosvg": "picosvg",
    "picosvgz": "compressed picosvg",
    "untouchedsvg": "svg",
    "untouchedsvgz": "svgz",
}


def file_sizes_for_file(file_name):
    p = Path(file_name)
    if not p.is_file():
        return None
    compressed_file = io.BytesIO()
    fontTools.ttLib.woff2.compress(file_name, compressed_file)
    return {
        "sfnt_uncompressed": p.stat().st_size,
        "woff2": len(compressed_file.getvalue()),
    }


def compare_sizes(name_format, noto_cbdt_path=None):
    (name, format) = name_format
    if format == "cbdt":
        # Use parent cbdt file pathname.
        assert noto_cbdt_path is not None
        return (name, format, file_sizes_for_file(noto_cbdt_path))
    file_name = f"fonts/{name}-{format}.{'o' if 'cff' in format else 't'}tf"
    return (name, format, file_sizes_for_file(file_name))


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--noto-cbdt", help="Provide a path for Noto Color Emoji as bitmap font."
    )
    parsed_args = parser.parse_args()
    noto_cbdt_path = None
    if parsed_args.noto_cbdt and Path(parsed_args.noto_cbdt).is_file():
        noto_cbdt_path = parsed_args.noto_cbdt

    files = list(itertools.product(FONT_BASE_NAMES, FORMAT_DICT))

    if noto_cbdt_path:
        files.insert(0, ("noto", "cbdt"))
        FORMAT_DICT["cbdt"] = "CBDT/CBLC bitmap"
    else:
        logging.getLogger().warning(
            "Not adding Noto Color Emoji bitmap info to result."
        )

    partial_compare_sizes = functools.partial(
        compare_sizes, noto_cbdt_path=noto_cbdt_path
    )
    with multiprocessing.Pool(math.floor(multiprocessing.cpu_count() * 0.75)) as p:
        size_results = p.map(partial_compare_sizes, files)
    csv_file = io.StringIO()
    field_names = ["font", "format", "uncompressed_sfnt_size", "woff2_size"]
    writer = csv.DictWriter(csv_file, field_names)
    writer.writeheader()

    for size_result in size_results:
        row_dict = {
            "font": FONT_BASE_NAMES[size_result[0]],
            "format": FORMAT_DICT[size_result[1]],
            "uncompressed_sfnt_size": size_result[2]["sfnt_uncompressed"],
            "woff2_size": size_result[2]["woff2"],
        }
        writer.writerow(row_dict)

    print(csv_file.getvalue())
