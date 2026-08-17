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

    def __init__(self, lat: float, lon: float, mass: float, drag_cof: float, ballast: float):
        """
        Latitude: Starting latitude
        Longitude: Starting longitude
        Mass: Kilograms
        Drag COF: Dimensionless Quantity
        Motor Force: Newtons
        Ballast: 0-1 range for how full the ballast tank is. 0.5 = neutrally boyant, 0 = fully boyant (floating)
        """
        self._lat_origin = lat
        self._lon_origin = lon
        self._lat = lat
        self._lon = lon

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

        self.thrust_direction = np.array([
            0.0,    #east
            1.0,    #north
            0.0     #depth
        ])

        self._x = 0 #east
        self._y = 0 #north
        self._z = 0 #depth

        self._heading = 0.0
        self._angular_velocity = 0.0

        self._time = 0
        self._delta_time = 0

    def step_time(self, delta_time: float):
        """
        Steps forward in time and runs the simulation.
        """
        self._delta_time = delta_time
        self._time += delta_time
        self.simulate(delta_time)

    def simulate_motor(self, motor: Motor, motor_position: np.array, motor_direction: np.array):
        """
        Runs the simulation.
        """
        thrust = motor.get_thrust()
        force = thrust * motor_direction
        torque = np.cross(motor_position, force)

    def update_lat_lon(self):
        """
        Updates the latitude and longitude of the AUV
        using the x and y position. 
        """
        lat_rad = math.radians(self._lat_origin)

        dlat = self._y / 6371000
        dlon = self._x / (6371000 * math.cos(lat_rad))

        self._lat = self._lat_origin + math.degrees(dlat)
        self._lon = self._lon_origin + math.degrees(dlon)

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

    