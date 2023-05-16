from ConsoleOut import ConsoleOut

class Script:

   def __init__ (self):
      self.step_counter = 0

   def initial_state (self, gcode_parser, printer):
      ConsoleOut.standard("Running Script - Initial State")

   def final_state (self, gcode_parser, printer):
      ConsoleOut.standard(
         "Running Script - Final State after "
         + str(self.step_counter)
         + " step(s)."
      )

   def is_requesting_rerun (self):
      return False

   def uses_previous_printer (self):
      return False

   def step (self, previous_printer, gcode_parser, new_printer):
      self.step_counter = self.step_counter + 1
