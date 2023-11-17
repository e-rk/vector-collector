import unittest
import shutil
from pathlib import Path
import subprocess

def build_test_app(path: Path) -> None:
    make = shutil.which("make")
    if make is None:
        raise RuntimeError("make not found")
    runner = subprocess.run([make], cwd=path)



class TestBasicOperation(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        build_test_app(Path("./data"))

    def test_vector_collection(self) -> None:
        pass

if __name__ == '__main__':
    unittest.main()
