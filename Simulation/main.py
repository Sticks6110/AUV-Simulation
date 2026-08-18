# Author: Brennan Werner
# Date Created: 8/16/26

import argparse

import data
from ocean_sim import OceanSim
from auv_sim import AUVSim

def get_input(auv: AUVSim):
    left = float(input("Left Throttle 0-1: "))
    cent = float(input("Center Throttle 0-1: "))
    right = float(input("Right Throttle 0-1: "))

    auv.power_left_motor(left)
    auv.power_middle_motor(cent)
    auv.power_right_motor(right)

    for i in range(0, 100):
        auv.step_time(0.01)

    print(str(auv))
    get_input(auv)

if __name__ == '__main__':
    # Argument Parsing
    #parser = argparse.ArgumentParser(description="An AUV Simulation.")

    #parser.add_argument("depthdata", type=str, help="The path to the NetCDF depth data.")

    #args = parser.parse_args()

    # Simulation
    #depth_data = data.load_bathymetry_data(args.depthdata)

    #ocean = OceanSim(depth_data)
    auv = AUVSim(5, 0.15, 0.5)
    get_input(auv)