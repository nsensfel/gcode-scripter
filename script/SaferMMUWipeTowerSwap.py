from ConsoleOut import ConsoleOut

from script.Script import Script
from gcode_parser.GCodeParser import GCodeParser

class SaferMMUWipeTowerSwap (Script):

   def perform (self, gcode_parser, printer):
      if (gcode_parser.completed()):
         return

      gcode_line = gcode_parser.get_next_raw_gcode_line()

      if (
         gcode_line.startswith("T")
         and (gcode_line[1] >= '0')
         and (gcode_line[1] <= '9')
      ):
         if (self.ignore_next_filament_swap):
            self.ignore_next_filament_swap = False
            return

         # Pretty sure just setting 
         # self.ignore_next_filament_swap = True
         # would be enough there, but let's use the script tags, so it showcases
         # them.
         if (printer.has_temporary_tag("NEXT_SWAP_HANDLED")):
            gcode_parser.insert_raw_gcode_after(
               GCodeParser.generate_temporary_tag_instruction_raw_gcode(
                  "NEXT_SWAP_HANDLED unset"
               ),
               offset = 1
            )
            return

         inserted_gcode_list = []

         gcode_parser.delete_next_gcode_line()

         (ox, oy, oz) = printer.get_location()
         (max_x, max_y, max_z) = printer.get_print_area_size()
         is_in_relative_mode = printer.is_using_relative_positioning()

         tx = self.x_target
         ty = self.y_target
         tz = oz + self.z_step

         if (tz > max_z):
            ConsoleOut.error(
               "Script unable to raise Z axis further. Wants "
               + str(tz)
               + " but max is "
               + str(max_z)
               + ". Using max instead."
            )

            tz = max_z

         inserted_gcode_list.append("; SaferMMUWipeTowerSwap - Moving to swap.")

         if (is_in_relative_mode):
            inserted_gcode_list.append("G90") # Use absolute positioning

         inserted_gcode_list.append("G0 Z" + str(tz) + "; raise head before move.")
         inserted_gcode_list.append(
            "G0"
            + " X" + str(tx)
            + " Y" + str(ty)
            + "; Go to safe location."
         )

         inserted_gcode_list.append(
            GCodeParser.generate_temporary_tag_instruction_raw_gcode(
               "NEXT_SWAP_HANDLED set"
            )
         )

         inserted_gcode_list.append(gcode_line)

         inserted_gcode_list.append(
            "G0"
            + " X" + str(ox)
            + " Y" + str(oy)
            + "; Return to previous location, with Z still high."
         )
         inserted_gcode_list.append(
            "G0"
            + " Z" + str(oz)
            + "; Return to previous Z height."
         )

         if (is_in_relative_mode):
            inserted_gcode_list.append("G91") # Restore relative positioning

         inserted_gcode_list.append("; SaferMMUWipeTowerSwap - Completed swap.")

         gcode_parser.insert_raw_gcode_after(inserted_gcode_list)

         ConsoleOut.standard("Handled a tool change (\"" + gcode_line + "\").")

         self.replaced_swaps += 1

   def __init__ (self, params):
      self.replaced_swaps = 0
      self.ignore_next_filament_swap = True

      self.x_target = None
      self.y_target = 0
      self.z_step = 1

      for param in params:
         if (param[0] == "SMMUWTS_TARGET_X"):
            self.x_target = float(param[1])
         elif (param[0] == "SMMUWTS_TARGET_Y"):
            self.y_target = float(param[1])
         elif (param[0] == "SMMUWTS_Z_STEP"):
            self.z_step = float(param[1])

   def initial_state (self, gcode_parser, printer):
      ConsoleOut.standard("Running SaferMMUWipeTowerSwap - Initial State")

      (psx, psy, psz) = printer.get_print_area_size()

      if (self.x_target == None):
         self.x_target = psx

      if (self.x_target > psx):
         ConsoleOut.error(
            "SaferMMUWipeTowerSwap is set to target X position \""
            + str(self.x_target)
            + "\" but the print area is defined with a max X value of \""
            + str(psx)
            + "\"."
         )

      if (self.y_target > psy):
         ConsoleOut.error(
            "SaferMMUWipeTowerSwap is set to target Y position \""
            + str(self.y_target)
            + "\" but the print area is defined with a max Y value of \""
            + str(psy)
            + "\"."
         )

      ConsoleOut.standard(
         "SaferMMUWipeTowerSwap - Target is (X: "
         + str(self.x_target)
         + ", Y: "
         + str(self.y_target)
         + "), with Z increased by "
         + str(self.z_step)
         + " during move and swap."
      )

      self.perform(gcode_parser, printer)

   def final_state (self, gcode_parser, printer):
      ConsoleOut.standard(
         "Running SaferMMUWipeTowerSwap - Final State reached after "
         + str(self.replaced_swaps)
         + " replaced swaps."
      )

   def is_requesting_rerun (self):
      return False

   def uses_previous_printer (self):
      return False

   def step (self, previous_printer, gcode_parser, new_printer):
      self.perform(gcode_parser, new_printer)
