# -*- coding: utf-8 -*-
#
# {project.authors}
# (c) {project.span} all rights reserved


# the dispatcher
def dispatcher(**kwds):
    """
    The handler of {{uri}} requests
    """
    # get the dispatcher
    from .Dispatcher import Dispatcher
    # instantiate and return
    return Dispatcher(**kwds)


# the app engine
def panel(**kwds):
    """
    The application engine
    """
    # get the factory
    from .Panel import Panel
    # instantiate and return
    return Panel(**kwds)


# end of file
