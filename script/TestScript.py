from ConsoleOut import ConsoleOut

from script.Script import Script

class TestScript(Script):

   def __init__ (self):
      self.step_counter = 0
      self.max_z = 0

   def initial_state (self, gcode_parser, printer):
      ConsoleOut.standard("Running TestScript - Initial State")

   def final_state (self, gcode_parser, printer):
      ConsoleOut.standard(
         "Running TestScript - Final State after "
         + str(self.step_counter)
         + " step(s)."
      )

   def is_requesting_rerun (self):
      return False

   def uses_previous_printer (self):
      return False

   def step (self, previous_printer, gcode_parser, new_printer):
      self.step_counter = self.step_counter + 1
      z = new_printer.get_location_z()

      if (z > self.max_z):
         ConsoleOut.standard("New max z:" + str(z))
         self.max_z = z
