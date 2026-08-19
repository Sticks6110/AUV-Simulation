# Author: Brennan Werner
# Date Created: 8/18/26

import auv_sim
import numpy as np
import math

class AUVDrive:
    """
    Acts as the computer of the AUV. Controlls the AUV
    to complete its mission.
    """

    def __init__(self, sim: auv_sim.AUVSim, checkpoints: np.ndarray):
        """
        sim: AUV Simulation
        checkpoints:
        """
        self._sim = sim
        self._checkpoints = checkpoints
        self._progress = 0

    def run(self):
        """
        """
        done = False

        print_count = 0

        while(not done):
            # Checks
            position = self._sim.get_position()

            distance = np.linalg.norm(self._checkpoints[self._progress] - position)

            distance_dir = np.linalg.norm(self._checkpoints[self._progress][:2] - position[:2])

            distance_depth = np.abs(self._checkpoints[self._progress][-1] - position[-1])

            if(distance <= 3):
                print("Finished Checkpoint")
                self._progress += 1
                if(self._progress >= len(self._checkpoints)):
                    print("DONE!")
                    done = True
                    break

            # Turning PID
            orientation = self._sim.get_orientation()
            ang_vel = self._sim.get_ang_velocity()
            desired_heading = self.get_desired_heading(position, self._checkpoints[self._progress])

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

            # Forward Movement
            forward = np.cos(heading_error)
            forward = max(0.0, forward)

            if(distance_dir < 20):
                forward *= distance_dir / 20

            self._sim.power_middle_motor(forward)

            # Ballast
            max_ballast = self._sim.get_max_ballast()

            target_depth = self._checkpoints[self._progress][2]
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
            self._sim.step_time(0.01)

            # Data callouts for debugging
            print_count += 1
            if(print_count >= 100):
                """print(
                    "Ballast:", self._sim.get_ballast(), "\n",
                    "Desired Ballast:", ballast, "\n",
                    "Orientation:", orientation, "\n",
                    "Desired Heading:", desired_heading, "\n",
                    "Heading Error:", heading_error, "\n",
                    "Position:", position, "\n",
                    "Velocity:", self._sim.get_velocity(), "\n",
                    "Checkpoint:", self._checkpoints[self._progress], "\n",
                    "Yaw:", np.degrees(orientation[2]), "\n",
                    "Desired:", np.degrees(desired_heading), "\n",
                    "Error:", np.degrees(heading_error), "\n",
                )"""
                print("Position: ", position, "Orientation: ", orientation, "Distance: ", distance)
                print_count = 0

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