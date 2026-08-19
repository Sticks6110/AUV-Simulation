# Author: Brennan Werner
# Date Created: 8/16/26

import numpy as np

import data
from ocean_sim import OceanSim
from auv_sim import AUVSim
from auv_drive import AUVDrive

def get_input(auv: AUVSim):
    left = float(input("Left Throttle 0-1: "))
    cent = float(input("Center Throttle 0-1: "))
    right = float(input("Right Throttle 0-1: "))
    ballast = float(input("Ballast Liters: "))

    auv.power_left_motor(left)
    auv.power_middle_motor(cent)
    auv.power_right_motor(right)
    auv.set_ballast(ballast)

    for i in range(0, 100):
        auv.step_time(0.01)

    print(str(auv))
    get_input(auv)

if __name__ == '__main__':
    # Simulation
    depth_data = data.load_bathymetry_data("Data/gebco_2026_n35.0_s30.0_w-75.0_e-70.0.nc")

    ocean = OceanSim(depth_data)
    auv = AUVSim(ocean, 8, 0.25, 10, 1000, 20, 390, 3600, 0.01)
    drive = AUVDrive(auv, np.array([[0, 50, -25], [100, 0, -25], [250, 250, -20], [250, 200, 0]]))

    drive.run()