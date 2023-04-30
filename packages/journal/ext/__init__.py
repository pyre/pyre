# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# attempt to
try:
    # the journal bindings
    from . import journal as libjournal
# if something goes wrong
except ImportError:
    # mark; the rest of the package will adjust
    libjournal = None


# end of file
