"""
<Started>
  July 2013

<Author>
  Savvas Savvides <savvas@purdue.edu>

<Purpose>

"""

import Parser
import Syscall

DEBUG = False


class TrussParser(Parser.Parser):
  """
  <Purpose>

  <Attributes>
  """


  def __init__(self, trace_path):
    """
    <Purpose>

    <Arguments>
      trace_path:
        The path to the trace file containing the traced system calls. This file
        should contain the output of the truss utility.

    <Exceptions>
      IOError:
        If the pickle file containing the system call definitions is not found.
        (this file should come as part of this program)
    
    <Side Effects>
      None

    <Returns>
      None
    """

    super(TrussParser, self).__init__(trace_path)
  



  def _detect_trace_options(self):
    """
    <Purpose>


      Truss options (taken from truss man page):

      -a  Shows the argument strings that are passed in each exec() system call.
      
      -e  Shows the environment strings that are passed in each exec() system 
          call.
      
      -d  Includes a time stamp on each line of trace output (seconds.fraction)
          relative to the beginning of the trace. The first line of the trace
          output shows the base time from which the individual time stamps are
          measured, both as seconds since the epoch and as a date string.
      
      -D  Includes a time delta on each line, represents the elapsed time for
          the LWP that incurred the event since the last reported event incurred
          by that LWP. Specifically, for system calls, this is not the time
          spent within the system call.

      -E  Includes a time delta on each line of trace output. The value appears
          as a field containing seconds.fraction and represents the difference
          in time elapsed between the beginning and end of a system call. In
          contrast to the -D option, this is the amount of time spent within the
          system call.

      -f  Follows all children created by fork() or vfork().

      -l  Includes the id of the responsible lightweight process (LWP) with each
          line of trace output. If -f is also specified, both the process-id and
          the LWP-id are included.

      -o  File to be used for the trace output. By default, the output goes to 
          standard error.

      -r  Shows the full contents of the I/O buffer for each read() on any of
          the specified file descriptors. The output is formatted 32 bytes per
          line and shows each byte as an ASCII character (preceded by one blank)
          or as a 2-character C language escape sequence for control characters
          such as horizontal tab (\t) and newline (\n). If ASCII
          interpretation is not possible, the byte is shown in 2-character
          hexadecimal representation. (The first 12 bytes of the I/O buffer for
          each traced print >read() are shown even in the absence of -r.)
          Default is -r!all.


      -v  Verbose. Displays the contents of any structures passed by address to
          the specified system calls (if traced by -t). Input values as well as
          values returned by the operating system are shown. For any field used
          as both input and output, only the output value is shown. Default is
          -v!all.

      -w  Shows the contents of the I/O buffer for each write() on any of the
          specified file descriptors (see the -r option). Default is -w!all.

      Example truss output with different options:
      
      Unlike in StraceParser, here we don't have any required options. The
      reason is we don't need the pid  since since any resuming syscalls contain
      all parameter values including the ones already given in the corresponding
      unfinished syscall:

      - no options or with -o option. -o option does not cause any changes to 
      the output format:
        write(1, " - r w - r - - r - -    ".., 66)      = 66

      -f:
        1794:   write(1, " - r w - r - - r - -    ".., 66)      = 66

      -a:
        without:
          1815:   execve("/usr/bin/ls", 0x08047558, 0x08047568)  argc = 3
        with:
          1815:   execve("/usr/bin/ls", 0x08047558, 0x08047568)  argc = 3
          1815:    argv: ls -l -a

      -e:
        with:
          1820:   execve("/usr/bin/ls", 0x08047558, 0x08047568)  argc = 3
          1820:    envp: MANPATH=/usr/dt/man:/usr/man:/usr/openwin/share/man
          1820:     DTSOURCEPROFILE=true TERM=xterm SHELL=/sbin/sh
          1820:     SDT_NO_TOOLTALK=1 DESKTOP_STARTUP_ID=
          1820:     GTK_RC_FILES=/etc/gtk/gtkrc://.gtkrc-1.2-gnome2
          1820:     WINDOWID=39845935
          1820:     DTHELPSEARCHPATH=//.dt/help/root-unknown-0/%H://.dt/help/root-unknown-0/%H.sdl://.dt/help/root-unknown-0/%H.hv://.dt/help/%H://.dt/help/%H.sdl://.dt/help/%H.hv:/usr/dt/appconfig/help/%L/%H:/usr/dt/appconfig/help/%L/%H.sdl:/usr/dt/appconfig/help/%L/%H.hv:/usr/dt/appconfig/help/C/%H:/usr/dt/appconfig/help/C/%H.sdl:/usr/dt/appconfig/help/C/%H.hv
          1820:     USER=root DTDEVROOT= OPENWINHOME=/usr/openwin
          1820:     DTXSERVERLOCATION=local XMBINDDIR=/usr/dt/lib/bindings
          1820:     GNOME_KEYRING_SOCKET=/var/tmp/keyring-UkxoVa/socket
          1820:     SESSION_MANAGER=local/unknown:/tmp/.ICE-unix/979,inet6/unknown:32815,inet/unknown:32816
          1820:     SESSION_SVR=unknown
          1820:     HELPPATH=/usr/openwin/lib/locale:/usr/openwin/lib/help
          1820:     PATH=/usr/sbin:/usr/bin:/usr/openwin/bin:/usr/ucb:/opt/csw/bin
          1820:     MAIL=/var/mail/root PWD=/savvas/TRUSS_TRACES
          1820:     START_SPECKEYSD=no EDITOR=/usr/dt/bin/dtpad LANG=C
          1820:     DTAPPSEARCHPATH=//.dt/appmanager:/usr/dt/appconfig/appmanager/%L:/usr/dt/appconfig/appmanager/C
          1820:     TZ=US/Eastern SDT_NO_DTDBCACHE=1
          1820:     XFILESEARCHPATH=/usr/openwin/lib/locale/%L/%T/%N%S:/usr/openwin/lib/%T/%N%S
          1820:     SESSIONTYPE=altDt SHLVL=1 HOME=/
          1820:     DTSCREENSAVERLIST=StartDtscreenSwarm StartDtscreenQix     StartDtscreenFlame StartDtscreenHop StartDtscreenImage StartDtscreenLife     StartDtscreenRotor StartDtscreenPyro StartDtscreenWorm StartDtscreenBlank
          1820:     GNOME_DESKTOP_SESSION_ID=Default LOGNAME=root
          1820:     G_FILENAME_ENCODING=@locale,UTF-8
          1820:     AB_CARDCATALOG=/usr/dt/share/answerbooks/C/ab_cardcatalog
          1820:     DTDATABASESEARCHPATH=//.dt/types,/usr/dt/appconfig/types/%L,/usr/dt/appconfig/types/C
          1820:     XMICONSEARCHPATH=//.dt/icons/%B%M.pm://.dt/icons/%B%M.bm://.dt/icons/%B:/usr/dt/appconfig/icons/%L/%B%M.pm:/usr/dt/appconfig/icons/%L/%B%M.bm:/usr/dt/appconfig/icons/%L/%B:/usr/dt/appconfig/icons/C/%B%M.pm:/usr/dt/appconfig/icons/C/%B%M.bm:/usr/dt/appconfig/icons/C/%B
          1820:     DTUSERSESSION=root-unknown-0 DISPLAY=:0.0
          1820:     XMICONBMSEARCHPATH=//.dt/icons/%B%M.bm://.dt/icons/%B%M.pm://.dt/icons/%B:/usr/dt/appconfig/icons/%L/%B%M.bm:/usr/dt/appconfig/icons/%L/%B%M.pm:/usr/dt/appconfig/icons/%L/%B:/usr/dt/appconfig/icons/C/%B%M.bm:/usr/dt/appconfig/icons/C/%B%M.pm:/usr/dt/appconfig/icons/C/%B
          1820:     G_BROKEN_FILENAMES=yes dtstart_sessionlogfile=/dev/null
          1820:     COLORTERM=gnome-terminal _=/usr/bin/truss OLDPWD=/savvas

      -ae:
        execve("/usr/bin/ls", 0x08047558, 0x08047568)  argc = 3
        1823:    argv: ls -l -a
        1823:    envp: MANPATH=/usr/dt/man:/usr/man:/usr/openwin/share/man
        1823:     DTSOURCEPROFILE=true TERM=xterm SHELL=/sbin/sh
        1823:     SDT_NO_TOOLTALK=1 DESKTOP_STARTUP_ID=
        1823:     GTK_RC_FILES=/etc/gtk/gtkrc://.gtkrc-1.2-gnome2
        1823:     WINDOWID=39845935 ...some text omitted here...

      -d:
        1826:    0.1370 write(1, " - r w - r - - r - -    ".., 66)      = 66
        Note:
          When this option is used, the first line of the trace is something 
          like this:
          Base time stamp: 1379861388.5198 [ Sun Sep 22 10:49:48 EDT 2013 ]

      -D:
        1829:    0.0002 write(1, " - r w - r - - r - -    ".., 66)      = 66

      -E:
        1835:    0.0001 write(1, " - r w - r - - r - -    ".., 66)      = 66

      -dDE:
        1841:    0.2406  0.0008  0.0001 write(1, " - r w - r - - r - -    ".., 66)      = 66

      -l:
        1844/1:         write(1, " - r w - r - - r - -    ".., 66)      = 66

      -rall:
        without:
          1844:         read(3, "\0\0\00201\0\0\0 407\0\0".., 336)      = 336
        with:
          1853:   read(3, 0x08045FB0, 336)                        = 336
          1853:     \0\0\00201\0\0\0 =07\0\0 <07\0\0 <07\0\0 y05\0\0\0\0\0\0\0\0\0\0
          1853:     \0\0\0\0\0\0\0\0 P A xD3EC05\0\0DC03\0\0\0\0\0\003\0 `\0 '\01F\0
          1853:      w i > RE988AB )\0\0\0\0FA e8D01\0\0\0\0\0\0\0\0 l s\0\0\0\0\0\0
          1853:     \0\0\0\0\0\0\0\0 l s   - l   - a\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0
          1853:     \0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0
          1853:     \0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\003\0\0\0
          1853:      X u04\b h u04\b01\0\0\0 M\0\0\001\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0
          1853:      X\0\0\0\0\0\0\0\0\0\0\001\0\0\0A0 ; ;D8\0\0\0\0\006 O1403\0 (\0
          1853:      ;\0\0\0 '\0\0\0 w i > R\0\0\0\0\0\0\0\0FA e8D01 I A\0\0\0\0\0\0
          1853:     \0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0FFFFFFFFFFFFFFFF\0\0\0\0
          1853:     \0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0

      -vall:
        without:
          1859:   stat64("/lib/libsec.so.1", 0x080469F0)          = 0
        with:
          1856:   stat64("/lib/libsec.so.1", 0x080469F0)          = 0
          1856:       d=0x00780000 i=4956  m=0100755 l=1  u=0     g=2     sz=78872
          1856:           at = Sep 21 23:52:23 EDT 2013  [ 1379821943.750957000 ]
          1856:           mt = Jul  4 17:14:47 EDT 2011  [ 1309814087.000000000 ]
          1856:           ct = Jan 29 20:52:59 EST 2013  [ 1359510779.638008000 ]
          1856:       bsz=8192  blks=156   fs=ufs

      -wall:
        without:
          1862:   write(1, " - r w - r - - r - -    ".., 66)      = 66
        with:
          1865:   write(1, 0xD0F46BA4, 66)                        = 66
          1865:      - r w - r - - r - -       1   r o o t           r o o t
          1865:              6 4 3 1   A p r   2 5   2 3 : 1 3   w r i t e . t r u s
          1865:      s\n

    <Arguments>
      None

    <Exceptions>
      None
    
    <Side Effects>
      None

    <Returns>
      A dictionary with options and whether they were provided or not.
      
      Name of Option      Possible Values      Corresponding truss Option
      -------------------------------------------------------------------------
      "exec_argv"         True/False           -a
      "exec_env"          True/False           -e
      "output"            True/False           -o
      "fork"              True/False           -f
      "lwpid"             True/False           -l
      "verbose"           True/False           -vall
      "read"              True/False           -rall
      "write"             True/False           -wall
      "timestamp"         None/float           -d
      "lwp_elapsed_time"  True/False           -D
      "elapsed_time"      True/False           -E

      Here True means the option was given. False means the option was not 
      given and None means we don't know whether the option was given or not.

      if the -d option is not set then timestamp is set to None otherwise 
      timestamp is set to a float value with the format xxxxxxxxxx.xxxx which
      represents the seconds since epoch (seconds.fraction(4 digits))
    """

    trace_options = {}
    trace_options["exec_argv"] = False
    trace_options["exec_env"] = False
    trace_options["output"] = False
    trace_options["fork"] = False
    trace_options["lwpid"] = False
    trace_options["verbose"] = False
    trace_options["read"] = False
    trace_options["write"] = False
    trace_options["timestamp"] = None
    trace_options["lwp_elapsed_time"] = False
    trace_options["elapsed_time"] = False

    # read the first line of the trace to detect the used options. Traces that
    # represent application executions should start with a complete execve
    # system call. But to allow traces that are "made up" e.g for testing
    # purposes, let's not assume that the first syscall is always execve.
    try:
      fh = open(self.trace_path, "r")
      
      trace_line = None

      # we need a trace line that is complete ore resumed in order to examine
      # which options were used. Keep reading lines until a suitable trace line
      # is found.
      line = fh.readline()
      while line:
        line = line.strip()
        
        # empty lines don't normally appear in trace files but in case this is a
        # made up trace let deal with empty lines.
        if line == "":
          line = fh.readline()
          continue

        # unfinished syscall trace lines don't give us all the info we need to 
        # figure out which options are used.
        if "(sleeping...)" in line:
          line = fh.readline()
          continue

        # if the -d option is set then the first line of the trace will loook
        # something like this:
        # Base time stamp: 1379861388.5198 [ Sun Sep 22 10:49:48 EDT 2013 ]
        # Let's grab the epoch.
        if "Base time stamp:" in line:
          epoch_string = line[line.find("Base time stamp:"):line.find("[")]
          epoch_string = epoch_string.strip()
          trace_options["timestamp"] = float(epoch)

          # we still need a proper trace line to check for other options.
          line = fh.readline()
          continue
        
        # got our line!
        trace_line = line

        # if the trace_line we got is an exec syscall then let's examine the two
        # subsequent lines so that we can check whether the -a and -e options
        # were used.
        exec_lines = []
        if "exec" in trace_line:
          for _ in range(2):
            line = fh.readline()
            if "argv:" in line:
              trace_options["exec_argv"] = True
            if "envp:" in line:
              trace_options["exec_env"] = True

        break

    except IOError:
      raise IOError("Unable to read trace file when trying to determine the " + 
                    "trace options.")
    finally:
      fh.close()

    # if no suitable trace line is found to extract the options, then return
    # the initial values of trace_options which assumes that no options were
    # used with the utility.
    if trace_line == None:
      return trace_options

    # output: Assumed to be always True since it has no effect on the output
    # itself.
    trace_options["output"] = True

    # check if the general format of a trace line is correct.
    # example: open("/lib/libcurses.so.1", O_RDONLY)   = 3
    if (trace_line.find('(') == -1 or trace_line.find(')') == -1 
     or trace_line.find('=') == -1):
      raise Exception("Incorrect format of trace line `" + trace_line + "`")

    # content differences based on the truss options we care about appear before
    # the syscall name. This excludes the -a and -e options that apply only to 
    # exec syscalls.
    options_string = trace_line[:trace_line.find("(")]
    # break the string to individual options and remove the last part which
    # should be the name of the syscall.
    options = options_string.split()
    options = options[:-1]

    # Let's check for a pid
    if ":" in options[0]:
      option = options.pop(0)
      # if option starts with a digit then the pid is included hence -f was set
      if option[0].isdigit():
        trace_options["fork"] = True
      # if the option includes a "/" then the -l option is set.
      if "/" in option:
        trace_options["lwpid"] = True

    # check for -d -D -E


    return trace_options