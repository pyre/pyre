# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


"""
merlin is a configuration management tool
"""


# import and publish pyre symbols
from pyre import (
    # protocols, components, traits, and their infrastructure
    schemata, constraints, properties, protocol, component, foundry,
    # decorators
    export, provides,
    # the manager of the pyre runtime
    executive,
    # shells
    application, plexus,
)

# register the package
package = executive.registerPackage(name='merlin', file=__file__)
# attach the geography
home, prefix, defaults = package.layout()


# publish the local modules
from . import meta
from . import exceptions
# user interfaces
from . import shells         # the supported application shells
from . import cli            # the command line interface


def main():
    """
    This is the main entry point in the package. It is invoked by the {merlin} script. Its job
    is to boot pyre, examine the command line to deduce which actor the user would like to
    invoke, instantiate it, and call its main entry point with the supplied command line
    arguments.

    There are other possible ways to invoke merlin. See the package documentation.
    """
    # let the plexus do its thing
    return merlin.run()


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
