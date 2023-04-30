# -*- coding: utf-8 -*-
#
# {project.authors}
# (c) {project.span} all rights reserved


# pull the action protocol
from ..shells import action
# and the base panel
from ..shells import command
# pull in the command decorator
from .. import foundry


# application introspection
@foundry(implements=action, tip="information about this application")
def about():
    # get the action
    from .About import About
    # borrow its docstring
    __doc__ = About.__doc__
    # and publish it
    return About


@foundry(implements=action, tip="configuration information")
def config():
    # get the action
    from .Config import Config
    # borrow its docstring
    __doc__ = Config.__doc__
    # and publish it
    return Config


@foundry(implements=action, tip="helpful information")
def info():
    # get the action
    from .Info import Info
    # borrow its docstring
    __doc__ = Info.__doc__
    # and publish it
    return Info


# low level info useful while debugging
@foundry(implements=action, tip="debugging information")
def debug():
    # get the action
    from .Debug import Debug
    # borrow its docstring
    __doc__ = Debug.__doc__
    # and publish it
    return Debug

# command completion; no tip so it doesn't show up on the help panel
@foundry(implements=action)
def complete():
    # get the action
    from .Complete import Complete
    # and publish it
    return Complete


# end of file
