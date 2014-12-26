# -*- coding: utf-8 -*-
#
# {project.authors}
# {project.affiliations}
# (c) {project.span} all rights reserved
#


# access the pyre framework
import pyre
# my protocol
from .. import components


# class declaration
class Command(pyre.panel, implements=components.action):
    """
    Base class for {{{project.name}}} commands
    """


# end of file
