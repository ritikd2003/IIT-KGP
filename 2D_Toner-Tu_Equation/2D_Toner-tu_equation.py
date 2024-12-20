"""
this is a Dedalus script for simulating a 2D toner-tu equation with a given specific 
relation and values of small level forcing.

It can be ran serially or in parallel, and uses the built-in analysis framework 
to save data snapshots to HDF5 files. The 'plot_snapshots.py` script can be used 
to produce plots from the saved data.
The simulation should take about 10 cpu-minutes to run.


To run and plot using e.g. 6 processes:
    $ mpiexec -n 6 python3 shear_flow.py
    $ mpiexec -n 6 python3 plot_snapshots.py snapshots/*.h5
"""


import numpy as np
import dedalus.public as d3
import logging
logger = logging.getLogger(__name__)

# Parameters
Lx, Lz = 2 * np.pi, 2 * np.pi
Nx, Nz = 256, 256
dealias = 3/2
stop_sim_time = 100
timestepper = d3.RK222
max_timestep = 0.01
dtype = np.float64

# Bases
coords = d3.CartesianCoordinates('x', 'z')
dist = d3.Distributor(coords, dtype=dtype)
xbasis = d3.RealFourier(coords['x'], size=Nx, bounds=(0, Lx), dealias=dealias)
zbasis = d3.RealFourier(coords['z'], size=Nz, bounds=(0, Lz), dealias=dealias)

# Fields
s = dist.Field(name='s', bases=(xbasis,zbasis))
psi = dist.Field(name='psi', bases=(xbasis,zbasis))
w = dist.Field( name='w', bases=(xbasis,zbasis))
tau = dist.Field(name='tau')

# Substitutions
T_0 = 0.001
T_2 = T_0 * 0.0025
T_4 = T_0 * 9.7e-7
x, z = dist.local_grids(xbasis, zbasis)
ex, ez = coords.unit_vector_fields(dist)

# Problem
problem = d3.IVP([w, psi, tau, s], namespace=locals())
problem.add_equation("dt(w) - T_0 * lap(w) + T_2 * lap(lap(w)) - T_4 * lap(lap(lap(w))) = - skew(grad(psi)) @ grad(w)")
problem.add_equation("dt(s) - nu * lap(s) = - skew(grad(psi)) @ grad(s)")
problem.add_equation("lap(psi) + tau - w = 0")
problem.add_equation("integ(psi) = 0")

# Solver
solver = problem.build_solver(timestepper)
solver.stop_sim_time = stop_sim_time

# Initial conditions
w['g'] = np.random.uniform(-1, 1, w['g'].shape) * 5  # Uniform random initial condition for w
s['g'] = np.random.uniform(-1, 1, s['g'].shape) * 5   # Uniform random initial condition for s

# Analysis
snapshots = solver.evaluator.add_file_handler('snapshots', sim_dt=0.1, max_writes=100)
snapshots.add_task(w, name='vorticity')

# CFL
CFL = d3.CFL(solver, initial_dt=max_timestep, cadence=10, safety=0.2, threshold=0.1,
             max_change=1.5, min_change=0.5, max_dt=max_timestep)
CFL.add_velocity(d3.skew(d3.grad(psi)))

# Flow properties
flow = d3.GlobalFlowProperty(solver, cadence=10)
flow.add_property((w)**2, name='w2')

# Main loop
try:
    logger.info('Starting main loop')
    while solver.proceed:
        timestep = max_timestep  # CFL.compute_timestep()
        solver.step(timestep)
        if (solver.iteration-1) % 10 == 0:
            max_w = np.sqrt(flow.max('w2'))
            logger.info('Iteration=%i, Time=%e, dt=%e, max(w)=%f' % (solver.iteration, solver.sim_time, timestep, max_w))
except:
    logger.error('Exception raised, triggering end of main loop.')
    raise
finally:
    solver.log_stats()
