# Author: Brennan Werner
# Date Created: 8/18/26

import auv_sim
import numpy as np
import math
import time
from Gui.gui import GUI

class AUVDrive:
    """
    Acts as the computer of the AUV. Controlls the AUV
    to complete its mission.
    """

    def __init__(self, sim: auv_sim.AUVSim, checkpoints: np.ndarray, gui: GUI = None):
        """
        sim: AUV Simulation
        checkpoints:
        """
        self._sim = sim
        self._gui = gui

        self._checkpoints = []
        self._progress = 0
        self._distance = 0
        self._left_throttle = 0
        self._cent_throttle = 0
        self._right_throttle = 0

        for checkpoint in checkpoints:
            self._checkpoints.append((checkpoint, self.local_to_latlon(checkpoint[0], checkpoint[1], 32.5, -72.5)))

    def run(self):
        """
        Automatically runs the simulation.
        """
        done = False

        while(not done):
            self.manual_step()
            self.update_gui()
            if(not self._gui.step()):
                done = True

    def manual_step(self) -> bool:
        """
        Manually steps the drive simulation. Returns
        true if done (completed or error), false if not.
        """
        if(self._progress >= len(self._checkpoints)):
            return True
        
        # Checks
        position = self._sim.get_position()

        distance = np.linalg.norm(self._checkpoints[self._progress][0] - position)
        self._distance = distance

        distance_dir = np.linalg.norm(self._checkpoints[self._progress][0][:2] - position[:2])

        distance_depth = np.abs(self._checkpoints[self._progress][0][-1] - position[-1])

        if(distance <= 3):
            print("Finished Checkpoint")
            self._progress += 1
            if(self._progress >= len(self._checkpoints)):
                print("DONE!")
                return True

        # Turning PID
        orientation = self._sim.get_orientation()
        ang_vel = self._sim.get_ang_velocity()
        desired_heading = self.get_desired_heading(position, self._checkpoints[self._progress][0])

        # Normalize the value between negative and positive pi
        heading_error = desired_heading - orientation[2]
        heading_error = (heading_error + math.pi) % (2 * math.pi) - math.pi

        Kp_o = 0.8
        Kd_o = 0.7

        if(abs(heading_error) < np.radians(1)):
            turn = 0.0
        else:
            turn = Kp_o * heading_error - Kd_o * ang_vel[2]
            turn = np.clip(turn, -1.0, 1.0)

        self._sim.power_left_motor(-turn)
        self._sim.power_right_motor(turn)

        self._left_throttle = -turn
        self._right_throttle = turn

        # Forward Movement
        forward = np.cos(heading_error)
        forward = max(0.0, forward)

        if(distance_dir < 20):
            forward *= distance_dir / 20

        self._sim.power_middle_motor(forward)
        self._cent_throttle = forward

        # Ballast
        max_ballast = self._sim.get_max_ballast()

        target_depth = self._checkpoints[self._progress][0][2]
        depth_error = target_depth - position[2]

        # Offset from neutrall boyancy
        neutral_mass = 1025 * 0.015
        neutral_ballast = neutral_mass - self._sim.get_mass_no_ballast()
        neutral_ballast = np.clip(neutral_ballast, 0, max_ballast)

        Kp_b = 0.05
        ballast_offset = -Kp_b * depth_error

        if(depth_error > 0.2 or depth_error < -0.2):
            ballast = neutral_ballast + ballast_offset
        else:
            ballast = neutral_ballast

        ballast = np.clip(ballast, 0.0, max_ballast)

        self._sim.set_ballast(ballast)

        # Step the physics simulation
        self._sim.step_time(0.02)

        return False

    def local_to_latlon(self, x, y, origin_lat, origin_lon):
        """
        Converts a local coordinate to latitude and longitude.
        """
        meters_per_degree_lat = 111320

        meters_per_degree_lon = (
            meters_per_degree_lat * math.cos(math.radians(origin_lat))
        )

        latitude = origin_lat + y / meters_per_degree_lat
        longitude = origin_lon + x / meters_per_degree_lon

        return latitude, longitude

    def get_desired_heading(self, position, checkpoint):
        """
        Gets the direction of the checkpoint relative to
        the AUV's position and normalizes it between negative
        and positive pi.
        """
        dx = checkpoint[0] - position[0]
        dy = checkpoint[1] - position[1]

        heading = -np.arctan2(dx, dy)

        return (heading + np.pi) % (2 * np.pi) - np.pi

    def update_gui(self):
        """
        """
        pos = self._sim.get_position()
        lat, lon = self.local_to_latlon(pos[0], pos[1], 32.5, -72.5)
        vel = self._sim.get_velocity()
        speed = self._sim.get_speed()
        orientation = self._sim.get_orientation()
        ang_vel = self._sim.get_ang_velocity()
        ballast = self._sim.get_ballast()
        max_ballast =self._sim.get_max_ballast()
        battery = self._sim.get_battery_percent()
        mass = self._sim.get_mass()

        checkpoints = []
        for i, checkpoint in enumerate(self._checkpoints):
            checkpoints.append((
                checkpoint[1][0],
                checkpoint[1][1],
                checkpoint[0][2],
                (i < self._progress)
            ))

        update_dictionary = {
            "Latitude": (lat, f"{lat:.6f} °"),
            "Longitude": (lon, f"{lon:.6f} °"),
            "Depth": (pos[2], f"{pos[2]:.3f} m"),
            "Velocity X": (vel[0], f"{vel[0]:.3f} (m/s)"),
            "Velocity Y": (vel[1], f"{vel[1]:.3f} (m/s)"),
            "Velocity Z": (vel[2], f"{vel[2]:.3f} (m/s)"),
            "Velocity": (speed, f"{speed:.3f} (m/s)"),
            "Roll": (orientation[0], f"{orientation[0]:.3f} °"),
            "Pitch": (orientation[1], f"{orientation[1]:.3f} °"),
            "Yaw": (orientation[2], f"{orientation[2]:.3f} °"),
            "Roll Velocity": (ang_vel[0], f"{ang_vel[0]:.3f} (°/s)"),
            "Pitch Velocity": (ang_vel[1], f"{ang_vel[1]:.3f} (°/s)"),
            "Yaw Velocity": (ang_vel[2], f"{ang_vel[2]:.3f} (°/s)"),
            "Checkpoint Distance": (self._distance, f"{self._distance:.3f} m"),
            "Mass": (mass, f"{mass:.3f} Kg"),
            "Ballast": (ballast, f"{ballast:.3f} L / {max_ballast:.3f} L"),
            "Battery": (battery, f"{battery:.3f} %"),
            "Left Throttle": (self._left_throttle, f"{self._left_throttle:.3f}"),
            "Center Throttle": (self._cent_throttle, f"{self._cent_throttle:.3f}"),
            "Right Throttle": (self._right_throttle, f"{self._right_throttle}"),
        }

        if self._progress < len(self._checkpoints):
            checkpoint = self._checkpoints[self._progress]
            update_dictionary["Checkpoint Latitude"] = (self._checkpoints[self._progress][1][0], f"{self._checkpoints[self._progress][1][0]:.6f} °")
            update_dictionary["Checkpoint Longitude"] = (self._checkpoints[self._progress][1][0], f"{self._checkpoints[self._progress][1][1]:.6f} °")
            update_dictionary["Checkpoint Depth"] = (self._checkpoints[self._progress][1][0], f"{self._checkpoints[self._progress][0][2]:.6f} °")

        self._gui.update(update_dictionary, checkpoints)