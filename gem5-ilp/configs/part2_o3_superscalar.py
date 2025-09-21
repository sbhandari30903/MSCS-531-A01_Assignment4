from m5.objects import *
from common_simple_sys import make_simple_system
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--binary", required=True)
parser.add_argument("--width", type=int, default=2, help="issue/decode/commit width")
parser.add_argument("--rob", type=int, default=192)
parser.add_argument("--lsq", type=int, default=64)
parser.add_argument("--iq", type=int, default=64)
parser.add_argument("--clk", default="3GHz")
parser.add_argument("--mem", default="512MB")
args = parser.parse_args()

cpu = DerivO3CPU()
# Superscalar knobs
cpu.fetchWidth  = args.width
cpu.decodeWidth = args.width
cpu.renameWidth = args.width
cpu.issueWidth  = args.width
cpu.executeWidth= args.width
cpu.commitWidth = args.width

cpu.numROBEntries = args.rob
cpu.LQEntries = args.lsq // 2
cpu.SQEntries = args.lsq // 2
cpu.numIQEntries = args.iq

# Branch predictor (keep reasonable)
cpu.branchPred = TournamentBP()

system = make_simple_system(cpu, mem_size=args.mem, clk=args.clk)

process = Process()
process.cmd = [args.binary]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system=False, system=system)

