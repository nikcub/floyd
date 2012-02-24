
import os
import sys
import jinja2

from templating import jinja
from floyd.util.timesince import timesince

      # jinja.setup(self.config.paths.template_sets)
      # 
      # # setup variables
      # passed_vars = self.get_template_vars(passed_vars)
      # passed_vars = self.get_plugin_vars(passed_vars)
      # 
      # # Get template_set and template_theme
      # template_set = self.get_template_set()
      # template_theme = self.get_template_theme(template_set)
      # 
      # # logging.info('Rendering with: template_name: %s template_theme: %s template_set: %s and variables:' % (template_name, template_theme, template_set))
      # # logging.info(passed_vars)
      # 
      # content = jinja.render(template_name, passed_vars, template_theme=template_theme, template_set=template_set)

def render(template_name, template_path, template_variables, output_file):
  template = os.path.join(template_path, template_name)
  
  template_sets = [template_path]
  jinja.setup(template_sets)
  
  content = jinja.render(template_name, passed_vars, template_theme=template_theme, template_set=template_set)
  return content
  
  # env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
  # env.filters['timesince'] = timesince
  # env.filters['tformat'] = timeformat
  # jinja_template = env.get_template(template_name)
  # return jinja_template.render(template_vars)