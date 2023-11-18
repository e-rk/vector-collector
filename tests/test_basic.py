import unittest
import shutil
from pathlib import Path
import subprocess
import time
from contextlib import suppress
import os

from datetime import datetime
from veccol.processor import process_capture
from veccol.types import Spec
from veccol.runner import Runner

def build_test_app(path: Path) -> None:
    make = shutil.which("make")
    if make is None:
        raise RuntimeError("make not found")
    runner = subprocess.run([make], cwd=path)

class TestBasicOperation(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        build_test_app(Path("./tests/data"))

    def test_vector_collection(self) -> None:
        spec = None
        datestr = datetime.now().strftime("%Y%m%d-%H%M%S")
        outdir = Path("captures", datestr)
        logname = Path(outdir, "capture.log")
        with suppress(FileExistsError):
            os.makedirs(outdir)
        with open("./tests/data/spec.yaml") as f:
            spec = Spec.from_yaml(f.read())
        runner = Runner(spec)
        runner.run(logname=logname)
        time.sleep(spec.config.timeout)
        process_capture(spec, logname, outdir)

if __name__ == '__main__':
    unittest.main()
