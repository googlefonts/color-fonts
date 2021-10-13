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

# Rebuild samples whose configurations are specified on cli. Runs all
# requested builds in parallel.
#
# Example:
#     ./build.py config/twemoji-*

import os
from pathlib import Path
import shutil
import subprocess
import sys
import time


def main():
    self_dir = Path(__file__).parent
    build_dir = Path("build").resolve()
    if build_dir.exists():
        shutil.rmtree(build_dir)

    font_dir = Path("fonts").resolve()
    config_dir = self_dir / "config"
    font_srcs_dir = self_dir / "font-srcs"

    assert config_dir.is_dir()
    assert font_srcs_dir.is_dir()

    run_me = []

    setup_start = time.monotonic()
    for config in sys.argv[1:]:
        config = Path(config).resolve()
        working_dir = self_dir / "build" / config.stem
        working_dir.mkdir(parents=True)

        os.symlink(config_dir, working_dir / config_dir.name)
        os.symlink(font_srcs_dir, working_dir / font_srcs_dir.name)

        if config.suffix == ".toml":
            cmd = ("nanoemoji", "--config", str(config))
        elif config.suffix == ".py":
            cmd = (sys.executable, str(config.resolve()), str(build_dir.resolve()))
        else:
            raise ValueError(f"Not sure how to handle {config}")

        run_me.append((working_dir, cmd))

    spawn_start = time.monotonic()
    procs = [
        subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            cwd=working_dir,
            text=True,
        )
        for working_dir, cmd in run_me
    ]
    for proc, (working_dir, cmd) in zip(procs, run_me):
        stdout, stderr = proc.communicate()
        with open(working_dir / "stdout", "w") as f:
            if stdout is not None:
                f.write(stdout)
        with open(working_dir / "stderr", "w") as f:
            if stderr is not None:
                f.write(stderr)

        cmd_str = " ".join(cmd)
        if proc.returncode == 0:
            print(f"{cmd_str} succeeded")
            working_build_dir = working_dir / "build"
            font_files = tuple(working_build_dir.glob("*.[ot]tf"))
            assert (
                len(font_files) == 1
            ), f"Expected exactly 1 font file in {working_build_dir}, found {font_files}"
            src, dst = font_files[0], font_dir / font_files[0].name
            shutil.copy(src, dst)
            print(src, "=>", dst)
        else:
            print(f"{cmd_str} failed, see {working_dir.relative_to(self_dir)} for logs")

        print(" ".join(cmd))  # very useful on failure
        before_rmtree = time.monotonic()
    done = time.monotonic()

    print(f"{spawn_start - setup_start:.1f}s to setup")
    print(f"{done - spawn_start:.1f}s to execute")


if __name__ == "__main__":
    main()
