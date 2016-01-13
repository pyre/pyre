# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# the framework
import pyre
# my superclass
from .ProjectTemplate import ProjectTemplate


# declaration
class Plexus(ProjectTemplate, family='pyre.weaver.projects.plexus'):
    """
    Encapsulation of the project information
    """


    # additional user configurable state
    template = pyre.properties.str(default='plexus')
    template.doc = "the project template"


# end of file
