#!/bin/env python3

###############################################################################
#### IMPORT ###################################################################
###############################################################################
import argparse

###############################################################################
#### PARAMETERS PARSING #######################################################
###############################################################################
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
   help='Scripts to execute. Will be processed in order.'
)
argument_parser.add_argument(
   '-ed',
   '--execute-directory',
   action='store',
   nargs=1,
   help='Execute scripts in directory, in alphabetical file name order.'
)

parsed_arguments = argument_parser.parse_args()
