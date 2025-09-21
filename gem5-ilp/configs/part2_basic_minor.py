# configs/part2_basic_minor.py
import os, argparse, importlib.util
try:
    from m5.objects import X86MinorCPU as MinorCPUClass
except Exception:
    from m5.objects import MinorCPU as MinorCPUClass
from m5.objects import Process, Root

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "common_simple_sys", os.path.join(HERE, "common_simple_sys.py")
)
common = importlib.util.module_from_spec(spec)
spec.loader.exec_module(common)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--binary", required=True)
    ap.add_argument("--clk", default="3GHz")
    ap.add_argument("--mem", default="512MB")
    ap.add_argument("--trace", action="store_true")
    args = ap.parse_args()

    # absolute path is safest for SEWorkload
    bin_path = os.path.abspath(args.binary)

    cpu = MinorCPUClass()

    # pass the binary path so SEWorkload.init_compatible() is happy
    system = common.make_simple_system(cpu, mem_size=args.mem, clk=args.clk,
                                       workload_path=bin_path)

    p = Process()
    p.cmd = [bin_path]
    system.cpu.workload = p
    system.cpu.createThreads()

    return Root(full_system=False, system=system)

root = main()
# enable pipeline trace with --debug-flags=MinorTrace

