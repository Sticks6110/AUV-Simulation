import dearpygui.dearpygui as dpg
import numpy as np
from pandas import DataFrame

import data

class GUI:
    """
    
    """

    def __init__(self):
        dpg.create_context()
        dpg.configure_app(docking=True, docking_space=True, load_init_file="layout.ini")
        
        dpg.create_viewport(title='AUV Simulator', width=800, height=600)

        #Section Header Theme
        with dpg.theme() as self._section_header_theme:
            with dpg.theme_component(dpg.mvText):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (50, 100, 255))

        #Menu Bar
        with dpg.viewport_menu_bar():
            with dpg.menu(label="Settings"):
                dpg.add_menu_item(label="Save Layout", callback=lambda: dpg.save_init_file("layout.ini"))

        dpg.show_imgui_demo()

        with dpg.window(label="Data"):
            self.section_header("POSITION")
            with dpg.table(header_row=False, borders_innerH=True, borders_outerH=False, borders_innerV=False, borders_outerV=False):
                dpg.add_table_column(width_fixed=True, width=50)
                dpg.add_table_column()
                dpg.add_table_column()
                self.row("Latitude", "lat", "0.000000 °")
                self.row("Longitude", "lon", "0.000000 °")
                self.row("Depth", "depth", "0.00 m")

            self.section_header("VELOCITY (m/s)")
            with dpg.table(header_row=False, borders_innerH=True, borders_outerH=False, borders_innerV=False, borders_outerV=False):
                dpg.add_table_column(width_fixed=True, width=50)
                dpg.add_table_column()
                dpg.add_table_column()
                self.row("X", "velx", "0.000 (m/s)")
                self.row("Y", "vely", "0.000 (m/s)")
                self.row("Z", "velz", "0.000 (m/s)")

            self.section_header("ORIENTATION")
            with dpg.table(header_row=False, borders_innerH=True, borders_outerH=False, borders_innerV=False, borders_outerV=False):
                dpg.add_table_column(width_fixed=True, width=50)
                dpg.add_table_column()
                dpg.add_table_column()
                self.row("Yaw", "yaw", "0.000 °")
                self.row("Pitch", "pitch", "0.000 °")
                self.row("Roll", "roll", "0.000 °")

            self.section_header("ANGULAR VELOCITY (°/s)")
            with dpg.table(header_row=False, borders_innerH=True, borders_outerH=False, borders_innerV=False, borders_outerV=False):
                dpg.add_table_column(width_fixed=True, width=50)
                dpg.add_table_column()
                dpg.add_table_column()
                self.row("Yaw", "angvelx", "0.000 (°/s)")
                self.row("Pitch", "angvely", "0.000 (°/s)")
                self.row("Roll", "angvelz", "0.000 (°/s)")

            dpg.add_separator()

            with dpg.group(horizontal=True):
                self.add_vertical_guage("Ballast", "ballastlevellabel", "50 %", 0.5, "ballastfilllevel", 50, 200, (50, 100, 255, 255))
                self.add_vertical_guage("Battery", "batterylevellabel", "5 L", 0.5, "batterylevel", 50, 200, (50, 100, 255, 255))

        with dpg.window(label="Graph"):
            dpg.add_text("Bruh")

        # Setup
        dpg.setup_dearpygui()
        dpg.show_viewport()

        self._destroyed = False

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

    def row(self, label: str, tag: str, placeholder: str):
        """
        Creates a row to disable data in a table. Adds
        a tracking button, a label, and the data entry.
        """
        with dpg.table_row():
            dpg.add_button(label="Track")
            dpg.add_text(label)
            dpg.add_text(placeholder, tag=tag)

    def section_header(self, label: str):
        """
        Adds a section header using the section header theme.
        """
        t = dpg.add_text(label)
        dpg.bind_item_theme(t, self._section_header_theme)

    def add_vertical_guage(self, label: str, bottom_label_tag: str, bottom_label_placeholder: str, default_fill_level: float, fill_level_tag: str, width: float, height: float, color: tuple):
        """
        Adds a vertical guage.
        """
        with dpg.group():
            dpg.add_button(label="Track")
            dpg.add_text(label)

            with dpg.drawlist(width=width, height=height):
                dpg.draw_rectangle((0, 0), (width, height), color=(50, 50, 50, 255), fill=(30, 30, 30, 255))

                fill_h = height * default_fill_level

                dpg.draw_rectangle( (0, 200 - fill_h), (width, height), color=(0, 0, 0, 0), fill=color, tag=fill_level_tag)

            dpg.add_text(bottom_label_placeholder, tag=bottom_label_tag)