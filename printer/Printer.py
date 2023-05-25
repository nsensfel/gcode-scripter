from ConsoleOut import ConsoleOut

class TagCollection (dict):
   def handle_text_instruction (self, text):
      instruction = text.split(" ")

      if (len(instruction) < 2):
         ConsoleOut.error("Invalid TagCollection instruction \"" + text + "\".")
         return
      elif (instruction[1] == "set"):
         self[instruction[0]] = (
            instruction[2] if (len(instruction) == 3) else True
         )
         return
      elif (instruction[1] == "start_list"):
         self[instruction[0]] = (
            [instruction[2]] if (len(instruction) == 3) else []
         )
         return
      elif (instruction[1] == "unset"):
         del self[instruction[0]]
         return

      if (len(instruction) < 3):
         ConsoleOut.error(
            "Missing argument in TagCollection instruction \""
            + text
            + "\"."
         )
         return

      if (instruction[1] == "+="):
         self[instruction[0]] = int(self[instruction[0]]) + int(instruction[2])
      elif (instruction[1] == "-="):
         self[instruction[0]] = int(self[instruction[0]]) - int(instruction[2])
      elif (instruction[1] == "f+="):
         self[instruction[0]] = (
            float(self[instruction[0]])
            + float(instruction[2])
         )
      elif (instruction[1] == "f-="):
         self[instruction[0]] = (
            float(self[instruction[0]])
            - float(instruction[2])
         )
      elif (instruction[1] == "add"):
         self[instruction[0]].append(instruction[2])
      elif (instruction[1] == "remove"):
         self[instruction[0]].remove(instruction[2])
      elif (instruction[1] == "remove_all"):
         while (instruction[2] in self[instruction[0]]):
            self[instruction[0]].remove(instruction[2])
      else:
         ConsoleOut.error(
            "Unknown operation in TagCollection instruction \""
            + text
            + "\"."
         )
         return

   def deepcopy (self):
      result = TagCollection()

      for key in self:
         result[key] = (
            self[key].copy() if isinstance(self[key], list) else self[key]
         )

      return result

class Printer:
   def reset (self):
      self.bed_temperature = 0
      self.hotend_temperature = 0
      self.active_tool = 0
      self.location_x = 0
      self.location_y = 0
      self.location_z = 0
      self.print_area_size_x = 200
      self.print_area_size_y = 200
      self.print_area_size_z = 200
      self.print_fan_speed = 0
      self.is_extruding = False
      self.is_using_relative_positioning_val = False
      self.temporary_tags = TagCollection()

   def __init__ (self):
      self.permanent_tags = TagCollection()
      self.reset()

   def set_parameters (self, params):
      for param in params:
         if (param[0] == "MAX_X"):
            self.print_area_size_x = float(param[1])
         elif (param[0] == "MAX_Y"):
            self.print_area_size_y = float(param[1])
         elif (param[0] == "MAX_Z"):
            self.print_area_size_z = float(param[1])
         else:
            ConsoleOut.error(
               "Unknown Virtual Printer parameter \""
               + param[0]
               + "\"."
            )

   def clone (self):
      result = Printer()

      result.bed_temperature = self.bed_temperature
      result.hotend_temperature = self.hotend_temperature
      result.active_tool = self.active_tool
      result.location_x = self.location_x
      result.location_y = self.location_y
      result.location_z = self.location_z
      result.print_area_size_x = self.print_area_size_x
      result.print_area_size_y = self.print_area_size_y
      result.print_area_size_z = self.print_area_size_z
      result.print_fan_speed = self.print_fan_speed = 0
      result.is_extruding = self.is_extruding
      result.is_using_relative_positioning_val = self.is_using_relative_positioning_val
      result.temporary_tags = self.temporary_tags.deepcopy()
      result.permanent_tags = self.permanent_tags.deepcopy()

      return result

   def set_bed_temperature (self, value):
      self.bed_temperature = value

   def get_bed_temperature (self):
      return self.bed_temperature

   def set_hotend_temperature (self, value):
      self.hotend_temperature = value

   def get_hotend_temperature (self):
      return self.hotend_temperature

   def set_active_tool (self, value):
      self.active_tool = value

   def get_active_tool (self):
      return self.active_tool

   def get_location_x (self):
      return self.location_x

   def set_location_x (self, value):
      self.location_x = value

   def get_location_y (self):
      return self.location_y

   def set_location_y (self, value):
      self.location_y = value

   def get_location_z (self):
      return self.location_z

   def set_location_z (self, value):
      self.location_z = value

   def set_print_area_size_x (self, value):
      self.print_area_size_x = value

   def get_print_area_size_x (self):
      return self.print_area_size_x

   def set_print_area_size_y (self, value):
      self.print_area_size_y = value

   def get_print_area_size_y (self):
      return self.print_area_size_y

   def set_print_area_size_z (self, value):
      self.print_area_size_z = value

   def get_print_area_size_z (self):
      return self.print_area_size_z

   def set_print_fan_speed (self, value):
      self.print_fan_speed = value

   def get_print_fan_speed (self):
      return self.print_fan_speed

   def set_is_extruding (self, value):
      self.is_extruding = value

   def is_extruding (self):
      return self.is_extruding

   def set_is_using_relative_positioning (self, value):
      self.is_using_relative_positioning_val = value

   def is_using_relative_positioning (self):
      return self.is_using_relative_positioning_val

   def set_location (self, x, y, z):
      self.location_x = x
      self.location_y = y
      self.location_z = z

   def get_location (self):
      return (
         self.location_x,
         self.location_y,
         self.location_z
      )

   def set_print_area_size (self, size):
      (x, y, z) = size
      self.print_area_size_x = x
      self.print_area_size_y = y
      self.print_area_size_z = z

   def get_print_area_size (self):
      return (
         self.print_area_size_x,
         self.print_area_size_y,
         self.print_area_size_z
      )

   def get_permanent_tag (self, name):
      return self.permanent_tags[name]

   def has_permanent_tag (self, name):
      return (name in self.permanent_tags)

   def interpret_permanent_tag_instruction (self, instr):
      self.permanent_tags.handle_text_instruction(instr)

   def get_temporary_tag (self, name):
      return self.temporary_tags[name]

   def has_temporary_tag (self, name):
      return (name in self.temporary_tags)

   def interpret_temporary_tag_instruction (self, instr):
      self.temporary_tags.handle_text_instruction(instr)
