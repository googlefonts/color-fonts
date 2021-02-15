#!/usr/bin/env python3
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

# Rebuild samples whose configurations are specified on cli
# Example:
#     ./build.py config/twemoji-*

from pathlib import Path
import shutil
import subprocess
import sys
import time

def main():
    build_dir = Path("build")
    font_dir = Path("fonts")
    for config in sys.argv[1:]:
        config = Path(config)
        cmd = (
            "nanoemoji",
            "--config",
            str(config)
        )
        print(" ".join(cmd))  # very useful on failure
        before_rmtree = time.monotonic()
        if build_dir.exists():
            shutil.rmtree(build_dir)
        after_rmtree = time.monotonic()
        subprocess.run(cmd, check=True)
        after_nanoemoji = time.monotonic()
        font_files = tuple(build_dir.glob("*.[ot]tf"))
        assert len(font_files) == 1
        src, dst = font_files[0], font_dir / (config.stem + font_files[0].suffix)
        shutil.copy(src, dst)
        print(f"{after_rmtree - before_rmtree:.1f}s to delete build/")
        print(f"{after_nanoemoji - after_rmtree:.1f}s to run {' '.join(cmd)}")


if __name__ == "__main__":
    main()
