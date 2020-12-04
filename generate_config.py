# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Generate config files for samples

from nanoemoji.util import rel
from pathlib import Path
import shutil
import tempfile
import textwrap
from typing import Iterable

_COLOR_FORMATS = (
    "glyf_colr_1",
    "cff_colr_1",
    "cff2_colr_1",
    "picosvg",
    "picosvgz",
    "untouchedsvg",
    "untouchedsvgz",
)
_SAMPLE_SVG_DIR = Path("font-srcs/samples")
_NOTO_SVG_DIR = Path("font-srcs/noto-emoji/svg")
_NOTO_SVG_FLAG_DIR = Path("font-srcs/noto-emoji/third_party/waved-flags/svg")
_TWEMOJI_SVG_DIR = Path("font-srcs/twemoji/assets/svg")
_CONFIG_DIR = Path("config")


def _denied_files(prefix):
    denyfile = Path(f"{prefix}-denylist.txt")
    if not denyfile.is_file():
        print(f"No denied files for {prefix} ({denyfile})")
        return set()
    print(f"Loading {denyfile}")
    return {l.strip() for l in denyfile.open() if l.strip()}


def _write_configs(prefix, color_formats, svg_files):
    denied_files = _denied_files(prefix)
    svg_files = [rel(_CONFIG_DIR, Path(f)) for f in svg_files if f.name not in denied_files]
    for color_format in color_formats:
        font_ext = ".ttf"
        if color_format.startswith("cff"):
            font_ext = ".otf"
        name = f"{prefix}-{color_format}"
        config_file = f"{name}.toml"
        for svg_file in svg_files:
            assert _CONFIG_DIR.joinpath(svg_file).is_file(), f"{svg_file} not found relative to {_CONFIG_DIR}"
        svg_list = ", ".join(f"\"{f}\"" for f in sorted(svg_files))
        with open(_CONFIG_DIR / config_file, "w") as f:
            f.write(textwrap.dedent(f"""
                family = "{name}"
                output_file = "{name}{font_ext}"
                color_format = "{color_format}"

                [axis.wght]
                name = "Weight"
                default = 400

                [master.regular]
                style_name = "Regular"
                srcs = [{svg_list}]

                [master.regular.position]
                wght = 400
                """))


def _write_noto_handwriting_configs():
    svgs = tuple(_NOTO_SVG_DIR.glob("emoji_u270d*.svg"))
    _write_configs("noto_handwriting", _COLOR_FORMATS, svgs)


def _write_twemoji_smiley_configs():
    svgs = tuple(_TWEMOJI_SVG_DIR / (f + ".svg") for f in (
        "263a",
        "1f619",
        "1f642",
        "1f970",
        "1f601",
        "1f603",
        "1f604",
        "1f605",
        "1f606",
        "1f607",
        "1f608",
        "1f60a",
        "1f60d",
        "1f60e",
        "1f60f"
    ))
    _write_configs("twemoji_smiley", _COLOR_FORMATS, svgs)


def _write_sample_configs():
    # hand crafted sample svgs, filename is activation ligature
    sample_tmp = Path("config/renamed_samples")
    sample_tmp.mkdir(parents=True, exist_ok=True)
    originals = tuple(_SAMPLE_SVG_DIR.glob("*.svg"))
    svgs = tuple(sample_tmp / ('-'.join([f'{ord(c):x}' for c in s.stem]) + s.suffix) for s in originals)
    for src, dst in zip(originals, svgs):
        shutil.copy(src, dst)
    _write_configs("samples", _COLOR_FORMATS, svgs)


def _write_all_noto_configs():
    svgs = tuple(_NOTO_SVG_DIR.glob("*.svg")) + tuple(_NOTO_SVG_FLAG_DIR.glob("*.svg"))
    _write_configs("noto", _COLOR_FORMATS, svgs)


def _write_all_twemoji_configs():
    svgs = tuple(_TWEMOJI_SVG_DIR.glob("*.svg"))
    _write_configs("twemoji", _COLOR_FORMATS, svgs)


def main():
    _write_sample_configs()
    _write_noto_handwriting_configs()
    _write_twemoji_smiley_configs()
    _write_all_noto_configs()
    _write_all_twemoji_configs()


if __name__ == "__main__":
    main()
