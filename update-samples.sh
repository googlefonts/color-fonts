#!/bin/bash -x

set -e

git submodule init
git submodule update

git submodule foreach git pull origin master

[ ! -d "venv" ] && python3 -m venv venv

source venv/bin/activate

# don't have pip + versions currently; just grab latest
pip install -e nanoemoji/
pip install -e nanosvg/

which nanoemoji  # sanity check

# Noto Emoji Handwriting
# https://rsheeter.github.io/android_fonts/emoji.html?q=u:270d
nanoemoji --color_format colr_1 \
	--output_file fonts/noto-handwriting-colr_1.ttf \
	$(find font-srcs/noto-emoji/svg -name 'emoji_u270d*.svg')

# Twemoji Smileys, these but twemoji:
# https://rsheeter.github.io/android_fonts/emoji.html?q=note:smi
nanoemoji --color_format colr_1 \
	--output_file fonts/twemoji-smiley-colr_1.ttf \
	font-srcs/twemoji/assets/svg/263a.svg \
	font-srcs/twemoji/assets/svg/1f60{1,3,4,5,6,7,8,a,d,e,f}.svg \
	font-srcs/twemoji/assets/svg/1f619.svg \
	font-srcs/twemoji/assets/svg/1f63{8,a,b,c}.svg \
	font-srcs/twemoji/assets/svg/1f642.svg \
	font-srcs/twemoji/assets/svg/1f970.svg
