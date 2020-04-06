#!/bin/bash -x

set -e

git submodule init
git submodule update

git submodule foreach git pull origin master

[ ! -d "venv" ] && python3 -m venv venv

source venv/bin/activate

pip install -e nanoemoji/

which nanoemoji  # sanity check

# Handwriting
nanoemoji --color_format colr_1 \
	--output_file fonts/handwriting-colr_1.ttf \
	$(find ../noto-emoji/svg -name 'emoji_u270d*.svg')
