#
# Copyright (c) 2023 Rafał Kuźnia <rafal.kuznia@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from veccol.types import Spec, Collect
from pathlib import Path
from itertools import chain
import csv

def process_collection(spec: Spec, data: list[str], collect: Collect) -> None:
    name = collect.name
    value_name = [v.name for v in chain.from_iterable(p.values for p in collect.points)]
    csvfile = None
    with open(f"{name}.csv", "w", newline='') as f:
        csvfile = csv.DictWriter(f, fieldnames=value_name)
        our_lines = filter(lambda x: x.startswith(name), data)
        removed_prefix = map(lambda x: x.removeprefix(f"{name}:"), our_lines)
        split_lines = map(lambda x: x.strip().split(","), removed_prefix)
        to_dict = list(map(lambda x: dict(zip(value_name, x)), split_lines))
        csvfile.writeheader()
        csvfile.writerows(to_dict)

def process_capture(spec: Spec, file: Path) -> None:
    lines = []
    with open(file) as f:
        lines = f.readlines()
    for c in spec.config.collect:
        process_collection(spec, lines, c)
