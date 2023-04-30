# -*- Python -*-
# -*- coding: utf-8 -*-
#
# {project.authors}
# {project.affiliations}
# (c) {project.span} all rights reserved
#


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
    # support for workflows, products, and factories
    flow,
    # shells
    application, plexus,
    # miscellaneous
    primitives, tracking, units, weaver,
    )


# register the package with the framework
package = executive.registerPackage(name='{project.name}', file=__file__)
# save the geography
home, prefix, defaults = package.layout()


# publish the local modules
# the bindings
from .ext import lib{project.name}
# basic functionality
from . import meta

# user interfaces
from . import shells
from . import cli


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
