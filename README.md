[![CI Build Status](https://github.com/googlefonts/color-fonts/workflows/Continuous%20Test%20+%20Deploy/badge.svg)](https://github.com/googlefonts/color-fonts/actions/workflows/ci.yml?query=workflow%3ATest)

# color-fonts
Experimental color font builds. Intended to help verify font toolchain builds things that work with consuming tools for COLRv1 ([colr gradients spec](https://github.com/googlefonts/colr-gradients-spec/blob/main/colr-gradients-spec.md)).

To update the fonts:

```bash
# Setup environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# If config needs to be updated
python generate_config.py


# To generate fonts with a config; ~30 minutes on a fairly fast desktop
time nanoemoji config/*.toml
cp -v build/*.[ot]tf fonts/

# To generate additional samples (covering space nanoemoji doesn't)
python config/more_samples-glyf_colr_1.py fonts/

# Commit, etc
```

Related:

*   [nanoemoji](https://github.com/googlefonts/nanoemoji), compiles a set of picosvg into a color font 
*   [picosvg](https://github.com/googlefonts/picosvg), simplifies svgs to use only a small subset of the full spec
