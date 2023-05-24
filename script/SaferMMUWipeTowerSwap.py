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

         if (printer.has_temporary_tag("NEXT_SWAP_HANDLED")):
            gcode_parser.insert_raw_gcode_after(
               GCodeParser.generate_temporary_tag_instruction_raw_gcode(
                  "NEXT_SWAP_HANDLED unset"
               ),
               offset = 1
            )
            self.ignore_next_filament_swap = True
            return

         inserted_gcode_list = []

         gcode_parser.delete_next_gcode_line()

         (ox, oy, oz) = printer.get_location()
         (max_x, max_y, max_z) = printer.get_print_area_size()
         is_in_relative_mode = printer.is_using_relative_positioning()

         tx = max_x
         ty = 0
         tz = oz + 1

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

         ConsoleOut.standard("Handled a tool change.")

         self.replaced_swaps += 1

   def __init__ (self):
      self.replaced_swaps = 0
      self.ignore_next_filament_swap = True

   def initial_state (self, gcode_parser, printer):
      ConsoleOut.standard("Running SaferMMUWipeTowerSwap - Initial State")
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
