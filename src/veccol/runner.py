#
# Copyright (c) 2023 Rafał Kuźnia <rafal.kuznia@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from veccol.types import Spec
from typing import TextIO
import tempfile
import shutil
from subprocess import run
from more_itertools import mark_ends
from itertools import chain
from pathlib import Path
import time
import os

class Runner:
    def __init__(self, spec: Spec):
        self.spec = spec

    def write(self, file: TextIO, command):
        file.write(f"{command}\n")

    def _make_temp(self) -> TextIO:
        return tempfile.NamedTemporaryFile(mode="w+")

    def _generate_script(self, logname: Path) -> TextIO:
        file = self._make_temp()
        for command in self.spec.pre_config.commands:
            self.write(file, command)
            self.write(file, "set logging redirect on")
            self.write(file, f"set logging file {logname}")
            self.write(file, "set logging on")
        for col in self.spec.config.collect:
            prefix = col.name
            for is_first, is_last, point in mark_ends(col.points):
                self.write(file, f"b {point.locspec}")
                self.write(file, "commands")
                self.write(file, "silent")
                for value in point.values:
                    value_name = f"{prefix}_{value.name}"
                    self.write(file, f"set ${value_name} = {value.expr}")
                if is_last or point.force_capture:
                    all_values = list(chain.from_iterable(p.values for p in col.points))
                    names = [f"${prefix}_{v.name}" for v in all_values]
                    formats = [v.format for v in all_values]
                    name_str = ",".join(names)
                    format_str = ",".join(formats)
                    self.write(file, f"printf \"{prefix}:{format_str}\\n\",{name_str}")
                    pass
                self.write(file, "continue")
                self.write(file, "end")
        for command in self.spec.post_config.commands:
            self.write(file, command)
        file.flush()
        return file

    def run(self, logname: Path) -> None:
        file = self._generate_script(logname=logname)
        gdb = shutil.which("gdb")
        if gdb is None:
            raise RuntimeError("GDB executable not found")
        os.system(f"{gdb} -x {file.name} &")
        time.sleep(1)

