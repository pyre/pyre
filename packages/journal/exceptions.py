# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# get the base pyre exception
from pyre.framework.exceptions import PyreError


# firewalls
class FirewallError(PyreError):
    """
    Exception raised whenever a fatal firewall is encountered
    """


    def __init__(self, firewall, **kwds):
        # build the info
        reason = "firewall breached; aborting..."
        locator = firewall.locator
        # chain up
        super().__init__(description=reason, locator=locator, **kwds)
        # record the error
        self.firewall = firewall
        # all done
        return


# application errors
class ApplicationError(PyreError):
    """
    Exception raised whenever an application error is encountered
    """


    def __init__(self, error, **kwds):
        # build the info
        reason = "firewall breached; aborting..."
        locator = error.locator
        # chain up
        super().__init__(description=reason, locator=locator, **kwds)
        # record the error
        self.error = error
        # all done
        return


# end of file
