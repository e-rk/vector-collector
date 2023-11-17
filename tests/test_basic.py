import unittest
import shutil
from pathlib import Path
import subprocess
import time

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
        with open("./tests/data/spec.yaml") as f:
            spec = Spec.from_yaml(f.read())
        runner = Runner(spec)
        runner.run()
        time.sleep(spec.config.timeout)
        process_capture(spec, Path("capture.log"))

if __name__ == '__main__':
    unittest.main()
