# Author: Brennan Werner
# Date Created: 8/16/26

from pandas import DataFrame
import numpy as np

class OceanSim:

    def __init__(self, depth_data: DataFrame):
        """
        
        """
        self._depth = depth_data

        self._min_lat = depth_data["lat"].min()
        self._max_lat = depth_data["lat"].max()
        self._min_lon = depth_data["lon"].min()
        self._max_lon = depth_data["lon"].max()

    def get_depth(self, lat: float, lon: float) -> float:
        """
        Gets the depth in meters of the ocean at the provided latitude and longitude.
        """
        if(not self.in_bounds(lat, lon)):
            print("Requested depth from an out of range coordinate.")

        mask_lat = np.isclose(self._depth["lat"], 37.9818, atol=1e-3)
        mask_lon = np.isclose(self._depth["lon"], -75.9309, atol=1e-3)

        return self._depth[mask_lat & mask_lon]

    def in_bounds(self, lat: float, lon: float) -> bool:
        """
        Returns true if the latitude and longitude are inside the bounding area. Otherwise it returs false.
        """
        if(lat < self._min_lat or lat > self._max_lat or lon < self._min_lon or lon > self._max_lon):
            return False
        return True