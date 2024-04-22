from tempfile import TemporaryDirectory

from magia import Elaborator

from script import cleanup, run_vivado
from src.top import Top

top_level = "Top"
xilinx_path = "/home/khwong/Xilinx/Vivado/2023.2"

if __name__ == "__main__":

    cleanup()

    # Create and Elaborate the top module
    Elaborator.to_file("src/generated/top.sv", Top(name=top_level))

    # Implement design and program the FPGA

    with TemporaryDirectory() as temp_dir:
        impl_ret = run_vivado("impl", top_level, xilinx_path=xilinx_path, work_dir=temp_dir)
        if impl_ret != 0:
            raise RuntimeError("Implementation failed")
        run_vivado("program", top_level, xilinx_path=xilinx_path, work_dir=temp_dir)
