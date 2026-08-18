import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.configure_app(docking=True, docking_space=True, load_init_file="layout.ini")

#Windows
with dpg.window(label="AUV Data", tag="AUVWin"):

    #Position
    dpg.add_text("POSITION")
    dpg.add_separator()
    with dpg.table(header_row=True):
        dpg.add_table_column(label="Parameter", width_fixed=True, init_width_or_weight=150)
        dpg.add_table_column(label="Lat", width_fixed=True, init_width_or_weight=80)
        dpg.add_table_column(label="Lon", width_fixed=True, init_width_or_weight=80)

        with dpg.table_row():
            dpg.add_text("Coordinates")
            dpg.add_text("40.741")
            dpg.add_text("-73.989")

        with dpg.table_row():
            dpg.add_text("Depth")
            dpg.add_text("30 m")
            dpg.add_text("")

    dpg.add_spacer(height=8)

    # Orientation
    dpg.add_text("ORIENTATION")
    dpg.add_separator()

    with dpg.table(header_row=True):
        dpg.add_table_column(label="Parameter", width_fixed=True, init_width_or_weight=150)
        dpg.add_table_column(label="Roll", width_fixed=True, init_width_or_weight=80)
        dpg.add_table_column(label="Pitch", width_fixed=True, init_width_or_weight=80)
        dpg.add_table_column(label="Yaw", width_fixed=True, init_width_or_weight=80)

        with dpg.table_row():
            dpg.add_text("Orientation")
            dpg.add_text("30")
            dpg.add_text("30")
            dpg.add_text("30")

    dpg.add_spacer(height=8)
    
    # Motion
    dpg.add_text("MOTION")
    dpg.add_separator()

    with dpg.table(header_row=True):
        dpg.add_table_column(label="Parameter", width_fixed=True, init_width_or_weight=150)
        dpg.add_table_column(label="X", width_fixed=True, init_width_or_weight=80)
        dpg.add_table_column(label="Y", width_fixed=True, init_width_or_weight=80)
        dpg.add_table_column(label="Z", width_fixed=True, init_width_or_weight=80)

        with dpg.table_row():
            dpg.add_text("Velocity m/s")
            dpg.add_text("30")
            dpg.add_text("30")
            dpg.add_text("30")

        with dpg.table_row():
            dpg.add_text("Angular Velocity deg/s")
            dpg.add_text("30")
            dpg.add_text("30")
            dpg.add_text("30")


dpg.create_viewport(title='AUV Simulator', width=800, height=600)

#Menu Bar
with dpg.viewport_menu_bar():
    with dpg.menu(label="Settings"):
        dpg.add_menu_item(label="Save Layout", callback=lambda: dpg.save_init_file("layout.ini"))


# Setup
dpg.setup_dearpygui()

#Loop
dpg.show_viewport()
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

# Destruction
dpg.destroy_context()