# Author: Brennan Werner
# Date Created: 8/20/26

import dearpygui.dearpygui as dpg
import numpy as np
import time
from collections import deque
from pandas import DataFrame

import data

class Oscilloscope:
    def __init__(self, max_seconds=25.0):
        self._max_seconds = max_seconds
        self._time = 0

        self._data = {}

        with dpg.window(label="Oscilloscope", tag="oscilloscope_window",):
            with dpg.plot(label="", height=-1, width=-1, tag="oscilloscope_plot"):
                dpg.add_plot_legend()

                dpg.add_plot_axis(dpg.mvXAxis, label="Time (s)", tag="osc_x_axis")

                with dpg.plot_axis(dpg.mvYAxis, label="Value", tag="osc_y_axis"):
                    pass

    def add_variable(self, name):
        self._data[name] = {
            "time": deque(maxlen=1000),
            "value": deque(maxlen=1000),
        }

        dpg.add_line_series([], [], label=name, parent="osc_y_axis", tag=f"series_{name}")

    def update(self, values):
        now = self._time + 0.2
        self._time += 0.2

        for name, value in values.items():

            if name not in self._data:
                continue

            self._data[name]["time"].append(now)
            self._data[name]["value"].append(value[0])

            dpg.set_value(f"series_{name}",
                [
                    list(self._data[name]["time"]),
                    list(self._data[name]["value"]),
                ],
            )

        dpg.set_axis_limits("osc_x_axis", max(0, now - self._max_seconds), max(self._max_seconds, now))