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
from datetime import datetime
from contextlib import suppress
import os

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

@click.command()
@click.argument("specfile", type=click.File())
@click.option("--timeout", type=int)
@click.option("--cfilter", "-f", type=str, multiple=True)
def collect(specfile: TextIO, timeout: int, cfilter: list[str]) -> None:
    spec = Spec.from_yaml(specfile.read())
    spec.config.collect = list(filter(
            lambda x: x.name in cfilter or not cfilter,
            spec.config.collect))
    logger.error(spec.config.collect)
    datestr = datetime.now().strftime("%Y%m%d-%H%M%S")
    logname = Path(f"{datestr}.log")
    outdir = Path("captures", datestr)
    with suppress(FileExistsError):
        os.makedirs(outdir)
    runner = Runner(spec)
    runner.run(logname=logname)
    if timeout:
        time.sleep(timeout)
    else:
        time.sleep(spec.config.timeout)
    process_capture(spec, logname, outdir)

@click.command()
@click.argument("specfile", type=click.File())
@click.argument("capturefile", type=click.Path(path_type=Path))
def process(specfile: Spec, capturefile: Path) -> None:
    spec = Spec.from_yaml(specfile.read())
    outdir = capturefile.parent
    process_capture(spec, capturefile, outdir)
