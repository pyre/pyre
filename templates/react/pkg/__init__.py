# -*- coding: utf-8 -*-
#
# {project.authors}
# (c) {project.span} all rights reserved


# import and publish pyre symbols
from pyre import (
    # protocols, components, traits, and their infrastructure
    schemata, constraints, properties, protocol, component, foundry,
    # decorators
    export, provides,
    # the manager of the pyre runtime
    executive,
    # support for concurrency
    nexus,
    # shells
    application, plexus,
    # miscellaneous
    primitives, tracking, units, weaver
    )


# register the package with the framework
package = executive.registerPackage(name='{project.name}', file=__file__)
# save the geography
home, prefix, defaults = package.layout()


# publish the local modules
# basic functionality
from . import meta           # package meta-data
from . import exceptions     # the exception hierarchy
# user interfaces
from . import shells         # the supported application shells
from . import cli            # the command line interface
from . import ux             # support for the web client


# administrivia
def copyright():
    """
    Return the copyright note
    """
    # pull and print the meta-data
    return print(meta.header)


def license():
    """
    Print the license
    """
    # pull and print the meta-data
    return print(meta.license)


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
    return print(meta.acknowledgments)


def version():
    """
    Return the version
    """
    # pull and return the meta-data
    return meta.version


# end of file
