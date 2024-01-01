# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# the framework
import pyre

# my superclass
from .ProjectTemplate import ProjectTemplate


# declaration
class Basic(ProjectTemplate, family="pyre.smith.projects.basic"):
    """
    Encapsulation of the project information
    """

    # additional user configurable state
    template = pyre.properties.str(default="basic")
    template.doc = "the project template"


# end of file
