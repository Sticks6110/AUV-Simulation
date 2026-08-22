import dearpygui.dearpygui as dpg

dpg.create_context()

class Popup:
    """
    This popup lets the user set the parameters of the AUV before starting
    the simulation.
    """

    def __init__(self, callback: function):
        """
        """
        self._destroyed = False
        self._checkpoints = []

        with dpg.window(label="Add Checkpoint", modal=True, show=False, tag="add_checkpoint_modal", no_title_bar=True, autosize=True):
            with dpg.group(horizontal=True):
                dpg.add_text("Latitude")
                dpg.add_input_double(default_value=32.5, tag="check_lat", format="%.6f")

            with dpg.group(horizontal=True):
                dpg.add_text("Longitude")
                dpg.add_input_double(default_value=-72.5, tag="check_lon", format="%.6f")

            with dpg.group(horizontal=True):
                dpg.add_text("Depth")
                dpg.add_input_float(default_value=-25.0, tag="check_depth")

            with dpg.group(horizontal=True):
                dpg.add_button(label="Add", width=75, callback=lambda: self.add_checkpoint())
                dpg.add_button(label="Cancel", width=75, callback=lambda: dpg.configure_item("add_checkpoint_modal", show=False))

        with dpg.window(label="Remove Checkpoint", modal=True, show=False, tag="remove_checkpoint_modal", no_title_bar=True, autosize=True):
            with dpg.group(horizontal=True):
                dpg.add_text("ID")
                dpg.add_input_int(default_value=0, tag="check_id")

            with dpg.group(horizontal=True):
                dpg.add_button(label="Remove", width=75, callback=lambda: self.remove_checkpoint())
                dpg.add_button(label="Cancel", width=75, callback=lambda: dpg.configure_item("remove_checkpoint_modal", show=False))

        with dpg.window(tag="Primary Window"):
            with dpg.table(header_row=False, borders_innerH=True, borders_outerH=False, borders_innerV=False, borders_outerV=False):
                dpg.add_table_column()
                dpg.add_table_column()
                #def __init__(self, mass: float, drag_cof: float, ballast_max: float, battery_max: float, battery_consumption: float, motor_wattage: float, motor_rpm: float, motor_thrust_cof: float):

                with dpg.table_row():
                    dpg.add_text("Latitude")
                    dpg.add_input_double(default_value=32.5, tag="lat", format="%.6f")
                with dpg.table_row():
                    dpg.add_text("Longitude")
                    dpg.add_input_double(default_value=-72.5, tag="lon", format="%.6f")
                with dpg.table_row():
                    dpg.add_text("Dry Mass (Kg)")
                    dpg.add_input_float(default_value=8, tag="mass")
                with dpg.table_row():
                    dpg.add_text("Ballast Capacity (L)")
                    dpg.add_input_float(default_value=10, tag="ballast")
                with dpg.table_row():
                    dpg.add_text("Battery (watt-hours)")
                    dpg.add_input_float(default_value=1000, tag="battery")
                with dpg.table_row():
                    dpg.add_text("Battery Consumption (watts per second)")
                    dpg.add_input_float(default_value=20, tag="battery_consumption")
                with dpg.table_row():
                    dpg.add_text("Motor Wattage (watts)")
                    dpg.add_input_float(default_value=400, tag="motor_watts")
                with dpg.table_row():
                    dpg.add_text("Motor Max RPM")
                    dpg.add_input_float(default_value=3600, tag="motor_rpm")
                with dpg.table_row():
                    dpg.add_text("Motor Thrust Coefficient")
                    dpg.add_input_float(default_value=0.1, tag="motor_thrust")

            dpg.add_separator()

            with dpg.group(horizontal=True):
                dpg.add_button(label="Add Checkpoint", callback=lambda: dpg.configure_item("add_checkpoint_modal", show=True))
                dpg.add_button(label="Remove Checkpoint", callback=lambda: dpg.configure_item("remove_checkpoint_modal", show=True))
            with dpg.child_window(height=150, border=True):
                with dpg.table(header_row=True, tag="checkpoint_table"):
                    dpg.add_table_column(label="Checkpoint")
                    dpg.add_table_column(label="Latitude")
                    dpg.add_table_column(label="Longitude")
                    dpg.add_table_column(label="Depth")

            dpg.add_separator()

            dpg.add_button(label="Run", width=-1, callback=lambda: self.run_pressed(callback))

        dpg.create_viewport(title='AUV Setup', width=800, height=475)

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Primary Window", True)

        dpg.start_dearpygui()

    def remove_checkpoint(self):
        """
        Removes a checkpoint from the list
        with the data from the modal. Then closes the
        modal and updates the table.
        """
        dpg.configure_item("remove_checkpoint_modal", show=False)
        
        id = dpg.get_value("check_id")

        del self._checkpoints[id]
        self.checkpoints_changed()

    def add_checkpoint(self):
        """
        Adds a checkpoint to the checkpoints list
        with the data from the modal. Then closes the
        modal and updates the table.
        """
        dpg.configure_item("add_checkpoint_modal", show=False)

        lat = dpg.get_value("check_lat")
        lon = dpg.get_value("check_lon")
        depth = dpg.get_value("check_depth")

        self._checkpoints.append((lat, lon, depth))
        self.checkpoints_changed()


    def checkpoints_changed(self):
        """
        Updates the checkpoints table
        """
        children = dpg.get_item_children("checkpoint_table", 1)
        
        if children:
            for row in children:
                dpg.delete_item(row)

        for i, checkpoint in enumerate(self._checkpoints):
            with dpg.table_row(parent="checkpoint_table"):
                dpg.add_text(str(i))
                dpg.add_text(f"{checkpoint[0]:.6f} °")
                dpg.add_text(f"{checkpoint[1]:.6f} °")
                dpg.add_text(f"{checkpoint[2]:.3f} m")

    def run_pressed(self, callback: function):
        """
        Destroys the current context and then
        calls the callback function with the
        data.
        """
        lat = dpg.get_value("lat")
        lon = dpg.get_value("lon")
        mass = dpg.get_value("mass")
        ballast = dpg.get_value("ballast")
        battery = dpg.get_value("battery")
        battery_consumption = dpg.get_value("battery_consumption")
        motor_watts = dpg.get_value("motor_watts")
        motor_rpm = dpg.get_value("motor_rpm")
        motor_thrust = dpg.get_value("motor_thrust")

        dpg.stop_dearpygui()

        callback((lat, lon, mass, ballast, battery, battery_consumption, motor_watts, motor_rpm, motor_thrust, self._checkpoints))