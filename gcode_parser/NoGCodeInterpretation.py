class NoGCodeInterpretation:
   def reset (self):
      self.index = 0

   def __init__ (self):
      self.gcode = []

      self.reset()

   def get_raw_gcode_instruction_list (self):
      return self.gcode

   def parse (self, gcode):
      self.gcode = gcode

   def step (self, printer):
      self.index = self.index + 1

   def get_index (self):
      return self.index

   def get_previous_raw_gcode (self):
      return self.gcode[self.index - 1]

   def get_next_raw_gcode (self):
      return self.gcode[self.index]

   def insert_raw_gcode_after (self, raw_gcode):
      if (isinstance(raw_gcode, list)):
         self.gcode = (
            self.gcode[:(self.index + 1)]
            + raw_gcode
            + self.gcode[(self.index + 1):]
         )
      else:
         self.gcode.insert((self.index + 1), raw_gcode)

   def delete_next_gcode (self):
      del self.gcode[self.index]

   def completed (self):
      return (self.index == len(self.gcode))

