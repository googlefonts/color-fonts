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

fmt="$1"
name="$2"
shift 2
inputs="$@"

if [[ $fmt = cff* ]]
then
	ext="otf"
else
	ext="ttf"
fi

nanoemoji --color_format $fmt \
	--output_file fonts/$name-$fmt.$ext \
	--build_dir build/$name \
	$inputs > /tmp/$name-$fmt.$ext.log 2>&1 \
	|| echo "ERROR; see /tmp/$name-$fmt.$ext.log"
