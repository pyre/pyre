# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
# orthologue
# (c) 1998-2015 all rights reserved
#


# markup support
from .. import foundry
from . import Service as service


# the http service
@foundry(implements=service)
def http():
    # get the component
    from .http.Server import Server
    # and return it
    return Server


# end of file
