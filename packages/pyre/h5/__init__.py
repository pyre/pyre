# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved

# support
import journal

# we may not have h5 runtime support, so
try:
    # to pull in the subpackages
    from . import disktypes
    from . import memtypes
    from . import schema
    from . import api

    # shortcuts
    reader = api.reader

# if anything goes wrong
except AttributeError as error:
    # make a channel
    channel = journal.warning("pyre.h5")
    # report
    channel.line(str(error))
    channel.line("while importing 'pyre.h5'")
    # flush
    channel.log()


# end of file
