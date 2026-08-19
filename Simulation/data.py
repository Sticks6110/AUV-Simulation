# Author: Brennan Werner
# Date Created: 8/16/26

import xarray as xr
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame

def load_bathymetry_data(nc_file: str):
    """

    """
    data_set = xr.open_dataset(nc_file)
    data_frame = data_set.to_dataframe()
    data_frame = data_frame.reset_index()
    return data_frame