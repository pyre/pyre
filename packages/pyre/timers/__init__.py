# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


"""
This package provides the necessary infrastructure for timing applications.

The sequence

    import pyre
    t = pyre.timers.wall(name="test")
    t.start()
    .
    .
    .
    delta = t.stop()   # returns the interval since the last {start}
    elapsed = t.read() # for the raw total elapsed time
    elapsed = t.sec()  # for float seconds
    elapsed = t.ms()   # for float milliseconds
    elapsed = t.us()   # for float microseconds

produces a timer, and registers it under the name {test}. Timers must be started before any
readings can take place. Stopping a timer prevents it from accumulating time, while {t.read}
returns the total amount of time the timer has been active. Timers can be {reset} and
reused as many times as you like.

Another interesting feature is that registered timers are available from anywhere in an
application. You can register a timer in one place, access it and start it in another, and stop
it and take a reading in a third, all without needing to pass around the variable. The timer
registry grants access to the same timer when it is asked for a timer of a known name.

If the {libpyre} bindings are available, the same timers are accessible from low level code
"""


# prefer the c++ bindings
libpyre_without_timers = False

# get the {__main__} module
import __main__

# so we can check
try:
    # whether the user asked for the pure python implementation
    libpyre_without_timers = __main__.libpyre_without_timers
# if this fails
except AttributeError:
    # it's because the user hasn't expressed an opinion; check with pyre
    import pyre

    # whether the C++ bindings are available
    if pyre.libpyre is None:
        # if not, fall back to the pure python implementations
        libpyre_without_timers = True


# so...
if libpyre_without_timers:
    # publish the pure python implementation
    from .WallTimer import WallTimer as wall
    from .ProcessTimer import ProcessTimer as cpu
# otherwise
else:
    # publish the C++ implementation
    wall = pyre.libpyre.timers.WallTimer
    cpu = pyre.libpyre.timers.ProcessTimer


# end of file
