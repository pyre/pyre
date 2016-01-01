# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
# orthologue
# (c) 1998-2016 all rights reserved
#


# channel access
def pipe(descriptors=None, **kwds):
    """
    If {descriptors} is not {None}, it is expected to be a pair ({infd}, {outfd}) of already
    open file descriptors; just wrap a channel around them. Otherwise, build a pair of pipes
    suitable for bidirectional communication between two processes on the same host

    """
    # access the channel
    from .Pipe import Pipe
    # if we were handed already open descriptors
    if descriptors:
        # unpack
        infd, outfd = descriptors
        # and go straight to the constructor
        return Pipe(infd=infd, outfd=outfd, **kwds)

    # build the pair and return it
    return Pipe.open(**kwds)


def tcp(address):
    """
    Builds a channel over a TCP connection to a server

    The parameter {address} is expected to be convertible to a {pyre.schemata.inet} compatible
    address.
    """
    # access the channel
    from .PortTCP import PortTCP
    # get it to build the channel
    return PortTCP.open(address=address)


def port(address=None):
    """
    Establishes a port at {address}
    """
    # access the channel
    from .PortTCP import PortTCP
    # get it installed at {address}
    return PortTCP.install(address=address)


# convenient access to the inet parser that builds addresses
def inet(spec=''):
    """
    Convert {spec} to a {pyre.schemata.inet} address
    """
    # access the type factories
    from .. import schemata
    # cast the value
    return schemata.inet.coerce(value=spec)


# my protocols
from .Dispatcher import Dispatcher as dispatcher
from .Marshaller import Marshaller as marshaller
# my components
from .Pickler import Pickler as pickler
from .Scheduler import Scheduler as scheduler
from .Selector import Selector as selector


# end of file
