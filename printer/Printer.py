class Printer:

   def reset (self):
      self.bed_temperature = 0
      self.hotend_temperature = 0
      self.active_tool = 0
      self.location_x = 0
      self.location_y = 0
      self.location_z = 0
      self.print_area_size_x = 0
      self.print_area_size_y = 0
      self.print_area_size_z = 0
      self.print_fan_speed = 0
      self.is_extruding = False
      self.is_using_relative_coordinates = False
      self.script_tags = dict()

   def __init__ (self):
      self.reset()

   def clone (self):
      result = GenericPrinter()

      result.bed_temperature = self.bed_temperature
      result.hotend_temperature = self.hotend_temperature
      result.active_tool = self.active_tool
      result.location_x = self.location_x
      result.location_y = self.location_y
      result.location_z = self.location_z
      result.print_area_size_x = self.print_area_size_x
      result.print_area_size_y = self.print_area_size_y
      result.print_area_size_z = self.print_area_size_z
      result.is_extruding = self.is_extruding
      result.is_using_relative_coordinates = self.is_using_relative_coordinates
      # deepcopy is not needed here.
      result.script_tags = self.script_tags.copy()

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
      self.is_using_relative_positioning = value

   def is_using_relative_positioning (self):
      return self.is_using_relative_positioning

   def set_location (self, location):
      (x, y, z) = location
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
         self.location_x,
         self.location_y,
         self.location_z
      )

   def add_script_tag (self, name, value = 1):
      self.script_tags[name] = value

   def remove_script_tag (self, name):
      del self.script_tags[name]

   def has_script_tag (self, name):
      return (name in self.script_tags)

   def get_script_tag (self, name):
      return self.script_tags[name]
