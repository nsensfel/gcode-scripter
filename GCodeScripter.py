#!/bin/env python3
import importlib
import os
import inspect

from gcode_parser.GCodeParser import GCodeParser
from printer.Printer import Printer
from script.Script import Script

from ConsoleOut import ConsoleOut

################################################################################
#### LIBRARY ###################################################################
################################################################################

class GCodeScripter:
   GCODE_PARSER_CLASS_FOLDERS = ['', 'gcode_parser.']
   SCRIPT_CLASS_FOLDERS = ['', 'script.']
   PRINTER_CLASS_FOLDERS = ['', 'printer.']

   #### STATIC #################################################################
   def extract_class_name (name):
      name = name.replace(os.sep, ".")

      if (name.endswith(".py")):
         name = name[:-len(".py")]

      try:
         return name[(name.rindex(".") + 1):]
      except Exception:
         return name

   def load_class (name, folder_list, parent_class, silent_fail = False):
      failed_module_paths = []
      failed_classes = []

      result = None

      for folder in folder_list:
         try:
            imported_module = importlib.import_module(folder + name)
         except Exception as e:
            failed_module_paths.append(((folder + name), e))
            continue

         try:
            result = (
               getattr(
                  imported_module,
                  GCodeScripter.extract_class_name(name)
               )
            )
         except Exception as e:
            failed_classes.append(((folder + name), e))
            continue

         if (result is None):
            failed_classes.append(((folder + name), e))
         elif (not issubclass(result, parent_class)):
            failed_classes.append(
               (
                  (folder + name),
                  ("Not a subclass of " + str(parent_class))
               )
            )
         else:
            return result

      if (silent_fail):
         return None

      error = "Could not find class \"" + name + "\":"

      for failed_module_path in failed_module_paths:
         (path, err) = failed_module_path
         error += "\n- Could not load a module from \"" + path + "\": "
         error +=  str(err) + "."

      for failed_class in failed_classes:
         (path, err) = failed_class
         error += "\n- Could not load a class from \"" + path + "\": "
         error += str(err) + "."

      ConsoleOut.error(error)

      return None

   def load_script_classes (name):
      result = (
         GCodeScripter.load_class(
            name,
            GCodeScripter.SCRIPT_CLASS_FOLDERS,
            Script,
            silent_fail = True
         )
      )

      if (result is not None):
         return [result]

      for folder in GCodeScripter.SCRIPT_CLASS_FOLDERS:
         for option in [(folder + name), (folder + name + ".py")]:
            if (os.path.exists(option)):
               if (os.path.isfile(option)):
                  return [
                     GCodeScripter.load_class(
                        option,
                        GCodeScripter.SCRIPT_CLASS_FOLDERS,
                        Script
                     )
                  ]
               else:
                  candidates = [
                     option + os.sep + filename
                     for filename in os.listdir(option)
                  ]

                  candidates = (
                     filter(
                        lambda filename : (
                           filename.endswith(".py")
                           or not os.path.isfile(filename)
                        ),
                        candidates
                     )
                  )

                  candidates.sort()

                  return [
                     load_script_classes(candidate)
                     for candidate in candidates
                  ]

      result = (
         GCodeScripter.load_class(
            name,
            GCodeScripter.SCRIPT_CLASS_FOLDERS,
            Script,
            silent_fail = False
         )
      )

      return result

   #############################################################################
   def __init__ (self):
      self.gcode_parser = GCodeParser()
      self.printer = Printer()

   def set_gcode (self, gcode):
      self.gcode_parser.set_raw_gcode_lines(gcode)

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

   def execute (self, script):
      if (isinstance(script, list)):
         for element in script:
            self.execute(element)

         return

      elif (isinstance(script, str)):
         self.execute(GCodeScripter.load_script_classes(script))

         return

      elif (not inspect.isclass(script)):
         ConsoleOut.error(
            "Cannot execute \""
            + str(script)
            + "\". It is not a class."
         )
         return

      elif (not issubclass(script, Script)):
         ConsoleOut.error(
            "Cannot execute \""
            + str(script)
            + "\". It is not a subclass of Script."
         )
         return

      script = script()

      while True:
         ConsoleOut.set_progress(
            self.gcode_parser.get_index(),
            self.gcode_parser.get_gcode_length()
         )

         script.initial_state(self.gcode_parser, self.printer)

         while (not self.gcode_parser.completed()):
            ConsoleOut.set_progress(
               self.gcode_parser.get_index() + 1,
               self.gcode_parser.get_gcode_length()
            )

            if (script.uses_previous_printer()):
               previous_printer = self.printer.clone()
            else:
               previous_printer = None

            self.gcode_parser.step(self.printer)

            script.step(
               previous_printer,
               self.gcode_parser,
               self.printer.clone()
            )

         ConsoleOut.set_progress(
            self.gcode_parser.get_index(),
            self.gcode_parser.get_gcode_length()
         )
         script.final_state(self.gcode_parser, self.printer)
         self.reset()

         if (not script.is_requesting_rerun()):
            break

################################################################################
#### SCRIPT MODE ###############################################################
################################################################################
if __name__ == "__main__":
   import argparse


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

   if (parsed_arguments.output_file is not None):
      ConsoleOut.set_log_file(parsed_arguments.output_file[0] + ".log")

   if (parsed_arguments.virtual_printer is not None):
      printer_class = (
         GCodeScripter.load_class(
            parsed_arguments.virtual_printer[0],
            GCodeScripter.PRINTER_CLASS_FOLDERS,
            Printer
         )
      )

      gcode_scripter.set_printer(printer_class())

   if (parsed_arguments.gcode_parser is not None):
      gcode_parser_class = (
         GCodeScripter.load_class(
            parsed_arguments.gcode_parser[0],
            GCodeScripter.GCODE_PARSER_CLASS_FOLDERS,
            GCodeParser
         )
      )

      gcode_scripter.set_gcode_parser(gcode_parser_class())

   if (parsed_arguments.input_file is not None):
      with open(parsed_arguments.input_file[0]) as input_file:
         gcode_scripter.set_gcode(input_file.readlines())

   if (parsed_arguments.execute is not None):
      gcode_scripter.execute(parsed_arguments.execute)

   if (parsed_arguments.output_file is not None):
      with open(parsed_arguments.output_file[0], 'w') as output_file:
         output_file.writelines(gcode_scripter.get_gcode())

   ConsoleOut.close()
