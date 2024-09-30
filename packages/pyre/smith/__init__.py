# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


"""
This package contains the machinery necessary to generate content in a variety of output formats.

The primary target is human readable formats, such source code for programming languages.
"""


# the marker of component factories
from .. import foundry


# the protocol that captures the project metadata
from .Project import Project as project


# the generator
def smith(**kwds):
    """
    The templater facility
    """
    # grab the protocol
    from .Smith import Smith

    # build a facility and return it
    return Smith(**kwds)


# bare bones app
@foundry(implements=project)
def basic():
    """
    A basic project
    """
    # grab the component class
    from .Basic import Basic as basic

    # and publish
    return basic


# bare bones command line interface
@foundry(implements=project)
def plexus():
    """
    The plexus project type
    """
    # grab the component class
    from .Plexus import Plexus as plexus

    # and publish
    return plexus


# {react} based ux
@foundry(implements=project)
def react():
    """
    The react project type
    """
    # grab the component class
    from .React import React as react

    # and publish
    return react


# end of file
