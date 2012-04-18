#!/usr/bin/env python
#
# Copyright (c) 2012, Nik Cubrilovic. All rights reserved.
#
# <nikcub@gmail.com> <http://nikcub.appspot.com>  
#
# Licensed under a BSD license. You may obtain a copy of the License at
#
#     http://nikcub.appspot.com/bsd-license
#
"""Floyd - multiopt.py

optparse extensions to support sub-commands and the 'help' command

@TODO move more functionality out of the holding class and into the custom
parent classes

"""

import sys
import optparse
from optparse import make_option

try:
    from gettext import gettext
except ImportError:
    def gettext(message):
        return message
_ = gettext

class CommandError(Exception): pass

class ArgumentError(Exception): pass

class OptionError(Exception): pass


class MultioptHelpFormatter(optparse.HelpFormatter):
  """
  Custom help formatter to include subcommands and other multiopt features
  """
  def __init__(self,
               indent_increment=2,
               max_help_position=24,
               width=None,
               short_first=1):
    optparse.HelpFormatter.__init__(self, indent_increment, max_help_position, width, short_first)
              
  def set_parser(self, parser):
    self.parser = parser
          
  def format_description(self, description):
    ret = ""
    if description:
      ret = self._format_text(description) + "\n"
    if hasattr(self.parser, 'command_help'):
      ret += "\n" + self.command_help_long() + "\n"
    return ret

  def format_usage(self, usage):
    return _("Usage: %s\n") % usage      

  def format_heading(self, heading):
    return "%*s%s:\n" % (self.current_indent, "", heading)

  def command_help_long(self):
    """
      Return command help for use in global parser usage string
      
      @TODO update to support self.current_indent from formatter
    """
    indent = " " * 2 # replace with current_indent
    help = "Command must be one of:\n"
    for action_name in self.parser.valid_commands:
      help += "%s%-10s %-70s\n" % (indent, action_name, self.parser.commands[action_name].desc_short.capitalize())
    help += '\nSee \'%s help COMMAND\' for help and information on a command' % self.parser.prog
    return help

  def command_help_short(self):
    """
      Return short single-line version of available commands
    """
    return ", ".join(self.parser.valid_commands)


class MultioptOptionParser(optparse.OptionParser):
  """
  An option parser that doesn't raise any errors on unknown options.
  """
  
  command_help = None
  
  def __init__(self,
                 usage=None,
                 option_list=None,
                 version=None,
                 description=None,
                 add_help_option=True,
                 prog=None,
                 epilog=None,
                 commands=[]):
      optparse.OptionParser.__init__(self, 
          usage=usage, 
          option_list=option_list, 
          version=version,
          description=description,
          add_help_option=add_help_option,
          prog=prog,
          epilog=epilog
        )
      self.formatter = MultioptHelpFormatter()
      self.formatter.set_parser(self)
      self.commands=commands
      self.valid_commands = sorted(self.commands.keys())

  def error(self, msg):
    pass

  # def print_help(self):
  #   """Output nothing.
  # 
  #   The lax options are included in the normal option parser, so under
  #   normal usage, we don't need to print the lax options.
  #   """
  #   optparse.OptionParser.print_help(self)

  def exit(self, status=0, msg=None):
    if msg:
      sys.stderr.write(msg)
    sys.exit(status)
        
  def print_version(self, file=None):
    optparse.OptionParser.print_version(self, file)
    self.exit(0)
    # @TODO why isn't it exiting?
    sys.exit(0)
  
  def print_help(self, file=None):
    optparse.OptionParser.print_help(self, file)
    print 'print help!'
    self.exit(1)
    sys.exit(0)
    
  def print_cmd_error(self, errstr=None):
    result = []
    formatter = self.formatter
    if self.usage:
      result.append(self.get_usage() + "\n")
    if errstr:
      result.append("Error: %s not a valid command. " % errstr)
    if len(self.commands) > 0 and hasattr(self.formatter, 'command_help_long'):
      # result.append(self.formatter.command_help_long() + "\n")
      result.append("Must be one of " + self.formatter.command_help_short() + ".\n")
      result.append("See `%s help` for more information." % self.prog)
    self._print_err(result)

  def print_exec_error(self, errcmd=None, errstr=None):
    result = []
    formatter = self.formatter
    if self.usage:
      result.append(self.get_usage() + "\n")
    if errstr:
      result.append("%s Error: %s\n" % (errcmd.capitalize(), errstr))
      result.append("See `%s help` for more information." % self.prog)
    self._print_err(result)
  
  def _print_err(self, errstr=""):
    if type(errstr) == type([]):
      errstr = "".join(errstr)
    print >> sys.stderr, errstr

  def print_lax_help(self):
    """Output the basic options available to every command.

    This just redirects to the default print_help() behavior.
    """
    optparse.OptionParser.print_help(self)

  def _process_args(self, largs, rargs, values):
    """
    override the behavior of the super class, which stop parsing
    at the first unrecognized option so we can extract command args
    """
    while rargs:
      arg = rargs[0]
      try:
        if arg[0:2] == "--" and len(arg) > 2:
          # process a single long option (possibly with value(s))
          # the superclass code pops the arg off rargs
          self._process_long_opt(rargs, values)
        elif arg[:1] == "-" and len(arg) > 1:
          # process a cluster of short options (possibly with
          # value(s) for the last one only)
          # the superclass code pops the arg off rargs
          self._process_short_opts(rargs, values)
        else:
          # it's either a non-default option or an arg
          # either way, add it to the args list so we can keep
          # dealing with options
          del rargs[0]
          raise Exception
      except:
        largs.append(arg)


class SubcommandParser(optparse.OptionParser):
  help_short = None
  help_long = None
  cmdname = None
  
  def __init__(self,
                 usage=None,
                 option_list=None,
                 version=None,
                 description=None,
                 add_help_option=True,
                 prog=None,
                 epilog=None,
                 help_short=None,
                 help_long=None,
                 cmdname=None):
      optparse.OptionParser.__init__(self, 
          usage=usage, 
          option_list=option_list, 
          version=version,
          description=help_short,
          add_help_option=add_help_option,
          prog=prog,
          epilog=epilog
        )
      self.help_long = help_long
      self.cmdname = cmdname
      self.formatter = MultioptHelpFormatter()
      self.formatter.set_parser(self)
        
  def print_exec_error(self, errcmd=None, errstr=None):
    result = []
    formatter = self.formatter
    if self.usage:
      result.append(self.get_usage() + "\n")
    if errstr:
      result.append("%s Error: %s\n" % (errcmd.capitalize(), errstr))
      result.append("See `%s help %s` for more information." % (self.prog, self.cmdname))
    self._print_err(result)

  def print_help_long(self):
    self._print(self.format_help_long())
    
  def format_help_long(self):
    formatter = self.formatter
    result = []
    if self.usage:
      result.append(self.get_usage() + "\n")
    if self.description:
      result.append(self.format_description(formatter) + "\n")
    if self.help_long:
      result.append(self.help_long + "\n\n")
    result.append(self.format_option_help(formatter))
    result.append(self.format_epilog(formatter))
    return "".join(result)
        
  def _print_err(self, errstr=""):
    if type(errstr) == type([]):
      errstr = "".join(errstr)
    print >> sys.stderr, errstr

  def _print(self, helpstr, file=None):
    """.
    """
    if file is None:
        file = sys.stdout
    encoding = self._get_encoding(file)
    file.write(helpstr.encode(encoding, "replace"))
        
class BaseCommand(object):
  """
  """
  option_set = []
  cmdname = None
  
  def __init__(self, header=None, footer=None, options=None, cmdname=None):
    self.header = header
    self.footer = footer
    self.option_set = options
    self.parser_class = SubcommandParser
    self.cmdname = cmdname
    # self.parser_class = MultioptOptionParser

  def set_cmdname(self, cmdname):
    self.cmdname = cmdname

  def get_parser(self, clsname, version, global_options):
    self._parser = self.parser_class(
      help_short=self.desc_short,
      help_long=self.desc_long,
      cmdname = self.cmdname,
      prog=clsname,
      version=version,
      usage=self.usage
    )
    for option in self.option_set + global_options:
      if isinstance(option, optparse.Option):
        self._parser.add_option(option)
      else:
        raise OptionError('invalid option')
    return self._parser


class SubCommand(BaseCommand):
  def __init__(self, func=None, usage=None, desc_short='', options=[], arguments=[], desc_long='', common=True, header=None, footer=None):
    self.func = func
    self.usage = usage or "%prog [options] <command>"
    self.desc_short = desc_short
    self.arguments = arguments
    self.desc_long = desc_long
    self.common = common    
    
    if not self.func:
      self.func = lambda *x : sys.stdout.write(" ".join(map(str,x)) + "\n")
    BaseCommand.__init__(self, header, footer, options)
  
  def __call__(self, func):
    meth = getattr(self, func)
    if meth:
      return meth()


class MultioptParser(object):
  """class to handle command line application
  
  Parses all command line options and commands and executes commands
  with passed options.
  """
  
  def __init__(self, command_set={}, argv=[], clsname='', version='', 
               desc_short="", global_options=[], add_help=False, 
               add_version=False, footer=None):
    """initialize a multioption parser
    
    command_set     dictionary of SubCommands
    argv            pass custom argv
    clsname         command name
    version         version string
    desc_short      short description of application
    global_options  options that can be passed on every command
    """
    self.command_set = command_set
    self.argv = argv or sys.argv[1:]
    self.clsname = clsname or self.argv[0]
    self.version = version
    self.desc_short = desc_short
    self.global_options = global_options
    if add_help:
      self._attach_help_command()
    if add_version:
      self._attach_version_command()
    self.footer=footer
    self.valid_commands = sorted(self.command_set.keys())

  def _attach_help_command(self):
    self.command_set['help'] = SubCommand(
      desc_short="Show help for subcommand",
      usage="%prog help <command>",
      
    )
  
  def _attach_version_command(self):
    self.command_set['version'] = SubCommand(
      desc_short="Show app version string",
      usage="%prog version",
      func=lambda *x: sys.stderr.write(self.version + '\n')
    )


  def autocomplete(self):
    """
    setup bash autocomplete
    
    @TODO
    """
    pass
    
  def run(self):
    """
      Run the multiopt parser
    """
    self.parser = MultioptOptionParser(
      usage="%prog <command> [options] [args]",
      prog=self.clsname,
      version=self.version,
      option_list=self.global_options,
      description=self.desc_short,
      commands=self.command_set,
      epilog=self.footer
    )
    
    try:
      self.options, self.args = self.parser.parse_args(self.argv)    
    except Exception, e:
      print str(e)
      pass

    if len(self.args) < 1:
      self.parser.print_lax_help()
      return 2
    
    self.command = self.args.pop(0)
    showHelp = False
    
    if self.command == 'help': 
      if len(self.args) < 1:
        self.parser.print_lax_help()
        return 2
      else:
        self.command = self.args.pop()
        showHelp = True

    if self.command not in self.valid_commands:
      self.parser.print_cmd_error(self.command)
      return 2

    self.command_set[self.command].set_cmdname(self.command)
    subcmd_parser = self.command_set[self.command].get_parser(self.clsname, self.version, self.global_options)
    subcmd_options, subcmd_args = subcmd_parser.parse_args(self.args)

    if showHelp:
      subcmd_parser.print_help_long()
      return 1

    try:
      self.command_set[self.command].func(subcmd_options, *subcmd_args)
    except (CommandError, TypeError), e:
      # self.parser.print_exec_error(self.command, str(e))
      subcmd_parser.print_exec_error(self.command, str(e))
      print 
      # @TODO show command help
      # self.parser.print_lax_help()
      return 2

      
    return 1
