import angr
import claripy

proj = angr.Project('./construct', auto_load_libs=False)

arg = claripy.BVS('arg', 8*31)
state = proj.factory.entry_state(args=['./construct', arg])
simgr = proj.factory.simulation_manager(state)
simgr.explore(find=lambda s: b"The flag is" in s.posix.dumps(1))

if len(simgr.found) > 0:
    state = simgr.found[0]
    print(state.solver.eval(arg, cast_to=bytes))
    print(state.posix.dumps(1))
else:
    print(":(")
