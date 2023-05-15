def SaferMMUWipeTowerSwap:

   def perform (self, gcode_parser, printer):
      gcode_line = gcode_parser.get_next_gcode_raw()

      if (gcode_line.startswith("T")):
         if (self.ignore_next_filament_swap):
            self.ignore_filament_swap = False
            return

         if (printer.has_script_tag("NEXT_SWAP_HANDLED")):
            printer.remove_script_tag("NEXT_SWAP_HANDLED")
            self.ignore_filament_swap = True
            return

         inserted_gcode_list = []

         gcode_parser.delete_next_gcode()

         (ox, oy, oz) = printer.get_current_location()
         (max_x, max_y, max_z) = printer.get_print_area_dimensions()
         is_in_relative_mode = printer.get_is_using_relative_coordinates()

         tx = max_x
         ty = 0
         tz = oz + 1

         if (tz > max_z):
            raise ...

         if (is_in_relative_mode):
            inserted_gcode_list.add("G90") # Use absolute positioning

         inserted_gcode_list.add("goto ox, oy, tz")
         inserted_gcode_list.add("goto tx, ty, tz")
         inserted_gcode_list.add("; [SCRIPT TAG] NEXT_SWAP_HANDLED")
         inserted_gcode_list.add(gcode_line)
         inserted_gcode_list.add("goto ox, oy, tz")
         inserted_gcode_list.add("goto ox, oy, oz")

         if (is_in_relative_mode):
            inserted_gcode_list.add("G91") # Restore relative positioning

         gcode_parser.insert_raw_gcode_after(inserted_gcode_list)

   def __init__ (self):
      # Ignore the first filament loading.
      self.ignore_next_filament_swap = True

   def initial_state (self, gcode_parser, printer):
      self.perform(gcode_parser, printer):

   def final_state (self, gcode_parser, printer):
      # Do Nothing

   def step (self, previous_printer, gcode_parser, new_printer):
      self.perform(gcode_parser, new_printer):
