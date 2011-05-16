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

# access to the public names
# diagnostics
from .Debug import Debug as debug
from .Firewall import Firewall as firewall
from .Info import Info as info
from .Warning import Warning as warning
from .Error import Error as error
# exceptions
from .exceptions import FirewallError


def boot():
    # access to the local types
    from .Journal import Journal
    from .Channel import Channel

    # attempt to load the journal extension
    try:
        from . import journal
    # if it fails for any reason
    except Exception:
        # ignore it; the default implementation will kick in
        pass
    # otherwise
    else:
        # access the {Channel} class
        from .Channel import Channel
        # so we can hand it to the default proxy device
        journal.initialize(Channel)

        # install the index from the extension module that enables interaction with low level code
        # access the index that's tied to the C++ maps
        from . import proxies
        # install the C++ indices
        debug._index = proxies.debugIndex()
        firewall._index = proxies.firewallIndex()
        info._index = proxies.infoIndex()
        warning._index = proxies.warningIndex()
        error._index = proxies.errorIndex()

    # collect all channel categories in one place
    categories = [ debug, firewall, info, warning, error ]
    # instantiate the journal component
    executive = Journal(name="journal", categories=categories)
    # patch {Channel}
    Channel.journal = executive

    # all done
    return


# initialize the package
boot()


# end of file 
