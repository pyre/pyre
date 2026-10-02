# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the base exception from the framework
from pyre.framework.exceptions import PyreError


# all local exceptions derive from this
class JournalError(PyreError):
    """
    Base class for all journal errors

    Useful when you are trying to catch all journal errors
    """


# the base of the exceptions that fatal channels raise
class EntryError(JournalError):
    """
    Base class for the exceptions raised by fatal channels; they carry the entry that the
    channel recorded, so that whoever catches them can examine it
    """

    # public data
    description = "{0.headline}"

    # metamethods
    def __init__(self, headline, channel, page=(), notes=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # the summary of the condition
        self.headline = headline
        # the name of the channel that raised me
        self.channel = channel
        # the content of the entry
        self.page = list(page)
        # and its metadata
        self.notes = dict(notes) if notes is not None else {}
        # all done
        return

    def __reduce__(self):
        """
        Support for pickling, so that processes can hand these exceptions to each other
        """
        # rebuild from the entry, and restore the rest of my state
        return (type(self), (self.headline, self.channel, self.page, self.notes), self.__dict__)


# raised by firewalls
class FirewallError(EntryError):
    """
    Exception raised when firewalls fire
    """


# raised by debug channels that are marked fatal
class DebugError(EntryError):
    """
    Exception raised when fatal debug channels fire
    """


# raised by error channels
class ApplicationError(EntryError):
    """
    Exception raised when an application error is encountered
    """


# raised while decoding a record that is not in its wire form
class RecordError(JournalError):
    """
    Exception raised when a journal record cannot be reconstructed from its wire form
    """

    # public data
    description = "malformed journal record: {0.reason}"

    # metamethods
    def __init__(self, reason, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the reason
        self.reason = reason
        # all done
        return


# end of file
