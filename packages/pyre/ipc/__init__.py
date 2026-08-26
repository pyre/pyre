# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved

# the marker of component factories
from .. import foundry


# channel access
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
def inet(spec=""):
    """
    Convert {spec} to a {pyre.schemata.inet} address
    """
    # access the type factories
    from .. import schemata

    # cast the value
    return schemata.inet.coerce(value=spec)


# my exceptions
from . import exceptions

# my protocols
from .Dispatcher import Dispatcher as dispatcher
from .Marshaler import Marshaler as marshaler
from .Transport import Transport as transport


# my component foundries
@foundry(implements=transport)
def pipe():
    """
    The transport that connects processes with pipes
    """
    # grab the component class record
    from .Pipes import Pipes as pipes

    # and return it
    return pipes


@foundry(implements=transport)
def socket():
    """
    The transport that connects processes with unix domain socket pairs, which can also carry
    open file descriptors between the two processes
    """
    # grab the component class record
    from .Sockets import Sockets as sockets

    # and return it
    return sockets


@foundry(implements=marshaler)
def pickler():
    """
    A marshaler that uses native python services to serialize objects
    """
    # grab the component class record
    from .Pickler import Pickler as pickler

    # and return it
    return pickler


@foundry
def scheduler():
    """
    A component that enables the construction of applications with event loops
    """
    # grab the component class record
    from .Scheduler import Scheduler as scheduler

    # and return it
    return scheduler


@foundry
def selector():
    """
    A scheduler that can listen to file objects
    """
    # grab the component class record
    from .Selector import Selector as selector

    # and return it
    return selector


@foundry
def psl():
    """
    An implementation of the dispatcher protocol based on the high level interface in the
    {selectors} module of the python standard library
    """
    # grab the class
    from .SelectorPSL import SelectorPSL as psl

    # and return it
    return psl


# my component factories; use to build an actual instance
def newPipe(**kwds):
    """
    The transport that connects processes with pipes
    """
    # grab the component class record
    from .Pipes import Pipes as pipes

    # and instantiate it
    return pipes(**kwds)


def newSocket(**kwds):
    """
    The transport that connects processes with unix domain socket pairs
    """
    # grab the component class record
    from .Sockets import Sockets as sockets

    # and instantiate it
    return sockets(**kwds)


def newPickler(**kwds):
    """
    A marshaler that uses native python services to serialize objects
    """
    # grab the component class record
    from .Pickler import Pickler as pickler

    # and return it
    return pickler(**kwds)


def newScheduler(**kwds):
    """
    A component that enables the construction of applications with event loops
    """
    # grab the component class record
    from .Scheduler import Scheduler as scheduler

    # and return it
    return scheduler(**kwds)


def newSelector(**kwds):
    """
    A scheduler that can listen to file objects
    """
    # grab the component class record
    from .Selector import Selector as selector

    # and return it
    return selector(**kwds)


def newPSL(**kwds):
    """
    A selector based on the high level interface in the python standard library
    """
    # grab the component class record
    from .SelectorPSL import SelectorPSL as psl

    # and return it
    return psl(**kwds)


# end of file
