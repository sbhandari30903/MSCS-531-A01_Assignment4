import re, sys, math

stats = open(sys.argv[1]).read()

def grab(key):
    m = re.search(r"^%s\s+([0-9eE\+\-\.]+)" % re.escape(key), stats, flags=re.M)
    return float(m.group(1)) if m else None

simInsts = grab("simInsts")
ticks = grab("simTicks")
tbp = grab("ticksPerSimPoint") or 1.0  # not always present
freq = grab("system.clk_domain.clock")  # not numeric; ignore
cycles = grab("system.cpu.numCycles") or (ticks / grab("system.cpu_clk_domain.clock"))

# Fallback if numCycles missing:
if not cycles and ticks:
    # X86 default tick is 1 ps; cycles ~ ticks / (period in ticks). Gem5 prints clock like "3GHz".
    clk = None
    m = re.search(r"^system.clk_domain.clock\s+(\d+)\s*([pnum]?s)", stats, flags=re.M)
    if m:
        val, unit = float(m.group(1)), m.group(2)
        scale = dict(ps=1e-12, ns=1e-9, us=1e-6, ms=1e-3, s=1.0)
        period = val * scale.get(unit, 1e-12)  # seconds
        # ticks are in ps => convert seconds to ticks:
        cycles = ticks / (period / 1e-12)
    else:
        cycles = None

if not simInsts or not cycles:
    print("Missing metrics. simInsts=", simInsts, "cycles=", cycles)
    sys.exit(1)

ipc = simInsts / cycles
cpi = cycles / simInsts
print(f"Committed Instructions: {simInsts:,.0f}")
print(f"Cycles: {cycles:,.0f}")
print(f"IPC (Throughput): {ipc:.4f}")
print(f"Avg Instruction Latency (≈ CPI): {cpi:.4f} cycles/inst")

