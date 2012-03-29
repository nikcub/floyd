
import os
import sys
import jinja2

from templating import jinja
from floyd.util.timesince import timesince

class BaseController(object):
  pass

def index():
  return floyd.render('index')


def TemplateVars(vars):
  additional = {
    'admin': False,
    'user': None,
    'logout': '/',
    'login': '/',
    'static_host': 'sketch-proto.appspot.com',
    'css_file': 'nikcub.030.min.css',
    'css_ver': '26',
    'src': 'database',
  }
  return dict(zip(additional.keys() + vars.keys(), additional.values() + vars.values()))

def RenderPosts(posts, outputdir):  
  for post in posts:
    print 'rendering -- %s' % post.stub
    template_vars = {}
    template_vars['posts'] = posts[:5]
    template_vars['post'] = post
    template_vars = TemplateVars(template_vars)
    
    render = floyd.templating.jinja.render('single', template_vars)
    post_output_path = os.path.join(outputdir, post.stub)
    print 'render: %s ' % post_output_path
    fp = open(post_output_path, 'w')
    fp.write(render)
    fp.close()

def post(post, route):
  print "Rendering %s at %s" % (post.title, route)

def page(post, route):
  print "Rendering %s at %s" % (post.title, route)

def index():
  print 'index'

def archive():
  print 'archive'

def feed():
  print 'feed'

def render(template_name, template_path, template_variables, output_file):
  template = os.path.join(template_path, template_name)
  
  template_sets = [template_path]
  jinja.setup(template_sets)
  
  content = jinja.render(template_name, passed_vars, template_theme=template_theme, template_set=template_set)
  return content
  
