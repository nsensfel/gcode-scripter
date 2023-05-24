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

   # Disable All Stepper Motors
   def M18_gcode (self, parameters, comment, printer):
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

   # Pause SD Print
   def M25_gcode (self, parameters, comment, printer):
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

   # ATX Power On
   def M80_gcode (self, parameters, comment, printer):
      a = 0

   # ATX Power Off
   def M81_gcode (self, parameters, comment, printer):
      a = 0

   # Set Extruder to Absolute Mode
   def M82_gcode (self, parameters, comment, printer):
      a = 0

   # Set Extruder to Relative Mode
   def M83_gcode (self, parameters, comment, printer):
      a = 0

   # Stop Idle Hold
   def M84_gcode (self, parameters, comment, printer):
      a = 0

   # Set Inactivity Shutdown Timer
   def M85_gcode (self, parameters, comment, printer):
      a = 0

   # Set Safety Timer Expiration Time
   def M86_gcode (self, parameters, comment, printer):
      a = 0

   # Set axis_steps_per_unit
   def M92_gcode (self, parameters, comment, printer):
      a = 0

   # Set Extruder Temperature
   def M104_gcode (self, parameters, comment, printer):
      param = GCodeParser.split_basic_gcode_parameters(parameter)

      if ('S' in param):
         printer.set_hotend_temperature(int(param['S']))

   # Get Extruder Temperature
   def M105_gcode (self, parameters, comment, printer):
      a = 0

   # Fan On
   def M106_gcode (self, parameters, comment, printer):
      param = GCodeParser.split_basic_gcode_parameters(parameter)

      if ('S' in param):
         printer.set_print_fan_speed(int(param['S']))
      else:
         printer.set_print_fan_speed(255)

   # Fan Off
   def M107_gcode (self, parameters, comment, printer):
      printer.set_print_fan_speed(0)

   # Set Extruder Temperature and Wait
   def M109_gcode (self, parameters, comment, printer):
      param = GCodeParser.split_basic_gcode_parameters(parameter)

      if ('R' in param):
         printer.set_hotend_temperature(int(param['S']))
      elif (('B' in param) and ('S' in param)):
         printer.set_hotend_temperature(int(param['B']))
      elif ('S' in param):
         printer.set_hotend_temperature(int(param['S']))

   # Set Current Line Number
   def M110_gcode (self, parameters, comment, printer):
      param = GCodeParser.split_basic_gcode_parameters(parameter)

      # Will be incremented right after handling.
      self.line = int(param['S']) - 1

   # Full (Emergency) Stop
   def M112_gcode (self, parameters, comment, printer):
      a = 0

   # Host Keepalive
   def M113_gcode (self, parameters, comment, printer):
      a = 0

   # Get Current Position
   def M114_gcode (self, parameters, comment, printer):
      a = 0

   # Get Firmware Version and Capabilities
   def M115_gcode (self, parameters, comment, printer):
      a = 0

   # Display Message
   def M117_gcode (self, parameters, comment, printer):
      a = 0

   # Get Endstop Status
   def M119_gcode (self, parameters, comment, printer):
      a = 0

   # Enable Endstop Detection
   def M120_gcode (self, parameters, comment, printer):
      a = 0

   # Disable Endstop Detection
   def M121_gcode (self, parameters, comment, printer):
      a = 0

   # Tachometer Value
   def M123_gcode (self, parameters, comment, printer):
      a = 0

   # Pause Print
   def M125_gcode (self, parameters, comment, printer):
      a = 0

   # Set Bed Temperation (Fast)
   def M140_gcode (self, parameters, comment, printer):
      param = GCodeParser.split_basic_gcode_parameters(parameter)

      if ('S' in param):
         printer.set_bed_temperature(int(param['S']))

   # Set LED Color
   def M150_gcode (self, parameters, comment, printer):
      a = 0

   # Automatically Send Temperatures
   def M155_gcode (self, parameters, comment, printer):
      a = 0

   # Set Bed Temperature and Wait
   def M190_gcode (self, parameters, comment, printer):
      param = GCodeParser.split_basic_gcode_parameters(parameter)

      if ('R' in param):
         printer.set_bed_temperature(int(param['S']))
      elif ('S' in param):
         printer.set_bed_temperature(int(param['S']))

   # Set Filament Diameter
   def M200_gcode (self, parameters, comment, printer):
      a = 0

   # Set Max Printing Acceleration
   def M201_gcode (self, parameters, comment, printer):
      a = 0

   # Set Max Feedrate
   def M203_gcode (self, parameters, comment, printer):
      a = 0

   # Set Default Acceleration
   def M204_gcode (self, parameters, comment, printer):
      a = 0

   # Advanced Settings
   def M205_gcode (self, parameters, comment, printer):
      a = 0

   # Offset Axes
   def M206_gcode (self, parameters, comment, printer):
      a = 0

   # Set Retract Length
   def M207_gcode (self, parameters, comment, printer):
      a = 0

   # Set Unretract Length
   def M208_gcode (self, parameters, comment, printer):
      a = 0

   # Enable Automatic Retract
   def M209_gcode (self, parameters, comment, printer):
      a = 0

   # Set Hotend Offset
   def M218_gcode (self, parameters, comment, printer):
      a = 0

   # Set Speed Factor Override Percentage
   def M220_gcode (self, parameters, comment, printer):
      a = 0

   # Set Extrude Factor Override Percentage
   def M221_gcode (self, parameters, comment, printer):
      a = 0

   # Wait for Pin State
   def M226_gcode (self, parameters, comment, printer):
      a = 0

   # Trigger Camera
   def M240_gcode (self, parameters, comment, printer):
      a = 0

   # Set Servo Position
   def M280_gcode (self, parameters, comment, printer):
      a = 0

   # Play Beep Sound
   def M300_gcode (self, parameters, comment, printer):
      a = 0

   # Set PID Parameters
   def M301_gcode (self, parameters, comment, printer):
      a = 0

   # Allow Cold Extrudes
   def M302_gcode (self, parameters, comment, printer):
      a = 0

   # Run PID Tuning
   def M303_gcode (self, parameters, comment, printer):
      a = 0

   # Set PID Parameters - Bed
   def M304_gcode (self, parameters, comment, printer):
      a = 0

   # Wait for Current Moves to Finish
   def M400_gcode (self, parameters, comment, printer):
      a = 0

   # Set Filament Type (Material) for Particular Extruder and Notify the MMU
   def M403_gcode (self, parameters, comment, printer):
      a = 0

   # Store Parameters in Non-Volatile Storage
   def M500_gcode (self, parameters, comment, printer):
      a = 0

   # Read Parameters from EEPROM
   def M501_gcode (self, parameters, comment, printer):
      a = 0

   # Restore Default Settings
   def M502_gcode (self, parameters, comment, printer):
      a = 0

   # Report Current Settings
   def M503_gcode (self, parameters, comment, printer):
      a = 0

   # Force Language Selection
   def M509_gcode (self, parameters, comment, printer):
      a = 0

   # Enable/Disable "Stop SD Print on Endstop Hit"
   def M540_gcode (self, parameters, comment, printer):
      a = 0

   # Filament Change Pause
   def M600_gcode (self, parameters, comment, printer):
      a = 0
      # Assuming here that the parameters do not affect the location once the
      # command is completed.

   # Filament Change Pause
   def M601_gcode (self, parameters, comment, printer):
      a = 0
      # Assuming here that the parameters do not affect the location once the
      # command is completed.

   # Resume Print
   def M602_gcode (self, parameters, comment, printer):
      a = 0

   # Stop Print
   def M603_gcode (self, parameters, comment, printer):
      a = 0

   # Set Z-Probe Offset
   def M851_gcode (self, parameters, comment, printer):
      a = 0

   # Wait For Probe Temperature
   def M860_gcode (self, parameters, comment, printer):
      a = 0

   # Set Probe Thermal Compensation
   def M861_gcode (self, parameters, comment, printer):
      a = 0

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
