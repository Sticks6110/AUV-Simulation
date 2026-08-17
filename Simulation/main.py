# Author: Brennan Werner
# Date Created: 8/16/26

import argparse

import data
from ocean_sim import OceanSim
from auv_sim import AUVSim

if __name__ == '__main__':
    # Argument Parsing
    parser = argparse.ArgumentParser(description="An AUV Simulation.")

    parser.add_argument("depthdata", type=str, help="The path to the NetCDF depth data.")

    args = parser.parse_args()

    # Simulation
    depth_data = data.load_bathymetry_data(args.depthdata)

    ocean = OceanSim(depth_data)
    auv = AUVSim()