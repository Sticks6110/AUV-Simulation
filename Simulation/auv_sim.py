# Author: Brennan Werner
# Date Created: 8/16/26

from pandas import DataFrame
import numpy as np
import math

class Motor:
    """
    """

    def __init__(self, max_power: float, max_rpm: float, thrust_cof: float, prop_diameter: float, water_density: float = 1025):
        """
        max_power: Maximum motor power in watts.
        max_rpm: Maximum propeller speed in RPM.
        thrust_coefficient: Dimensionless propeller thrust coefficient (CT).
        prop_diameter: Propeller diameter in meters.
        water_density: Water density in kg/m^3.
        """
        self._max_power = max_power
        self._max_rpm = max_rpm
        self._ct = thrust_cof
        self._diameter = prop_diameter
        self._water_density = water_density

        self._throttle = 0.0

    def set_water_density(self, density: float):
        """
        Sets the water density, this
        variable can change depending on depth, possibly even
        salinity and temperature in the future.
        """
        self._water_density = density

    def set_throttle(self, throttle: float):
        """
        Sets the throttle of the motor. Should be a value
        between 0 and 1.
        """
        self._throttle = np.clip(throttle, 0.0, 1.0)

    def get_power(self) -> float:
        """
        Returns the current motor power consumption in watts.
        """
        return self._max_power * self._throttle
    
    def get_thrust(self):
        """
        Calculates the thrust of the motor
        and propeller and returns it in newtons.
        """
        rpm = self._throttle * self._max_rpm
        rps = rpm / 60.0

        return self._ct * self._water_density * (rps ** 2) * (self._diameter ** 4)

class AUVSim:
    """
    """

    def __init__(self, mass: float, drag_cof: float, ballast: float):
        """
        Latitude: Starting latitude
        Longitude: Starting longitude
        Mass: Kilograms
        Drag COF: Dimensionless Quantity
        Motor Force: Newtons
        Ballast: 0-1 range for how full the ballast tank is. 0.5 = neutrally boyant, 0 = fully boyant (floating)
        """

        self._mass = mass
        self._drag_cof = drag_cof

        self._left_motor = Motor(500, 3000, 0.1, 0.1)
        self._center_motor = Motor(750, 5000, 0.1, 0.1)
        self._right_motor = Motor(500, 3000, 0.1, 0.1)

        self._left_motor_pos = np.array([
            -0.1225,    #east
            0.5,        #north
            0.0         #depth
        ])

        self._center_motor_pos = np.array([
            0.0,
            0.5,
            0.0
        ])

        self._right_motor_pos = np.array([
            0.1225,
            0.5,
            0.0
        ])

        self._thrust_direction = np.array([
            0.0,    #east
            1.0,    #north
            0.0     #depth
        ])

        self._position = np.zeros(3) #x = east, y = north, z = depth
        self._velocity = np.zeros(3)

        self._orientation = np.zeros(3)
        self._angular_velocity = np.zeros(3)

        self._time = 0
        self._delta_time = 0

    def step_time(self, delta_time: float):
        """
        Steps forward in time and runs the simulation.
        """
        self._delta_time = delta_time
        self._time += delta_time

        total_torque = np.zeros(3)
        total_force = np.zeros(3)

        motors = [
            (self._left_motor, self._left_motor_pos),
            (self._center_motor, self._center_motor_pos),
            (self._right_motor, self._right_motor_pos)
        ]

        world_direction = self.rotate_vector(self._thrust_direction)

        for motor, position in motors:
            thrust = motor.get_thrust()
            force = thrust * world_direction

            world_position = self.rotate_vector(position)

            total_force += force
            total_torque += np.cross(world_position, force)

        # Angular acceleration
        angular_acceleration = (
            total_torque / self.get_inertia()
        )

        # Angular velocity
        self._angular_velocity += (
            angular_acceleration * delta_time
        )

        # Orientation
        self._orientation += (
            self._angular_velocity * delta_time
        )

        # Gravity
        gravity_force = self.get_mass() * -9.81 * np.array([0, 0, 1.0])
        total_force += gravity_force

        # Buoyancy
        if (self._position[2] <= 0):
            buoyancy_force = 1025 * 0.015 * 9.81 * np.array([0, 0, 1.0])
            total_force += buoyancy_force

        # Drag
        drag_force = 0.5 * 1025 * (self._velocity ** 2) * self._drag_cof * 0.015
        total_force += drag_force

        # Acceleration
        acceleration = total_force / self.get_mass()

        # Velocity
        self._velocity += acceleration * delta_time

        # Position
        self._position += self._velocity * delta_time

    def power_middle_motor(self, ammount: float):
        """
        Powers the middle motor for forward movement.
        ammount: 0-1 range
        """
        self._center_motor.set_throttle(ammount)

    def power_left_motor(self, ammount: float):
            """
            Powers the left motor for rightward movement.
            ammount: 0-1 range
            """
            self._left_motor.set_throttle(ammount)

    def power_right_motor(self, ammount: float):
            """
            Powers the right motor for leftward movement.
            ammount: 0-1 range
            """
            self._right_motor.set_throttle(ammount)

    def get_inertia(self) -> np.array:
            """
            Gets the moment of inertia for a rectanglular prism.
            """

            mass = self._mass

            ix = 0.01625 * mass
            iy = 0.505 * mass
            iz = 0.51125 * mass

            return np.array([ix, iy, iz])

    def get_mass(self) -> float:
         """
         Calculates the mass for the AUV.
         """
         return self._mass

    def get_rotation_matrix(self) -> np.ndarray:
        roll, pitch, yaw = self._orientation

        cr = np.cos(roll)
        sr = np.sin(roll)

        cp = np.cos(pitch)
        sp = np.sin(pitch)

        cy = np.cos(yaw)
        sy = np.sin(yaw)

        rx = np.array([
            [1, 0, 0],
            [0, cr, -sr],
            [0, sr, cr]
        ])

        ry = np.array([
            [cp, 0, sp],
            [0, 1, 0],
            [-sp, 0, cp]
        ])

        rz = np.array([
            [cy, -sy, 0],
            [sy, cy, 0],
            [0, 0, 1]
        ])

        return rz @ ry @ rx

    def rotate_vector(self, vector: np.ndarray) -> np.ndarray:
        """
        Rotates a local vector into world coordinates
        based on the AUV's orientation.
        """
        rotation_matrix = self.get_rotation_matrix()
        return rotation_matrix @ vector

    def __str__(self) -> str:
        return "(X, Y, Z) : " + str(self._position)  + " | (roll, pitch, yaw) : " + str(self._orientation) + " | Velocity : " + str(self._velocity)