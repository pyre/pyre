# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# exceptions
from ..framework.exceptions import FrameworkError


# local anchor
class NexusError(FrameworkError):
    """
    Base exceptions for all error conditions detected by nexus components
    """


# a temporary error
class RecoverableError(NexusError):
    """
    A recoverable error has occurred
    """


# a task that took its crew member down with it
class Casualty(RecoverableError):
    """
    A crew member died while carrying a task

    A death without a report means the task itself may be the killer, e.g. a request that
    crashes native code; such a task must never be retried in the team's own process, whose
    survival is the whole point of farming work out to crews
    """


# connection reset by peer
class ConnectionResetError(NexusError):
    """
    The connection was closed by the peer
    """


# end of file
