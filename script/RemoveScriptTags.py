def RemoveScriptTags:

   def delete_script_tag_comments (gcode_parser):
      while True:
         if (gcode_parser.completed()):
            break

         gcode_line = gcode_parser.get_next_gcode_raw()

         if (gcode_line.startswith("; [SCRIPT TAG]")):
            gcode_parser.delete_next_gcode()
         else:
            break

   def __init__ (self, params):
      # Do Nothing

   def initial_state (self, gcode_parser, printer):
      delete_script_tag_comments(gcode_parser)

   def final_state (self, gcode_parser, printer):
      # Do Nothing

   def step (self, previous_printer, gcode_parser, new_printer):
      delete_script_tag_comments(gcode_parser)
