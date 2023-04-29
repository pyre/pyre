# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# the base exception from the framework
from pyre.framework.exceptions import PyreError


# all local exceptions derive from this
class JournalError(PyreError):
    """
    Base class for all journal errors

    Useful when you are trying to catch all journal errors
    """


# raised by firewalls
class FirewallError(JournalError):
    """
    Exception raised when firewalls fire
    """

    # public data
    description = "firewall breached; aborting..."

    # metamethods
    def __init__(self, channel, **kwds):
        # chain up
        super().__init__(locator=channel.locator, **kwds)
        # save the channel
        self.firewall = channel
        # all done
        return


# raised by debug channels that are marked fatal
class DebugError(JournalError):
    """
    Exception raised when fatal debug channels fire
    """

    # public data
    description = "aborting..."

    # metamethods
    def __init__(self, channel, **kwds):
        # chain up
        super().__init__(locator=channel.locator, **kwds)
        # save the channel
        self.debug = channel
        # all done
        return


# raised by error channels
class ApplicationError(JournalError):
    """
    Exception raised when an application error is encountered
    """

    # public data
    description = "application error; aborting..."

    # metamethods
    def __init__(self, channel, **kwds):
        # chain up
        super().__init__(locator=channel.locator, **kwds)
        # save the channel
        self.error = channel
        # all done
        return


# end of file
