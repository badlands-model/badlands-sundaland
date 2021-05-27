#!/usr/bin/env python3
# coding: utf-8

# run me with: mpiexec -n $CPUS python3 -m mpi4py.futures mpi_sunda.py

import meshio
import numpy as np
import time

from mpi4py import MPI
from mpi4py.futures import MPIPoolExecutor


from LECMesh import LECMesh

import argparse

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

parser = argparse.ArgumentParser(
    description="LEC computation.",
    add_help=True,
)


parser.add_argument("-i", "--input", help="input file", required=True)

args = None
try:
    if rank == 0:
        # Parsing command line arguments
        args = parser.parse_args()
finally:
    args = comm.bcast(args, root=0)

infile = str(args.input)
confile = infile[:-3]+str('npz')
outfile = str('cost')+infile

print(rank,infile,outfile)


def parprint(*args, **kwargs):
    if rank == 0:
        print(*args, **kwargs)

def init(point):
    global lm
    try:
        lm
    except NameError:
        print("{}: creating lm obj".format(rank), flush=True)
        lm = LECMesh(mesh,
                     max_fuel,
                     neighbours_cache_size = points_above_sealevel.shape[0],
                     neighbour_finding_function = None) #precomputed_neighs)
    # Setup the LECMesh functions via class instantiation.

    return lm.get_dist_from_point(point)


# Load connectivity of the mesh
# n = None
# with np.load(confile) as d:
#     n = d['n']

# def precomputed_neighs(self, point):
#     neighs = n[point]
#     neighs = neighs[neighs > 0] # a negative value is just a NaN in this context
#     elevations = self.mesh.point_data['Z'][neighs]
#     # Return a list of connected points, as long as they are above sea-level
#     return neighs[elevations >= 0]

mesh = meshio.read(infile)
points_above_sealevel = np.nonzero(mesh.point_data['Z'] >= 0)[0]
parprint("Total starting points available: ", points_above_sealevel.shape[0], flush=True)

# Setup the output file:
mesh.point_data['cost'] = np.zeros_like(mesh.point_data['Z'])

max_fuel = 300 # A smaller value means visiting far fewer nodes, so it speeds things up a lot


if __name__ == "__main__":

    all_costs = []
    with MPIPoolExecutor() as ex:
        for res in ex.map(init, points_above_sealevel, chunksize=10):
            all_costs.append(res)
            parprint('Progress: {: 4.3f} %'.format((len(all_costs)/points_above_sealevel.shape[0]) * 100), flush=True)

    # The first CPU can now write out all the data
    if rank == 0:
        for i in all_costs:
            mesh.point_data['cost'][i[0]] = i[1]
        meshio.write(outfile, mesh)
