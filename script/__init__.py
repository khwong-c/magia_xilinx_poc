from pathlib import Path

from .xilinx import run_vivado


def cleanup():
    Path("src/generated").mkdir(parents=True, exist_ok=True)

    # Remove previous generated files
    old_sv = list(Path("src/generated").rglob("*.sv"))
    for file in old_sv:
        file.unlink()

    # Remove Existing output directory
    old_output = list(Path("output").rglob("*"))
    for file in old_output:
        file.unlink()


__all__ = ["run_vivado", "cleanup"]
