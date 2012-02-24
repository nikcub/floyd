
import time

from floyd.util.dateformat import DateFormat, TimeFormat, datetime_to_timestamp, utc_mktime
from floyd.util.timesince import timesince as ts, timeuntil as tu

__all__ = ['date_format', 'time_format', 'short_date', 'iso_date', 
           'rfc2822_date', 'datetimeformat', 'timesince', 'timeuntil', 'utc_timestamp', 'timestamp']

def date_format(value, format_string):
  "Helper function for PHP style date formatting"
  df = DateFormat(value)
  return df.format(format_string)

def time_format(value, format_string):
  "Helper function for PHP style time formatting"
  tf = TimeFormat(value)
  return tf.format(format_string)

def short_date(value):
  df = DateFormat(value)
  return df.format('jS M Y')

def iso_date(value):
  """
  @todo convert to python native
  """
  df = DateFormat(value)
  return df.format('c')

def rfc2822_date(value):
  """
  """
  return value.strftime("%a, %d %b %Y %H:%M:%S +0000")

def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
  "Helper function for native Python date formatting"
  return value.strftime(format)

def utc_timestamp(value):
  return datetime_to_timestamp(value)

def timestamp(value):
  return datetime_to_timestamp(value)

def timesince(value):
  return ts(value)

def timeuntil(value):
  return tu(value)

def timeuntil_two(value):
  return 
  


