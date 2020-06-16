#!/bin/bash -x
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

# Starting to feel like we should move to make

set -e

function prebuild() {
	[ ! -d "venv" ] && python3 -m venv venv

	source venv/bin/activate

	# upgrade eagerly so that all dependencies are updated regardless of whether
	# the currently installed version satisfies the requirement of the upgraded package.
	pip install --upgrade --upgrade-strategy "eager" nanoemoji

	which nanoemoji  # sanity check
}

function compile_small_samples() {
	# Sample sets
	local noto_handwriting_svgs=$(find font-srcs/noto-emoji/svg -name 'emoji_u270d*.svg')

	local twemoji_smiley_svgs="$(echo font-srcs/twemoji/assets/svg/{263a,1f619,1f642,1f970}.svg)"
	twemoji_smiley_svgs="$twemoji_smiley_svgs $(echo font-srcs/twemoji/assets/svg/1f60{1,3,4,5,6,7,8,a,d,e,f}.svg)"
	twemoji_smiley_svgs="$twemoji_smiley_svgs $(echo font-srcs/twemoji/assets/svg/1f63{8,a,b,c}.svg)"

	# Noto Emoji Handwriting
	# https://rsheeter.github.io/android_fonts/emoji.html?q=u:270d
	nanoemoji --color_format glyf_colr_1 \
		--output_dir fonts \
		--output_file noto-handwriting-colr_1.ttf \
		$noto_handwriting_svgs

	nanoemoji --color_format svg \
		--output_dir fonts \
		--output_file noto-handwriting-svg.ttf \
		$noto_handwriting_svgs

	nanoemoji --color_format svgz \
		--output_dir fonts \
		--output_file noto-handwriting-svgz.ttf \
		$noto_handwriting_svgs


	# Twemoji Smileys, these but twemoji:
	# https://rsheeter.github.io/android_fonts/emoji.html?q=note:smi
	# Use COLRv0 since these don't use any gradiants
	nanoemoji --color_format glyf_colr_0 \
		--output_dir fonts \
		--output_file twemoji-smiley-colr_0.ttf \
		$twemoji_smiley_svgs

	nanoemoji --color_format svg \
		--output_dir fonts \
		--output_file twemoji-smiley-svg.ttf \
		$twemoji_smiley_svgs

	nanoemoji --color_format svgz \
		--output_dir fonts \
		--output_file twemoji-smiley-svgz.ttf \
		$twemoji_smiley_svgs

	# SVG files from repo
	# Name becomes the ligature to reach, e.g. radial.svg is a glyph activated by
	# the string "radial"

	# rename input files
	tmp_dir=$(mktemp -d)
	find font-srcs/samples -name '*.svg' -execdir cp {} "$tmp_dir/" ';'
	ls $tmp_dir
	python rename.py "$tmp_dir"
	samples_svgs=$(find "$tmp_dir" -name '*.svg')

	nanoemoji --color_format glyf_colr_0 \
		--output_dir fonts \
		--output_file samples-colr_0.ttf \
		$samples_svgs

	nanoemoji --color_format glyf_colr_1 \
		--output_dir fonts \
		--output_file samples-colr_1.ttf \
		$samples_svgs

	nanoemoji --color_format svg \
		--output_dir fonts \
		--output_file samples-svg.ttf \
		$samples_svgs

	nanoemoji --color_format svgz \
		--output_dir fonts \
		--output_file samples-svgz.ttf \
		$samples_svgs
}

function compile_noto_emoji() {
	time nanoemoji --color_format glyf_colr_1 \
		--output_dir fonts \
		--output_file noto-emoji-colr_1.ttf \
		$(find font-srcs/noto-emoji/svg -name '*.svg')
}

function compile_twemoji() {
	time nanoemoji --color_format glyf_colr_1 \
		--output_dir fonts \
		--output_file twemoji-colr_1.ttf \
		$(find font-srcs/twemoji/assets/svg/ -name '*.svg')
}

function usage() {
	echo "Usage: -t target"
	echo ""
	echo "-t one of small_samples, noto_emoji, twemoji"
}

target=""
while getopts "t:" opt; do
  case $opt in
  t)  target="$OPTARG"
    ;;
  \?) echo "Invalid arg: -$OPTARG"
      usage
      exit 1
      ;;
  esac
done

case "$target" in
  small_samples)
	prebuild
	compile_small_samples
    ;;
  noto_emoji)
	prebuild
	compile_noto_emoji
    ;;
  twemoji)
	prebuild
	compile_twemoji
    ;;
  *)  set +x
      echo "Invalid target $target"
      usage
      exit 1
    ;;
esac
