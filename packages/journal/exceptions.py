# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class FirewallError(Exception):
    """
    Exception raised whenever a fatal firewall is encountered
    """


    def __init__(self, firewall):
        self.firewall = firewall
        return


    def __str__(self):
        return "firewall breached; aborting..."


# end of file 
