# Author: Brennan Werner
# Date Created: 8/17/26

import dearpygui.dearpygui as dpg
import numpy as np
import time
from collections import deque
from pandas import DataFrame

import data
from Gui.oscilloscope import Oscilloscope
from Gui.data_view import DataView

class GUI:
    """
    
    """

    def __init__(self):
        self._destroyed = False

        dpg.create_context()
        dpg.configure_app(docking=True, docking_space=True, load_init_file="layout.ini")
        
        dpg.create_viewport(title='AUV Simulator', width=800, height=600)

        #Menu Bar
        with dpg.viewport_menu_bar():
            with dpg.menu(label="Settings"):
                dpg.add_menu_item(label="Save Layout", callback=lambda: dpg.save_init_file("layout.ini"))

        self._data_view = DataView()

        self._oscilloscope = Oscilloscope()
        self._oscilloscope.add_variable("Latitude")
        self._oscilloscope.add_variable("Longitude")
        self._oscilloscope.add_variable("Depth")
        self._oscilloscope.add_variable("Velocity X")
        self._oscilloscope.add_variable("Velocity Y")
        self._oscilloscope.add_variable("Velocity Z")
        self._oscilloscope.add_variable("Velocity")
        self._oscilloscope.add_variable("Roll")
        self._oscilloscope.add_variable("Pitch")
        self._oscilloscope.add_variable("Yaw")
        self._oscilloscope.add_variable("Yaw Velocity")
        self._oscilloscope.add_variable("Pitch Velocity")
        self._oscilloscope.add_variable("Roll Velocity")
        self._oscilloscope.add_variable("Checkpoint Latitude")
        self._oscilloscope.add_variable("Checkpoint Longitude")
        self._oscilloscope.add_variable("Checkpoint Depth")
        self._oscilloscope.add_variable("Checkpoint Distance")
        self._oscilloscope.add_variable("Mass")
        self._oscilloscope.add_variable("Ballast")
        self._oscilloscope.add_variable("Battery")
        self._oscilloscope.add_variable("Left Throttle")
        self._oscilloscope.add_variable("Center Throttle")
        self._oscilloscope.add_variable("Right Throttle")

        # Setup
        dpg.setup_dearpygui()
        dpg.show_viewport()

    def __del__(self):
        if(not self._destroyed):
            dpg.destroy_context()
            self._destroyed = True

    def step(self):
        """
        Updates the GUI. Returns True if still running and False if not.
        """
        if(dpg.is_dearpygui_running()):
            dpg.render_dearpygui_frame()
            return True

        if(not self._destroyed):
            dpg.destroy_context()
            self._destroyed = True
        return False

    def update(self, values, checkpoints):
        """
        
        """
        self._oscilloscope.update(values)
        self._data_view.update(values)
        self._data_view.set_checkpoints(checkpoints)