# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


def timer(name):
    """
    Access the named timer.

    If a timer by this name has been created previously, {timer} will return a reference to
    that instance. If not, a new timer will be created and registered under the given name.
    """
    # ask the registrar for the named timer
    return registrar.timer(name)


# end of file 
