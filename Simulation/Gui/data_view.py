# Author: Brennan Werner
# Date Created: 8/20/26

import dearpygui.dearpygui as dpg
import numpy as np
import time
from collections import deque
from pandas import DataFrame

import data

class DataView:
    def __init__(self):
        self._tracking = {}

        #Section Header Theme
        with dpg.theme() as self._section_header_theme:
            with dpg.theme_component(dpg.mvText):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (50, 100, 255))

        with dpg.window(label="Data"):
            self.section_header("POSITION")
            with dpg.table(header_row=False, borders_innerH=True, borders_outerH=False, borders_innerV=False, borders_outerV=False):
                dpg.add_table_column()
                dpg.add_table_column()
                self.row("Latitude", "Latitude", "0.000000 °")
                self.row("Longitude", "Longitude", "0.000000 °")
                self.row("Depth", "Depth", "0.00 m")

            self.section_header("VELOCITY (m/s)")
            with dpg.table(header_row=False, borders_innerH=True, borders_outerH=False, borders_innerV=False, borders_outerV=False):
                dpg.add_table_column()
                dpg.add_table_column()
                self.row("X", "Velocity X", "0.000 (m/s)")
                self.row("Y", "Velocity Y", "0.000 (m/s)")
                self.row("Z", "Velocity Z", "0.000 (m/s)")
                self.row("Speed", "Velocity", "0.000 (m/s)")

            self.section_header("ORIENTATION")
            with dpg.table(header_row=False, borders_innerH=True, borders_outerH=False, borders_innerV=False, borders_outerV=False):
                dpg.add_table_column()
                dpg.add_table_column()
                self.row("Yaw", "Yaw", "0.000 °")
                self.row("Pitch", "Pitch", "0.000 °")
                self.row("Roll", "Roll", "0.000 °")

            self.section_header("ANGULAR VELOCITY (°/s)")
            with dpg.table(header_row=False, borders_innerH=True, borders_outerH=False, borders_innerV=False, borders_outerV=False):
                dpg.add_table_column()
                dpg.add_table_column()
                self.row("Yaw", "Yaw Velocity", "0.000 (°/s)")
                self.row("Pitch", "Pitch Velocity", "0.000 (°/s)")
                self.row("Roll", "Roll Velocity", "0.000 (°/s)")

            self.section_header("CURRENT CHECKPOINT")

            with dpg.table(header_row=False, borders_innerH=True, borders_outerH=False, borders_innerV=False, borders_outerV=False):
                dpg.add_table_column()
                dpg.add_table_column()
                self.row("Latitude", "Checkpoint Latitude", "0.000000 °")
                self.row("Longitude", "Checkpoint Longitude", "0.000000 °")
                self.row("Depth", "Checkpoint Depth", "0.00 m")
                self.row("Distance", "Checkpoint Distance", "0.00 m")

            self.section_header("CHECKPOINTS")

            with dpg.child_window(height=150, border=True):
                with dpg.table(header_row=True, tag="checkpoint_table"):
                    dpg.add_table_column(label="Checkpoint")
                    dpg.add_table_column(label="Latitude")
                    dpg.add_table_column(label="Longitude")
                    dpg.add_table_column(label="Depth")
                    dpg.add_table_column(label="Done")
                    for i in range(0, 50):
                        with dpg.table_row():
                            dpg.add_text(str(i))
                            dpg.add_text("0.000000 °")
                            dpg.add_text("0.000000 °")
                            dpg.add_text("0.00 m")
                            chk = dpg.add_checkbox(tag="checkpoint_" + str(i), default_value=False)
                            dpg.configure_item(chk, enabled=False)

            self.section_header("MISC")
            with dpg.table(header_row=False, borders_innerH=True, borders_outerH=False, borders_innerV=False, borders_outerV=False):
                dpg.add_table_column()
                dpg.add_table_column()
                self.row("Mass", "Mass", "0.00 Kg")
                self.row("Ballast", "Ballast", "0.000 L / 5.0 L")
                self.row("Battery", "Battery", "0.000 %")
                self.row("Left Motor", "Left Throttle", "0.00")
                self.row("Center Motor", "Center Throttle", "0.00")
                self.row("Right Motor", "Right Throttle", "0.00")

    def update(self, values):
        for name, value in values.items():
            dpg.set_value(name, value[1])

    def row(self, label: str, tag: str, placeholder: str):
        """
        Creates a row to disable data in a table. Adds
        a tracking button, a label, and the data entry.
        """
        with dpg.table_row():
            dpg.add_text(label)
            dpg.add_text(placeholder, tag=tag)

    def section_header(self, label: str):
        """
        Adds a section header using the section header theme.
        """
        t = dpg.add_text(label)
        dpg.bind_item_theme(t, self._section_header_theme)

    def set_checkpoints(self, checkpoints):
        """
        Fills the checkpoint table with the checkpoint data.
        """
        children = dpg.get_item_children("checkpoint_table", 1)

        if children:
            for row in children:
                dpg.delete_item(row)

        for i, checkpoint in enumerate(checkpoints):
            with dpg.table_row(parent="checkpoint_table"):
                dpg.add_text(str(i))
                dpg.add_text(f"{checkpoint[0]:.6f} °")
                dpg.add_text(f"{checkpoint[1]:.6f} °")
                dpg.add_text(f"{checkpoint[2]:.3f} m")

                chk = dpg.add_checkbox(tag="checkpoint_" + str(i), default_value=checkpoint[3])
                dpg.configure_item(chk, enabled=False)