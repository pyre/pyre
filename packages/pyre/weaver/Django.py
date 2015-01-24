# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# the framework
import pyre
# my protocol
from .Project import Project


# declaration
class Django(pyre.component, family='pyre.smith.projects.django', implements=Project):
    """
    Encapsulation of the project information
    """


    # user configurable state
    name = pyre.properties.str(default='project')
    name.doc = "the name of the project"

    authors = pyre.properties.str(default=None)
    authors.doc = "the list of project authors"

    affiliations = pyre.properties.str(default=None)
    affiliations.doc = "the author affiliations"

    span = pyre.properties.str(default=None)
    span.doc = "the project duration for the copyright message"

    template = pyre.properties.str(default='django')
    template.doc = "the project template"


# end of file
