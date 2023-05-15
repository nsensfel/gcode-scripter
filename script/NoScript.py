class NoScript:

   def __init__ (self):
      self.step_counter = 0

   def initial_state (self, gcode_parser, printer):
      print("Running NoScript - Initial State")

   def final_state (self, gcode_parser, printer):
      print(
         "Running NoScript - Final State after "
         + str(self.step_counter)
         + " step(s)."
      )

   def step (self, previous_printer, gcode_parser, new_printer):
      self.step_counter = self.step_counter + 1
