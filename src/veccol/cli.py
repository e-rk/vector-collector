#
# Copyright (c) 2023 Rafał Kuźnia <rafal.kuznia@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import click
import logging
import time
from veccol.types import Spec

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

@click.command()
def collect() -> None:
    with open("tests/basic/data/spec.yaml") as f:
        spec = Spec.from_yaml(f.read())
        print(spec)
