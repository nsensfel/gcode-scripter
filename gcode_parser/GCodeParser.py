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
         result_comment = line[1:]
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

   ##### Comment Handlers ######################################################
   def comment_handler (self, parameters, comment, printer):
      if (comment.startswith(" [TEMP_TAG] ")):
         printer.interpret_temporary_tag_instruction(
            comment[len(" [TEMP_TAG] "):]
         )
      elif (comment.startswith(" [PERMA_TAG] ")):
         printer.interpret_permanent_tag_instruction(
            comment[len(" [PERMA_TAG] "):]
         )

   ##### M-Code Handlers #######################################################
   # Enable/Power All Stepper Motors
   def M17_gcode (self, parameters, comment, printer):
      a = 0

   # List SD Card
   def M20_gcode (self, parameters, comment, printer):
      a = 0

   # Initialize SD Card
   def M21_gcode (self, parameters, comment, printer):
      a = 0

   # Release SD Card
   def M22_gcode (self, parameters, comment, printer):
      a = 0

   # Select SD File
   def M23_gcode (self, parameters, comment, printer):
      a = 0

   # Start/Resume SD Print
   def M24_gcode (self, parameters, comment, printer):
      a = 0

   # Set SD Position
   def M26_gcode (self, parameters, comment, printer):
      a = 0

   # Report SD Print Status
   def M27_gcode (self, parameters, comment, printer):
      a = 0

   # Begin Write to SD Card
   def M28_gcode (self, parameters, comment, printer):
      a = 0

   # Stop Writing to SD Card
   def M29_gcode (self, parameters, comment, printer):
      a = 0

   # Delete a File on the SD Card
   def M30_gcode (self, parameters, comment, printer):
      a = 0

   # Output Time Since Last M109 or SD Card Start to Serial
   def M31_gcode (self, parameters, comment, printer):
      a = 0

   # Select File and Start SD Print
   def M32_gcode (self, parameters, comment, printer):
      a = 0

   # Switch I/O Pin
   def M42_gcode (self, parameters, comment, printer):
      a = 0

   # Reset the Bed Skew and Offset Calibration
   def M44_gcode (self, parameters, comment, printer):
      a = 0

   # Bed Skew and Offset with Manual Z Up
   def M45_gcode (self, parameters, comment, printer):
      a = 0

   # Show the Assigned IP Address
   def M46_gcode (self, parameters, comment, printer):
      a = 0

   # Show End Stops Dialog on the Display
   def M47_gcode (self, parameters, comment, printer):
      a = 0

   # Measure Z-Prove Repeatability
   def M48_gcode (self, parameters, comment, printer):
      a = 0

   # Set/Get Build Percentage
   def M73_gcode (self, parameters, comment, printer):
      a = 0

   # Set Extruder Temperature
   def M104_gcode (self, parameters, comment, printer):
      param = GCodeParser.split_basic_gcode_parameters(parameter)

      if ('S' in param):
         printer.set_hotend_temperature(int(param['S']))

   # Get Extruder Temperature
   def M105_gcode (self, parameters, comment, printer):
      a = 0

   # Full (Emergency) Stop
   def M112_gcode (self, parameters, comment, printer):
      a = 0

   # Set Bed Temperation (Fast)
   def M140_gcode (self, parameters, comment, printer):
      param = GCodeParser.split_basic_gcode_parameters(parameter)

      if ('S' in param):
         printer.set_bed_temperature(int(param['S']))

   # Start SD Logging
   def M928_gcode (self, parameters, comment, printer):
      a = 0

   ##### Special Handlers ######################################################
   def PRUSA_gcode (self, parameters, comment, printer):
      # TODO
      a = 0

   ##### G-Code Handlers #######################################################
   # Move without extruding
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

   # Move while extruding
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

   # Clockwise Arc Move
   def G2_gcode (self, parameters, comment, printer):
      printer.set_is_extruding(True)

      param = GCodeParser.split_basic_gcode_parameters(parameter)

      (x, y, z) = printer.get_location()

      if (printer.is_using_relative_positioning()):
         printer.set_location(
            ((x + float(param['X'])) if 'X' in param else x),
            ((y + float(param['Y'])) if 'Y' in param else y),
            z
         )
      else:
         printer.set_location(
            (float(param['X']) if 'X' in param else x),
            (float(param['Y']) if 'Y' in param else y),
            z
         )

   # Counter-Clockwise Arc Move
   def G3_gcode (self, parameters, comment, printer):
      printer.set_is_extruding(True)

      param = GCodeParser.split_basic_gcode_parameters(parameter)

      (x, y, z) = printer.get_location()

      if (printer.is_using_relative_positioning()):
         printer.set_location(
            ((x + float(param['X'])) if 'X' in param else x),
            ((y + float(param['Y'])) if 'Y' in param else y),
            z
         )
      else:
         printer.set_location(
            (float(param['X']) if 'X' in param else x),
            (float(param['Y']) if 'Y' in param else y),
            z
         )

   # Dwell
   def G4_gcode (self, parameters, comment, printer):
      printer.set_is_extruding(False)

   # Retract
   def G10_gcode (self, parameters, comment, printer):
      printer.set_is_extruding(False)

   # Retract Recover
   def G11_gcode (self, parameters, comment, printer):
      printer.set_is_extruding(False)

   # Set Units to Millimeters
   def G21_gcode (self, parameters, comment, printer):
      a = 0

   # Move to Origin (Home)
   def G28_gcode (self, parameters, comment, printer):
      printer.set_is_extruding(False)
      printer.set_location(0.0, 0.0, 0.0)

   # Detailed Z-Probe
   def G29_gcode (self, parameters, comment, printer):
      a = 0

   # Single Z-Probe
   def G30_gcode (self, parameters, comment, printer):
      a = 0

   # Dock Z-Probe Sled
   def G31_gcode (self, parameters, comment, printer):
      a = 0

   # Undock Z-Probe Sled
   def G32_gcode (self, parameters, comment, printer):
      a = 0

   # Print temperature interpolation
   def G75_gcode (self, parameters, comment, printer):
      a = 0

   # PINDA probe temperature calibration
   def G76_gcode (self, parameters, comment, printer):
      a = 0

   # Mesh-based Z probe
   def G80_gcode (self, parameters, comment, printer):
      printer.set_location(0.0, 0.0, 0.0)

   # Mesh bed leveling status
   def G81_gcode (self, parameters, comment, printer):
      a = 0

   # Single Z probe at current location
   def G82_gcode (self, parameters, comment, printer):
      a = 0

   # Babystep in Z and store to EEPROM
   def G83_gcode (self, parameters, comment, printer):
      a = 0

   # UNDO Babystep in Z (move Z axis back)
   def G84_gcode (self, parameters, comment, printer):
      a = 0

   # Pick best babystep
   def G85_gcode (self, parameters, comment, printer):
      a = 0

   # Disable babystep correction after home
   def G86_gcode (self, parameters, comment, printer):
      a = 0

   # Enable babystep correction after home
   def G87_gcode (self, parameters, comment, printer):
      a = 0

   # Reserved
   def G88_gcode (self, parameters, comment, printer):
      a = 0

   # Set to Absolute Positioning
   def G90_gcode (self, parameters, comment, printer):
      printer.set_is_using_relative_positioning(False)

   # Set to Relative Positioning
   def G91_gcode (self, parameters, comment, printer):
      printer.set_is_using_relative_positioning(True)

   # Set Position (defines current location, does not move)
   def G92_gcode (self, parameters, comment, printer):
      # FIXME: Don't know how to handle that.
      param = GCodeParser.split_basic_gcode_parameters(parameter)

      (x, y, z) = printer.get_location()

      printer.set_location(
         ((x + float(param['X'])) if 'X' in param else x),
         ((y + float(param['Y'])) if 'Y' in param else y),
         ((z + float(param['Z'])) if 'Z' in param else z)
      )

   # Activate Farm Mode
   def G98_gcode (self, parameters, comment, printer):
      a = 0

   # Deactivate Farm Mode
   def G99_gcode (self, parameters, comment, printer):
      a = 0

######## Comment Handler #######################################################
GCodeParser.GCODE_HANDLER[''] = GCodeParser.comment_handler

######## G-Code Handlers #######################################################
GCodeParser.GCODE_HANDLER['G0'] = GCodeParser.G0_gcode
GCodeParser.GCODE_HANDLER['G1'] = GCodeParser.G1_gcode
GCodeParser.GCODE_HANDLER['G4'] = GCodeParser.G4_gcode
GCodeParser.GCODE_HANDLER['G10'] = GCodeParser.G10_gcode
GCodeParser.GCODE_HANDLER['G11'] = GCodeParser.G11_gcode
GCodeParser.GCODE_HANDLER['G21'] = GCodeParser.G21_gcode
GCodeParser.GCODE_HANDLER['G28'] = GCodeParser.G28_gcode
GCodeParser.GCODE_HANDLER['G29'] = GCodeParser.G29_gcode
GCodeParser.GCODE_HANDLER['G30'] = GCodeParser.G30_gcode
GCodeParser.GCODE_HANDLER['G31'] = GCodeParser.G31_gcode
GCodeParser.GCODE_HANDLER['G32'] = GCodeParser.G32_gcode
GCodeParser.GCODE_HANDLER['G75'] = GCodeParser.G75_gcode
GCodeParser.GCODE_HANDLER['G76'] = GCodeParser.G76_gcode
GCodeParser.GCODE_HANDLER['G80'] = GCodeParser.G80_gcode
GCodeParser.GCODE_HANDLER['G81'] = GCodeParser.G81_gcode
GCodeParser.GCODE_HANDLER['G82'] = GCodeParser.G82_gcode
GCodeParser.GCODE_HANDLER['G83'] = GCodeParser.G83_gcode
GCodeParser.GCODE_HANDLER['G84'] = GCodeParser.G84_gcode
GCodeParser.GCODE_HANDLER['G85'] = GCodeParser.G85_gcode
GCodeParser.GCODE_HANDLER['G86'] = GCodeParser.G86_gcode
GCodeParser.GCODE_HANDLER['G87'] = GCodeParser.G87_gcode
GCodeParser.GCODE_HANDLER['G88'] = GCodeParser.G88_gcode
GCodeParser.GCODE_HANDLER['G90'] = GCodeParser.G90_gcode
GCodeParser.GCODE_HANDLER['G91'] = GCodeParser.G91_gcode
GCodeParser.GCODE_HANDLER['G92'] = GCodeParser.G92_gcode
GCodeParser.GCODE_HANDLER['G98'] = GCodeParser.G98_gcode
GCodeParser.GCODE_HANDLER['G99'] = GCodeParser.G99_gcode

######## M-Code Handlers #######################################################
