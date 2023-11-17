#
# Copyright (c) 2023 Rafał Kuźnia <rafal.kuznia@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import click
import logging
import time
from pathlib import Path
from veccol.types import Spec
from typing import TextIO
from veccol.runner import Runner
from veccol.processor import process_capture

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

@click.command()
@click.argument("spec", type=click.File())
@click.option("--timeout", type=int)
def collect(_spec: TextIO, timeout: int) -> None:
    spec = Spec.from_yaml(_spec.read())
    runner = Runner(spec)
    runner.run()
    if timeout:
        time.sleep(timeout)
    else:
        time.sleep(spec.config.timeout)
    process_capture(spec, Path("capture.txt"))

