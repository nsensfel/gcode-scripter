#!/bin/env python3

def GCodeScripter:

   def __init__ (self, script):
      self.gcode_parser = NoGCodeInterpretation()
      self.printer = GenericPrinter()
      self.script = script

   def set_gcode (self, gcode):
      self.gcode_parser.parse(gcode)

   def get_gcode (self):
      return self.raw_gcode

   def set_gcode_parser (self, gcode_parser):
      gcode_parser.parse(self.gcode_parser.get_raw_gcode())
      self.gcode_parser = gcode_parser

   def set_printer (self, printer):
      self.printer = printer

   def process (self):
      self.script.initial_state(self.gcode_parser, self.printer)

      while (not self.gcode_parser.completed()):
         previous_printer = self.printer.clone()

         self.gcode_parser.step(self.printer)
         self.script.step(
            previous_printer,
            self.gcode_parser,
            self.printer
         )

      self.script.final_state(self.gcode_parser, self.printer)

################################################################################
#### SCRIPT MODE ###############################################################
################################################################################
if __name__ == "__main__":
   import argparse

   def load_module ():

   def check_module_is_printer (module):
   def check_module_is_gcode_parser (module):

   def load_printers ():
      

   def load_gcode_parsers ():
      

   printer_types = load_printers()
   gcode_parser_types = load_gcode_parsers()

   #### PARAMETERS PARSING #####################################################
   argument_parser = (
      argparse.ArgumentParser(
         prog='GCodeScripter.py',
         description='Utility to modify GCode files through scripting.',
         epilog='See https://gcode-scripter.segfault.tech for help.'
      )
   )

   argument_parser.add_argument(
      '-if',
      '--input-file',
      action='store',
      nargs=1,
      help='GCode file to read.'
   )

   argument_parser.add_argument(
      '-of',
      '--output-file',
      action='store',
      nargs=1,
      help='Output GCode file.'
   )

   argument_parser.add_argument(
      '-e',
      '--execute',
      action='store',
      nargs='+',
      help=(
         'Scripts to execute. Will be processed in order.'
         + ' Directories will be explored for scripts to execute in file name'
         + ' order.'
      )
   )

   argument_parser.add_argument(
      '-vpa',
      '--virtual-printer-argument',
      action='append',
      nargs=2,
      help=(
         '"NAME" "VALUE" argument to pass the virtual printer.'
         + ' Use -lvpa PRINTER_NAME to see available arguments.'
      )
   )

   argument_parser.add_argument(
      '-gpa',
      '--gcode-parser-argument',
      action='append',
      nargs=2,
      help=(
         '"NAME" "VALUE" argument to pass the GCode parser.'
         + ' Use -lgpa GCODE_PARSER_NAME to see available arguments.'
      )
   )

   argument_parser.add_argument(
      '-sa',
      '--script-argument',
      action='append',
      nargs=2,
      help=(
         '"NAME" "VALUE" argument to pass the script.'
         + ' Use -lsa SCRIPT_FILE to see available arguments.'
      )
   )

   available_printer_options = []

   for printer_module in printer_modules:
      available_printer_option
   argument_parser.add_argument(
      '-p',
      '--printer',
      action='store',
      nargs=1,
      help=(
         'Printer to use for status. Available options are:'
         + ' Directories will be explored for scripts to execute in file name'
         + ' order.'
      )
   )

   parsed_arguments = argument_parser.parse_args()

   if (parsed_arguments execute

   gcode_scripter = GCodeScripter()
