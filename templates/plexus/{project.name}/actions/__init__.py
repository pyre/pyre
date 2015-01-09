# -*- coding: utf-8 -*-
#
# {project.authors}
# {project.affiliations}
# (c) {project.span} all rights reserved
#


# pull in the command decorators
from .. import foundry, action

# help
@foundry(implements=action)
def info():
    from .Info import Info
    return Info


# end of file
