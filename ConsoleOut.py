#!/bin/env python3
import sys
import os

################################################################################
#### LIBRARY ###################################################################
################################################################################
class ConsoleOut:
   log_file = None
   enable_debug_messages = False
   warnings = 0
   errors = 0
   progress_index = 0
   progress_max = 0

   def set_log_file (filename):
      if (ConsoleOut.log_file is not None):
         ConsoleOut.log_file.close()

      ConsoleOut.log_file = open(filename, 'w')

   def set_progress (index, max_val):
      ConsoleOut.progress_index = index
      ConsoleOut.progress_max = max_val

   def enable_debug_messages ():
      ConsoleOut.enable_debug_messages = True

   def close ():
      ConsoleOut.standard(
         "Completed with "
         + str(ConsoleOut.errors)
         + " error(s) and "
         + str(ConsoleOut.warnings)
         + " warning(s)."
      )

      if (ConsoleOut.log_file is not None):
         ConsoleOut.standard(
            "Logs available in "
            + str(os.path.realpath(ConsoleOut.log_file.name))
            + "."
         )
         ConsoleOut.log_file.close()

   def handle_message (tag, message, stdout):
      if (ConsoleOut.progress_max > 0):
         message = (
            tag
            + "[GCODE: "
            + str(ConsoleOut.progress_index)
            + "/"
            + str(ConsoleOut.progress_max)
            + "] "
            + message
         )
      else:
         message = tag + (" " if (len(tag) > 0) else "") + message

      if (ConsoleOut.log_file is not None):
         ConsoleOut.log_file.write(message)
         ConsoleOut.log_file.write("\n")

      print(message, file = stdout)

   def error (message):
      ConsoleOut.errors = ConsoleOut.errors + 1
      ConsoleOut.handle_message("[E]", message, sys.stderr)

   def warning (message):
      ConsoleOut.warnings = ConsoleOut.warnings + 1
      ConsoleOut.handle_message("[W]", message, sys.stderr)

   def fatal (message):
      ConsoleOut.handle_message("[F]", message, sys.stderr)
      ConsoleOut.close()
      os.exit(-1)

   def debug (message):
      if (ConsoleOut.enable_debug_messages):
         ConsoleOut.handle_message("[D]", message, sys.stdout)

   def standard (message):
      ConsoleOut.handle_message('', message, sys.stdout)

