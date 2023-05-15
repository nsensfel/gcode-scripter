#!/bin/env python3

from gcode_parser.NoGCodeInterpretation import NoGCodeInterpretation
from printer.GenericPrinter import GenericPrinter
from script.NoScript import NoScript

class GCodeScripter:

   def __init__ (self):
      self.gcode_parser = NoGCodeInterpretation()
      self.printer = GenericPrinter()
      self.script = NoScript()

   def set_script (self, script):
      self.script = script

   def set_gcode (self, gcode):
      self.gcode_parser.parse(gcode)

   def get_gcode (self):
      return self.gcode_parser.get_raw_gcode_instruction_list()

   def set_gcode_parser (self, gcode_parser):
      gcode_parser.parse(self.gcode_parser.get_raw_gcode_instruction_list())
      self.gcode_parser = gcode_parser

   def set_printer (self, printer):
      self.printer = printer

   def reset (self):
      self.gcode_parser.reset()
      self.printer.reset()

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
   import os

   def extract_class_name (name):
      if (name.endswith(".py")):
         name = name[:-len(".py")]
      try:
         return name[(name.rindex(".") + 1):]
      except Exception:
         return name

   #def load_module ():

   #def check_module_is_printer (module):

   #def check_module_is_gcode_parser (module):

   #printer_types = load_printers()
   #gcode_parser_types = load_gcode_parsers()

   #### PARAMETERS PARSING #####################################################
   argument_parser = (
      argparse.ArgumentParser(
         prog='GCodeScripter.py',
         description='Utility to modifyG-Codefiles through scripting.',
         epilog='See https://gcode-scripter.segfault.tech for help.'
      )
   )

   argument_parser.add_argument(
      '-if',
      '--input-file',
      action='store',
      nargs=1,
      help='G-Code file to read.'
   )

   argument_parser.add_argument(
      '-of',
      '--output-file',
      action='store',
      nargs=1,
      help='OutputG-Codefile.'
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
         '"NAME" "VALUE" argument to pass theG-Codeparser.'
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

   argument_parser.add_argument(
      '-vp',
      '--virtual-printer',
      action='store',
      nargs=1,
      help=(
         'Virtual printer to use for status. Available options are:'
      )
   )

   argument_parser.add_argument(
      '-gp',
      '--gcode-parser',
      action='store',
      nargs=1,
      help=(
         'G-Code parser to use for interpretation. Available options are:'
      )
   )

   parsed_arguments = argument_parser.parse_args()

   gcode_scripter = GCodeScripter()

   def script_name_to_script_class (script_name):
      script_module = None

      while True:
         try:
            script_module = importlib.import_module(script_name)
         except Exception:
            a = 0

         if (script_module is not None):
            break

         try:
            script_module = importlib.import_module("script." + script_name)
         except Exception:
            a = 0

         if (script_module is not None):
            break

         print("[E] Could not find script module \"" + script_name + "\".")
         break

      return getattr(
         script_module,
         extract_class_name(script_name)
      )

   def argument_to_script_list (argument):
      result = []

      #if (script is dir):
      #  get_py_file_list, sort, run_scripts(gcode_scripter)

      for script_name in argument:
         if (os.path.exists(script_name)):
            result.append(script_name)
         elif (os.path.exists(script_name + ".py")):
            result.append(script_name)
         elif (os.path.exists("script" + os.path.sep + script_name)):
            result.append("script." + script_name[:-len(".py")])
         elif (os.path.exists("script" + os.path.sep + script_name + ".py")):
            result.append("script." + script_name)
         else:
            print("[E] Could not find script path \"" + script_name + "\".")

      return result


   def run_scripts (gcode_scripter, script_class_list):
      for script in script_class_list:
         gcode_scripter.set_script(script())
         gcode_scripter.process()
         gcode_scripter.reset()

   if (parsed_arguments.virtual_printer is not None):
      import importlib

      printer_module = None

      while True:
         try:
            printer_module = (
               importlib.import_module(parsed_arguments.virtual_printer[0])
            )
         except Exception:
            a = 0

         if (printer_module is not None):
            break

         try:
            printer_module = (
               importlib.import_module(
                  "printer."
                  + parsed_arguments.virtual_printer[0]
               )
            )
         except Exception:
            a = 0

         if (printer_module is not None):
            break

         print("[E] Could not find printer.")
         break

      printer_class = (
         getattr(
            printer_module,
            extract_class_name(parsed_arguments.virtual_printer[0])
         )
      )

      gcode_scripter.set_printer(printer_class())

   if (parsed_arguments.gcode_parser is not None):
      import importlib

      gcode_parser_module = None

      while True:
         try:
            gcode_parser_module = (
               importlib.import_module(parsed_arguments.gcode_parser[0])
            )
         except Exception:
            a = 0

         if (gcode_parser_module is not None):
            break

         try:
            gcode_parser_module = (
               importlib.import_module(
                  "gcode_parser."
                  + parsed_arguments.gcode_parser[0]
               )
            )
         except Exception:
            a = 0

         if (gcode_parser_module is not None):
            break

         print("[E] Could not find gcode_parser.")
         break

      gcode_parser_class = (
         getattr(
            gcode_parser_module,
            extract_class_name(parsed_arguments.gcode_parser[0])
         )
      )

      gcode_scripter.set_gcode_parser(gcode_parser_class())

   if (parsed_arguments.execute is not None):
      run_scripts(
         gcode_scripter,
         [
            script_name_to_script_class(script_name)
            for script_name in argument_to_script_list(parsed_arguments.execute)
         ]
      )

   if (parsed_arguments.output_file is not None):
      with open(parsed_arguments.output_file[0], 'w') as output_file:
         output_file.writelines(gcode_scripter.get_gcode())
