"""Floyd
  
A command line static website generator for popular cloud hosting providers
  
This source file is subject to the new BSD license that is bundled with this 
package in the file LICENSE.txt. The license is also available online at the 
URL: <http://nikcub.appspot.com/bsd-license.txt>

:copyright: Copyright (C) 2012 Nik Cubrilovic and others, see AUTHORS
:license: new BSD, see LICENSE for more details.
"""

__version__ = '0.0.1'
__author__ = 'Nik Cubrilovic <nikcub@gmail.com>'

import argparse
import os
import sys

parser = argparse.ArgumentParser(description='Static website generator for cloud hosting platforms', epilog='Report any issues to [Github url]')
parser.add_argument('-s','--src', required=True, nargs=1, help='Project source ("src" by default)')
parser.add_argument('-d','--dir', required=False, nargs=1, help='The directory in which to create site (creates in "site" by default)')

def run():
  print 'Running Floyd'
  args = parser.parse_args()
  cur_dir = os.getcwd()
  try:
    print "Creating project from : %s in : %s" % (args.src[0], args.dir[0])
  except IOError as (errno, strerror):
    print strerror