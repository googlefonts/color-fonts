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

	pip install --upgrade pip setuptools wheel
	pip install -r requirements.txt

	which nanoemoji  # sanity check
}

function compile_small_samples() {
	# Sample sets
	local noto_handwriting_svgs=$(find font-srcs/noto-emoji/svg -name 'emoji_u270d*.svg')

	local twemoji_smiley_svgs="$(echo font-srcs/twemoji/assets/svg/{263a,1f619,1f642,1f970}.svg)"
	twemoji_smiley_svgs="$twemoji_smiley_svgs $(echo font-srcs/twemoji/assets/svg/1f60{1,3,4,5,6,7,8,a,d,e,f}.svg)"
	twemoji_smiley_svgs="$twemoji_smiley_svgs $(echo font-srcs/twemoji/assets/svg/1f63{8,a,b,c}.svg)"

	# SVG files from repo
	# Name becomes the ligature to reach, e.g. radial.svg is a glyph activated by
	# the string "radial"

	# rename input files
	local tmp_dir=$(mktemp -d)
	find font-srcs/samples -name '*.svg' -execdir cp {} "$tmp_dir/" ';'
	python rename.py "$tmp_dir"
	local samples_svgs=$(find "$tmp_dir" -name '*.svg')

	# compile each sample set in each format
	for fmt in glyf_colr_1 cff_colr_1 cff2_colr_1 picosvg picosvgz untouchedsvg untouchedsvgz; do
		# Noto Emoji Handwriting
		# https://rsheeter.github.io/android_fonts/emoji.html?q=u:270d
		./compile.sh $fmt noto-handwriting $noto_handwriting_svgs

		# Twemoji Smileys, these but twemoji:
		# https://rsheeter.github.io/android_fonts/emoji.html?q=note:smi
		# Use COLRv0 since these don't use any gradiants
		./compile.sh $fmt twemoji-smiley $twemoji_smiley_svgs

		# Sample files from repo
		./compile.sh $fmt samples $samples_svgs
	done
}

function compile_noto_emoji() {
	local fmt="$1"
	local svgs="$(find font-srcs/noto-emoji/svg -name '*.svg')"
	# filter out input SVGs in the blocklist
	local svgs="$(echo "$svgs" | tr ' ' '\n' | fgrep -vf BLOCKLIST.txt)"
	./compile.sh $fmt noto-emoji $svgs
}

function compile_twemoji() {
	local fmt="$1"
	local svgs="$(find font-srcs/twemoji/assets/svg/ -name '*.svg')"
	./compile.sh $fmt twemoji $svgs
}

function build() {
	local target="$1"
	local pids=""
	case "$target" in
	  small_samples)
		prebuild
		compile_small_samples
	    ;;
	  twemoji)
		prebuild
		compile_twemoji picosvg
		compile_twemoji picosvgz
		compile_twemoji untouchedsvg
		compile_twemoji untouchedsvgz
		compile_twemoji glyf_colr_0
		compile_twemoji cff_colr_0
		compile_twemoji cff2_colr_0
		compile_twemoji glyf_colr_1
		compile_twemoji cff_colr_1
		compile_twemoji cff2_colr_1
	    ;;
	  noto_emoji)
		prebuild
		compile_noto_emoji picosvg
		compile_noto_emoji picosvgz
		compile_noto_emoji untouchedsvg
		compile_noto_emoji untouchedsvgz
		compile_noto_emoji glyf_colr_1
		compile_noto_emoji cff_colr_1
		compile_noto_emoji cff2_colr_1
	    ;;
	  *)  set +x
	      echo "Invalid target $target"
	      usage
	      exit 1
	    ;;
	esac
}

function usage() {
	echo "Usage: -t target"
	echo ""
	echo "-t one of:"
	echo "     small_samples"
	echo "     noto_emoji"
	echo "     twemoji"
}

target=""
while getopts "t:f:" opt; do
  case $opt in
  t)  target="$OPTARG"
    ;;
  \?) echo "Invalid arg: -$OPTARG"
      usage
      exit 1
      ;;
  esac
done

build "$target"

