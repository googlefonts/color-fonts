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

import os
import sys

dirpath = sys.argv[1]
for f in os.listdir(dirpath):
  root, ext = os.path.splitext(f)
  old = os.path.join(dirpath, f)
  new = os.path.join(dirpath, '-'.join([f'{ord(c):x}' for c in root]) + ext)
  print(f'{old} -> {new}')
  os.rename(old, new)