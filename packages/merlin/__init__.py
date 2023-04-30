# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


"""
merlin is a configuration management tool
"""


# import and publish pyre symbols
from pyre import (
    # basic stuff
    patterns, primitives, tracking,
    # protocols, components, traits, and their infrastructure
    schemata, constraints, properties, protocol, component, foundry,
    # decorators
    export, provides,
    # the manager of the pyre runtime
    executive,
    # shells
    application, plexus,
    # content mills
    weaver,
    # flow
    flow,
)

# register the package
package = executive.registerPackage(name='merlin', file=__file__)
# attach the geography
home, prefix, defaults = package.layout()


# publish the local modules
from . import meta
from . import exceptions
# local extensions of the framework plumbing
from . import protocols
from . import components
# flow nodes
from . import assets
from . import factories
# builder abstractions
from . import languages
from . import compilers
# builders
from . import builders
# support for the user interfaces
from . import shells         # the supported application shells
from . import cli            # the command line interface


# administrative
def built():
    """
    Return the build timestamp
    """
    # pull and return the meta-data
    return meta.date


def credits():
    """
    Print the acknowledgments
    """
    # generate the message
    return print(meta.acknowledgments)


def copyright():
    """
    Return the merlin copyright note
    """
    # generate the message
    return print(meta.copyright)


def license():
    """
    Print the merlin license
    """
    # generate the message
    return print(meta.license)


def version():
    """
    Return the merlin version
    """
    # return the version
    return meta.version


# end of file
