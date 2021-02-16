[![Travis Build Status](https://travis-ci.org/googlefonts/color-fonts.svg?branch=main)](https://travis-ci.org/googlefonts/color-fonts)

# color-fonts
Experimental color font builds. Intended to help verify font toolchain builds things that work with consuming tools for COLRv1 ([colr gradients spec](https://github.com/googlefonts/colr-gradients-spec/blob/main/colr-gradients-spec.md)).

To update the fonts:

1.  Run [generate_config.py](https://github.com/googlefonts/color-fonts/blob/main/generate_config.py) if the config needs to be updated
1.  Run [build.py](https://github.com/googlefonts/color-fonts/blob/main/build.py) to generate the font(s) you want to update

Related:

*   [nanoemoji](https://github.com/googlefonts/nanoemoji), compiles a set of picosvg into a color font 
*   [picosvg](https://github.com/googlefonts/picosvg), simplifies svgs to use only a small subset of the full spec
