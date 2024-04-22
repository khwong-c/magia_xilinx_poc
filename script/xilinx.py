import os
import subprocess
from functools import cache
from tempfile import NamedTemporaryFile
from typing import Literal

from script.tcl_script import impl_script, program_script


@cache
def xilinx_env(xilinx_vivado: None | str = None):
    if xilinx_vivado is None:
        xilinx_vivado = os.environ.get("XILINX_VIVADO")
        if xilinx_vivado is None:
            raise ValueError("XILINX_VIVADO environment variable is not set")

    xilinx_lib_path = f"{xilinx_vivado}/lib/lnx64.o/Rhel/9"
    xilinx_exec_path = f"{xilinx_vivado}/bin"

    ld_library_path = os.environ.get("LD_LIBRARY_PATH")
    exec_path = os.environ.get("PATH")

    ld_library_path = f"{xilinx_lib_path}:{ld_library_path}" if ld_library_path is not None else xilinx_lib_path
    exec_path = f"{xilinx_exec_path}:{exec_path}" if exec_path is not None else xilinx_exec_path

    return {
        **os.environ.copy(),
        "XILINX_VIVADO": xilinx_vivado,
        "LD_LIBRARY_PATH": ld_library_path,
        "PATH": exec_path,
    }


def run_vivado(
        task: Literal["impl", "program"],
        top_level: str,
        fpga_part: str = "xc7z020clg484-1",
        xilinx_path: None | str = None,
        work_dir: None | str = None,
):
    match task:
        case "impl":
            script = impl_script(top_level, fpga_part)
        case "program":
            script = program_script()
        case _:
            raise ValueError(f"Unknown task: {task}")

    with NamedTemporaryFile("w", suffix=".tcl") as tcl_file:
        tcl_file.write(script)
        tcl_file.flush()
        result = subprocess.run(
            f"vivado -mode batch -source {tcl_file.name}",
            shell=True,  # noqa: S602
            env=xilinx_env(xilinx_path),
            cwd=work_dir,
        )
        return result.returncode
