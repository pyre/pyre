# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# administrative
def copyright():
    """
    Return the pyre journal copyright note
    """
    return _journal_copyright


def license():
    """
    Print the pyre journal license
    """
    print(_journal_license)
    return


def version():
    """
    Return the pyre journal version
    """
    return _journal_version


# license
_journal_version = (1, 0, 0)

_journal_copyright = "pyre journal: Copyright (c) 1998-2011 Michael A.G. Aïvázis"

_journal_license = """
    pyre journal 1.0
    Copyright (c) 1998-2011 Michael A.G. Aïvázis
    All Rights Reserved


    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions
    are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in
      the documentation and/or other materials provided with the
      distribution.

    * Neither the name pyre nor the names of its contributors may be
      used to endorse or promote products derived from this software
      without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
    FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
    COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
    BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
    LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
    ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.
    """

# various initialization routines
# channel configuration
def configureChannels(config, channels):
    """
    Extract and apply channel configuration information
    """
    # access the type converters
    import pyre.schema
    # and iterate over {channels}, updating their indices with the contents of the pyre
    # configuration store in {config}
    for channel in channels:
        # build the key prefix
        prefix = "journal\." + channel.severity
        # identify the relevant keys
        for name, node in config.select(pattern=prefix):
            # get the value
            value = node.value
            # if it's {None}, it probably came from the command line without an assignment
            if value is None: value = True
            # attempt to cast to a bool
            try:
                value = pyre.schema.bool.pyre_cast(value)
            # if this fails
            except pyre.schema.bool.CastingError:
                # ignore it and move on
                continue
            # extract the channel name
            channelname = '.'.join(name.split('.')[2:])
            # update the index
            channel(channelname).active = value



# diagnostics
from .Debug import Debug as debug
from .Firewall import Firewall as firewall


# collect them all in one place
channels = [
    debug, firewall
    ]

# boot strapping
# attempt to load the journal extension
try:
    from . import journal
# if it fails for any reason
except Exception:
    # install the pure python diagnostic index
    pass
# otherwise
else:
    # install the index from the extension module that enables interaction with low level code
    pass

# configure the journal channels
import pyre
configureChannels(config=pyre.executive.configurator, channels=channels)


# end of file 
