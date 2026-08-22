# Author: Brennan Werner
# Date Created: 8/16/26

import numpy as np
import sys
import subprocess
from pathlib import Path

import data
from auv_sim import AUVSim
from auv_drive import AUVDrive
from Gui.gui import GUI
from Gui.popup import Popup

def lat_lon_to_local(lat: float, lon: float, origin_lat: float, origin_lon: float):
    """
    Converts latitude and longitude cordinates
    to local offset x, y cordinates in meters.
    """
    R = 6371000.0  # Earth radius in meters

    d_lat = np.radians(lat - origin_lat)
    d_lon = np.radians(lon - origin_lon)

    x = R * d_lon * np.cos(np.radians(origin_lat))
    y = R * d_lat

    return x, y

def parse_arguments(arguments: list[str], index: int = 0, o: dict = None):
    """
    Recursively parses the arguments and
    returns a dictionary of them.
    """

    if(o is None):
        # Default Values
        o = {
            "checkpoints": [],
            "lat": 32.5,
            "lon": -72.5,
            "mass": 8.0,
            "ballast": 10.0,
            "battery": 1000.0,
            "battery-drain": 20.0,
            "motor-watts": 400.0,
            "motor-rpm": 3600.0,
            "motor-thrust": 0.1,
        }

    if(index + 1 >= len(arguments)):
        return o

    # Change the default values with the arguments passed
    if(arguments[index] == "-checkpoint"):
        lat, lon, depth = arguments[index + 1].split(',')
        o["checkpoints"].append([float(lat), float(lon), float(depth)])
        return parse_arguments(arguments, index + 2, o=o)
    else:
        o[arguments[index][1:]] = float(arguments[index + 1])
        return parse_arguments(arguments, index + 2, o=o)

def format_checkpoints(lat: float, lon: float, checkpoints: list):
    """
    Converts the coordinates to local offsets from
    the starting point in meters.
    """
    new_checkpoints = []

    for checkpoint in checkpoints:
        x, y = lat_lon_to_local(checkpoint[0], checkpoint[1], lat, lon)
        new_checkpoints.append([x, y, checkpoint[2]])

    return new_checkpoints

def run_sim(data: tuple):
    """
    """
    print(data)
    python_exe = Path(__file__).parent.parent / ".venv" / "Scripts" / "python.exe"
    simulation_main = Path(__file__).parent / "main.py"

    command = [
        str(python_exe),
        str(simulation_main),
        "-lat", str(data[0]),
        "-lon", str(data[1]),
        "-mass", str(data[2]),
        "-ballast", str(data[3]),
        "-battery", str(data[4]),
        "-battery-drain", str(data[5]),
        "-motor-watts", str(data[6]),
        "-motor-rpm", str(data[7]),
        "-motor-thrust", str(data[8]),
    ]

    for i, checkpoint in enumerate(data[9]):
        command.append("-checkpoint")
        command.append(f'{checkpoint[0]},{checkpoint[1]},{checkpoint[2]}')

    process = subprocess.Popen(command, shell=True)

if __name__ == '__main__':
    # Argument Parsing
    arguments = sys.argv[1:]
    if(len(arguments) > 0):
        # Get Args
        args = parse_arguments(arguments)
        checkpoints = format_checkpoints(args['lat'], args['lon'], args['checkpoints'])

        print(checkpoints)

        # Run simulation
        #auv = AUVSim(8, 0.25, 10, 1000, 20, 390, 3600, 0.01)
        auv = AUVSim(args["mass"], 0.25, args["ballast"], args["battery"], args["battery-drain"], args["motor-watts"], args["motor-rpm"], args["motor-thrust"])
        gui = GUI()
        drive = AUVDrive(auv, np.array(checkpoints), gui)

        drive.run()
    else:
        # Data Entry Popup
        popup = Popup(run_sim)