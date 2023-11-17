#
# Copyright (c) 2023 Rafał Kuźnia <rafal.kuznia@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import click
import shutil
import signal
import logging
import time
from subprocess import Popen, PIPE
from threading import Thread

from veccol.types import Spec

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

class Gdb:
    def __init__(self) -> None:
        path = shutil.which("gdb")
        if path is None:
            raise RuntimeError("GDB executable not found")
        self.gdb = Popen([path, "-q"], 
                         stdin=PIPE, 
                         stdout=PIPE, 
                         text=True,
                         universal_newlines=True)
        self.stdout_thread = Thread(target=self._read_thread)
        self.stdout_thread.start()

    def _read_thread(self) -> None:
        while (True):
            s = self.read()
            logger.info(s)

    def send_command(self, command: str) -> None:
        logger.debug(f"Sending: {command}")
        self.gdb.stdin.write(f"{command}\n")

    def connect(self, remote: str) -> None:
        logger.debug(f"Connecting to remote: {remote}")
        self.send_command(f"target remote {remote}")

    def sigint(self) -> None:
        self.gdb.send_signal(signal.SIGINT)

    def cont(self) -> None:
        self.send_command("continue")

    def read(self) -> str:
        return self.gdb.stdout.read()

@click.command()
def collect() -> None:
    with open("tests/basic/data/spec.yaml") as f:
        spec = Spec.from_yaml(f.read())
        print(spec)
