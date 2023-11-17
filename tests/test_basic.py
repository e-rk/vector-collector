import unittest
import shutil
from pathlib import Path
import subprocess

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
        with open("./tests/data/spec.yaml") as f:
            spec = Spec.from_yaml(f.read())
            runner = Runner(spec)
            runner.run()
            print(spec)
            exit(1)

if __name__ == '__main__':
    unittest.main()
