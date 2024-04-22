import os
from pathlib import Path


def impl_script(top_level, fpga_part="xc7z020clg484-1", proj_dir=None):
    proj_dir = Path(os.getcwd()) if proj_dir is None else Path(proj_dir)
    sv_files = list((proj_dir / "src").rglob("*.sv"))
    sv_files = " ".join([str(file.absolute()) for file in sv_files])
    xdc_files = list((proj_dir / "src").rglob("*.xdc"))
    xdc_files = " ".join([str(file.absolute()) for file in xdc_files])
    output_dir = str((proj_dir / "output").absolute())

    read_files = f"""
    set outputDir {output_dir}
    set outputBit $outputDir/output.bit
    set outputDcp $outputDir/final.dcp
    file mkdir $outputDir

    read_verilog -sv {{ {sv_files} }}
    read_xdc {{ {xdc_files} }}
    """

    synth = f"""
    # Synthesis
    synth_design -top {top_level} -part {fpga_part}

    report_timing_summary -file $outputDir/post_synth_timing_summary.rpt
    report_utilization -file $outputDir/post_synth_util.rpt
    """

    impl = """
    # Optimization
    opt_design

    # Implementation
    place_design
    report_clock_utilization -file $outputDir/clock_util.rpt
    route_design
    report_route_status -file $outputDir/post_route_status.rpt
    report_timing_summary -file $outputDir/post_route_timing_summary.rpt
    report_power -file $outputDir/post_route_power.rpt
    report_drc -file $outputDir/post_imp_drc.rpt

    # Final output product
    write_checkpoint -force $outputDcp
    write_bitstream -force $outputBit
    """

    return "\n".join([read_files, synth, impl])


def program_script(proj_dir=None):
    proj_dir = Path(os.getcwd()) if proj_dir is None else Path(proj_dir)
    output_dir = str((proj_dir / "output").absolute())

    return f"""
set outputDir {output_dir}
set outputBit $outputDir/output.bit

# Program the device
open_hw_manager
connect_hw_server
open_hw_target

current_hw_device [get_hw_devices x*]
set_property PROGRAM.FILE $outputBit [current_hw_device]

program_hw_devices

disconnect_hw_server
close_hw_manager
"""
