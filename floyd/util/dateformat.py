"""
PHP date() style date formatting
See http://www.php.net/date for format strings

Usage:
>>> import datetime
>>> d = datetime.datetime.now()
>>> df = DateFormat(d)
>>> print df.format('jS F Y H:i')
7th October 2003 11:39
>>>
"""

import re
import time
import calendar
import time
from datetime import tzinfo, timedelta
from floyd.util.unicode import force_unicode, force_utf8
from floyd.util.dates import MONTHS, MONTHS_3, MONTHS_AP, WEEKDAYS, WEEKDAYS_ABBR
from floyd.util.translation import ugettext as _

re_formatchars = re.compile(r'(?<!\\)([aAbBcdDfFgGhHiIjlLmMnNOPrsStTUuwWyYzZ])')
re_escaped = re.compile(r'\\(.)')


try:
  from email.utils import formatdate
  def HTTPDate(timeval=None):
    return formatdate(timeval, usegmt=True)
except ImportError:
  from rfc822 import formatdate as HTTPDate

class LocalTimezone(tzinfo):
    "Proxy timezone information from time module."
    def __init__(self, dt):
        tzinfo.__init__(self)
        self._tzname = self.tzname(dt)

    def __repr__(self):
        return smart_str(self._tzname)

    def utcoffset(self, dt):
        if self._isdst(dt):
            return timedelta(seconds=-time.altzone)
        else:
            return timedelta(seconds=-time.timezone)

    def dst(self, dt):
        if self._isdst(dt):
            return timedelta(seconds=-time.altzone) - timedelta(seconds=-time.timezone)
        else:
            return timedelta(0)

    def tzname(self, dt):
        try:
            return force_unicode(time.tzname[self._isdst(dt)], 'utf-8')
        except UnicodeDecodeError:
            return None

    def _isdst(self, dt):
        tt = (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.weekday(), 0, -1)
        try:
            stamp = time.mktime(tt)
        except (OverflowError, ValueError):
            # 32 bit systems can't handle dates after Jan 2038, and certain
            # systems can't handle dates before ~1901-12-01:
            #
            # >>> time.mktime((1900, 1, 13, 0, 0, 0, 0, 0, 0))
            # OverflowError: mktime argument out of range
            # >>> time.mktime((1850, 1, 13, 0, 0, 0, 0, 0, 0))
            # ValueError: year out of range
            #
            # In this case, we fake the date, because we only care about the
            # DST flag.
            tt = (2037,) + tt[1:]
            stamp = time.mktime(tt)
        tt = time.localtime(stamp)
        return tt.tm_isdst > 0

class Formatter(object):
    def format(self, formatstr):
        pieces = []
        for i, piece in enumerate(re_formatchars.split(force_unicode(formatstr))):
            if i % 2:
                pieces.append(force_unicode(getattr(self, piece)()))
            elif piece:
                pieces.append(re_escaped.sub(r'\1', piece))
        return u''.join(pieces)

class TimeFormat(Formatter):
    def __init__(self, t):
        self.data = t

    def a(self):
        "'a.m.' or 'p.m.'"
        if self.data.hour > 11:
            return _('p.m.')
        return _('a.m.')

    def A(self):
        "'AM' or 'PM'"
        if self.data.hour > 11:
            return _('PM')
        return _('AM')

    def B(self):
        "Swatch Internet time"
        raise NotImplementedError

    def f(self):
        """
        Time, in 12-hour hours and minutes, with minutes left off if they're
        zero.
        Examples: '1', '1:30', '2:05', '2'
        Proprietary extension.
        """
        if self.data.minute == 0:
            return self.g()
        return u'%s:%s' % (self.g(), self.i())

    def g(self):
        "Hour, 12-hour format without leading zeros; i.e. '1' to '12'"
        if self.data.hour == 0:
            return 12
        if self.data.hour > 12:
            return self.data.hour - 12
        return self.data.hour

    def G(self):
        "Hour, 24-hour format without leading zeros; i.e. '0' to '23'"
        return self.data.hour

    def h(self):
        "Hour, 12-hour format; i.e. '01' to '12'"
        return u'%02d' % self.g()

    def H(self):
        "Hour, 24-hour format; i.e. '00' to '23'"
        return u'%02d' % self.G()

    def i(self):
        "Minutes; i.e. '00' to '59'"
        return u'%02d' % self.data.minute

    def P(self):
        """
        Time, in 12-hour hours, minutes and 'a.m.'/'p.m.', with minutes left off
        if they're zero and the strings 'midnight' and 'noon' if appropriate.
        Examples: '1 a.m.', '1:30 p.m.', 'midnight', 'noon', '12:30 p.m.'
        Proprietary extension.
        """
        if self.data.minute == 0 and self.data.hour == 0:
            return _('midnight')
        if self.data.minute == 0 and self.data.hour == 12:
            return _('noon')
        return u'%s %s' % (self.f(), self.a())

    def s(self):
        "Seconds; i.e. '00' to '59'"
        return u'%02d' % self.data.second

    def u(self):
        "Microseconds"
        return self.data.microsecond


class DateFormat(TimeFormat):
  """PHP style date formatter
  
  Format string:
  
    Day
    d   Day of the month, 2 digits with leading zeros (01 to 31)
    D   A textual representation of a day, three letters (Mon - Sun)
    j   Day of the month without leading zeros  (1 - 31)
    l   A full textual representation of the day of the week (Sunday - Saturday)
    N   ISO-8601 numeric representation of the day of the week (1 - 7)
    S   English ordinal suffix for the day of the month (st, nd, rd or th)
    w   Numeric representation of the day of the week (0 - 6)
    z   The day of the year (0 - 365)

    Week
    W   ISO-8601 week number of year, weeks starting on Monday

    Month
    F   A full textual representation of a month (January - December)
    m   Numeric representation of a month, zero pad (01 - 12)
    M   A short textual representation of a month, three letters (Jan - Dec)
    n   Numeric representation of a month, without leading zeros (1 - 12)
    t   Number of days in the given month (28 - 31)

    Year
    L   Whether it's a leap year (1 leap, 0 not)
    o   ISO-8601 year number for that ISO week (Y gives real year)
    Y   A full numeric representation of a year, 4 digits (1999)
    y   A two digit representation of a year (99)

    Time
    a   Lowercase Ante meridiem and Post meridiem (am, pm)
    A   Uppercase Ante meridiem and Post meridiem (AM, PM)
    B   Swatch Internet time (000 - 999)
    g   12-hour format of an hour without leading zeros (1 - 12)
    G   24-hour format of an hour without leading zeros (0 - 23)
    h   12-hour format of an hour with leading zeros (01 - 12)
    H   24-hour format of an hour with leading zeros (00 - 23)
    i   Minutes with leading zeros (00 - 59)
    s   Seconds, with leading zeros (00 - 59)
    u   Microseconds (000000 - 999999)

    Timezone
    e   Timezone identifier (UTC, GMT, Atlantic/Azores)
    I   Daylight savings (1 or 0)
    O   Difference to Greenwich time (GMT) in hours (+0200)
    P   Difference to Greenwich time (GMT) in hours formatted: (+02:00)
    T   Timezone abbreviation (EST, MDT, GMT)
    Z   Timezone offset in seconds. (-43200 through 50400)

    Full Date/Time
    c   ISO 8601 date (2004-02-12T15:19:21+00:00)
    r   RFC 2822 formatted date (Thu, 21 Dec 2000 16:01:07 +0200)
    U   Seconds since the Unix Epoch (timestamp)
  
  """
  year_days = [None, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]

  def __init__(self, dt):
    # Accepts either a datetime or date object.
    self.data = dt
    self.timezone = getattr(dt, 'tzinfo', None)
    if hasattr(self.data, 'hour') and not self.timezone:
      self.timezone = LocalTimezone(dt)

  def b(self):
    "Month, textual, 3 letters, lowercase; e.g. 'jan'"
    return MONTHS_3[self.data.month]

  def c(self):
    """
    ISO 8601 Format
    Example : '2008-01-02T10:30:00.000123'
    """
    return self.data.isoformat()

  def d(self):
    "Day of the month, 2 digits with leading zeros; i.e. '01' to '31'"
    return u'%02d' % self.data.day

  def D(self):
    "Day of the week, textual, 3 letters; e.g. 'Fri'"
    return WEEKDAYS_ABBR[self.data.weekday()]

  def F(self):
    "Month, textual, long; e.g. 'January'"
    return MONTHS[self.data.month]

  def I(self):
    "'1' if Daylight Savings Time, '0' otherwise."
    if self.timezone and self.timezone.dst(self.data):
      return u'1'
    else:
      return u'0'

  def j(self):
    "Day of the month without leading zeros; i.e. '1' to '31'"
    return self.data.day

  def l(self):
    "Day of the week, textual, long; e.g. 'Friday'"
    return WEEKDAYS[self.data.weekday()]

  def L(self):
    "Boolean for whether it is a leap year; i.e. True or False"
    return calendar.isleap(self.data.year)

  def m(self):
    "Month; i.e. '01' to '12'"
    return u'%02d' % self.data.month

  def M(self):
    "Month, textual, 3 letters; e.g. 'Jan'"
    return MONTHS_3[self.data.month].title()

  def n(self):
    "Month without leading zeros; i.e. '1' to '12'"
    return self.data.month

  def N(self):
    "Month abbreviation in Associated Press style. Proprietary extension."
    return MONTHS_AP[self.data.month]

  def O(self):
    "Difference to Greenwich time in hours; e.g. '+0200'"
    seconds = self.Z()
    return u"%+03d%02d" % (seconds // 3600, (seconds // 60) % 60)

  def r(self):
    "RFC 2822 formatted date; e.g. 'Thu, 21 Dec 2000 16:01:07 +0200'"
    return self.format('D, j M Y H:i:s O')

  def S(self):
    "English ordinal suffix for the day of the month, 2 characters; i.e. 'st', 'nd', 'rd' or 'th'"
    if self.data.day in (11, 12, 13): # Special case
      return u'th'
    last = self.data.day % 10
    if last == 1:
      return u'st'
    if last == 2:
      return u'nd'
    if last == 3:
      return u'rd'
    return u'th'

  def t(self):
    "Number of days in the given month; i.e. '28' to '31'"
    return u'%02d' % calendar.monthrange(self.data.year, self.data.month)[1]

  def T(self):
    "Time zone of this machine; e.g. 'EST' or 'MDT'"
    name = self.timezone and self.timezone.tzname(self.data) or None
    if name is None:
      name = self.format('O')
    return unicode(name)

  def U(self):
    "Seconds since the Unix epoch (January 1 1970 00:00:00 GMT)"
    if getattr(self.data, 'tzinfo', None):
      return int(calendar.timegm(self.data.utctimetuple()))
    else:
      return int(time.mktime(self.data.timetuple()))

  def w(self):
    "Day of the week, numeric, i.e. '0' (Sunday) to '6' (Saturday)"
    return (self.data.weekday() + 1) % 7

  def W(self):
    "ISO-8601 week number of year, weeks starting on Monday"
    # Algorithm from http://www.personal.ecu.edu/mccartyr/ISOwdALG.txt
    week_number = None
    jan1_weekday = self.data.replace(month=1, day=1).weekday() + 1
    weekday = self.data.weekday() + 1
    day_of_year = self.z()
    if day_of_year <= (8 - jan1_weekday) and jan1_weekday > 4:
      if jan1_weekday == 5 or (jan1_weekday == 6 and calendar.isleap(self.data.year-1)):
        week_number = 53
      else:
        week_number = 52
    else:
      if calendar.isleap(self.data.year):
        i = 366
      else:
        i = 365
      if (i - day_of_year) < (4 - weekday):
        week_number = 1
      else:
        j = day_of_year + (7 - weekday) + (jan1_weekday - 1)
        week_number = j // 7
        if jan1_weekday > 4:
          week_number -= 1
    return week_number

  def y(self):
    "Year, 2 digits; e.g. '99'"
    return unicode(self.data.year)[2:]

  def Y(self):
    "Year, 4 digits; e.g. '1999'"
    return self.data.year

  def z(self):
    "Day of the year; i.e. '0' to '365'"
    doy = self.year_days[self.data.month] + self.data.day
    if self.L() and self.data.month > 2:
      doy += 1
    return doy

  def Z(self):
    """
    Time zone offset in seconds (i.e. '-43200' to '43200'). The offset for
    timezones west of UTC is always negative, and for those east of UTC is
    always positive.
    """
    if not self.timezone:
      return 0
    offset = self.timezone.utcoffset(self.data)
    # Only days can be negative, so negative offsets have days=-1 and
    # seconds positive. Positive offsets have days=0
    return offset.days * 86400 + offset.seconds


  
def utc_mktime(utc_tuple):
  """Returns number of seconds elapsed since epoch
  Note that no timezone are taken into consideration.
  utc tuple must be: (year, month, day, hour, minute, second)
  """
  if len(utc_tuple) == 6:
      utc_tuple += (0, 0, 0)
  return time.mktime(utc_tuple) - time.mktime((1970, 1, 1, 0, 0, 0, 0, 0, 0))


def datetime_to_timestamp(dt):
  """Converts a datetime object to UTC timestamp"""
  return int(utc_mktime(dt.timetuple()))
