class GCodeParser:
   GCODE_HANDLER = dict()

   #############################################################################
   def parse_raw_gcode_line (line):
      result_instruction = ""
      result_params = ""
      result_comment = None

      line = line.split(';', 1)

      if (1 in line):
         result_comment = line[1]

      line = line[0].trim()

      if (line.startswith(';')):
         result_comment = line
      else:
         line = line.split('0', 1)
         result_instruction = line[0].trim()

         if (1 in line):
            result_params = line[1].trim()

      return (result_instruction, result_params, result_comment)

   def split_basic_gcode_parameters (arguments):
      result = dict()

      arguments.split(' ')

      for argument in arguments:
         if len(argument) == 1:
            result[argument[0]] = True
         elif len(argument) > 1:
            result[argument[0]] = argument[1:]

      return result

   #############################################################################
   def reset (self):
      self.index = 0

   def __init__ (self):
      self.gcode = []

      self.reset()

   def get_raw_gcode_lines (self):
      return self.gcode

   def load_raw_gcode_lines (self, gcode):
      self.gcode = gcode


   def step (self, printer):
      if (self.completed()):
         return

      (instruction, params, comment) = (
         parse_raw_gcode_line(self.gcode[self.index])
      )

      if (len(instruction) > 0):
         fun = GCodeParser.GCODE_HANDLER[instruction]

         if (fun is None):
            ConsoleOut.warning(
               "G-Code parser met unknown instruction \""
               + instruction
               + "\""
            )
         else:
            fun(self, params, comment, printer)

      self.index = self.index + 1

   def get_index (self):
      return self.index

   def get_gcode_length (self):
      return len(self.gcode)

   def get_previous_raw_gcode_line (self):
      return self.gcode[self.index - 1]

   def get_next_raw_gcode_line (self):
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

   def delete_next_gcode_line (self):
      del self.gcode[self.index]

   def completed (self):
      return (self.index == len(self.gcode))

   def stop (self):
      self.index = len(self.gcode)

   ##### M-Code Handlers #######################################################
   def M0_gcode (self, parameters, comment, printer):
      a = 0

   def M1_gcode (self, parameters, comment, printer):
      a = 0

   ##### G-Code Handlers #######################################################
   def G0_gcode (self, parameters, comment, printer):
      printer.set_is_extruding(False)

      param = GCodeParser.split_basic_gcode_parameters(parameter)

      (x, y, z) = printer.get_location()

      if (printer.is_using_relative_positioning()):
         printer.set_location(
            ((x + float(param['X'])) if 'X' in param else x),
            ((y + float(param['Y'])) if 'Y' in param else y),
            ((z + float(param['Z'])) if 'Z' in param else z)
         )
      else:
         printer.set_location(
            (float(param['X']) if 'X' in param else x),
            (float(param['Y']) if 'Y' in param else y),
            (float(param['Z']) if 'Z' in param else z)
         )

   def G1_gcode (self, parameters, comment, printer):
      printer.set_is_extruding(True)

      param = GCodeParser.split_basic_gcode_parameters(parameter)

      (x, y, z) = printer.get_location()

      if (printer.is_using_relative_positioning()):
         printer.set_location(
            ((x + float(param['X'])) if 'X' in param else x),
            ((y + float(param['Y'])) if 'Y' in param else y),
            ((z + float(param['Z'])) if 'Z' in param else z)
         )
      else:
         printer.set_location(
            (float(param['X']) if 'X' in param else x),
            (float(param['Y']) if 'Y' in param else y),
            (float(param['Z']) if 'Z' in param else z)
         )

######## G-Code Handlers #######################################################
GCodeParser.GCODE_HANDLER['G0'] = GCodeParser.G0_gcode
GCodeParser.GCODE_HANDLER['G1'] = GCodeParser.G1_gcode

######## M-Code Handlers #######################################################
