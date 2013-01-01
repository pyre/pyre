# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


class FirewallError(Exception):
    """
    Exception raised whenever a fatal firewall is encountered
    """


    def __init__(self, firewall, **kwds):
        super().__init__(**kwds)
        self.firewall = firewall
        return


    def __str__(self):
        return "firewall breached; aborting..."


class ApplicationError(Exception):
    """
    Exception raised whenever an application error is encountered
    """


    def __init__(self, error, **kwds):
        super().__init__(**kwds)
        self.error = error
        return


    def __str__(self):
        return "the application encountered a non-recoverable error; aborting..."


# end of file 
