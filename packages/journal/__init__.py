# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# publish the package metadata
from . import meta
# load the exception hierarchy
from . import exceptions

# set up a marker about whether we are going to load and publish the bindings
without_libjournal = False
# get the {__main__} module
import __main__
# check whether
try:
    # the user has expressed an opinion
    without_libjournal = __main__.journal_no_libjournal
# if not
except AttributeError:
    # no worries
    pass

# if we are allowed
if not without_libjournal:
    # load the bindings
    from .ext import libjournal
    # if something went wrong
    if libjournal is None:
        # indicate that we don't have access to the bindings
        without_libjournal = True

# if we don't have access to the bindings, rely on the pure python implementation
if without_libjournal:
    # publish the keeper of the global settings
    from .Chronicler import Chronicler
    # instantiate the singleton and publish the instance
    chronicler = Chronicler()

    # devices
    from .Trash import Trash as trash
    from .File import File as file
    from .Console import Console as cout
    from .ErrorConsole import ErrorConsole as cerr

    # channels
    # developer facing
    from .Debug import Debug as debug
    from .Firewall import Firewall as firewall
    # user facing
    from .Informational import Informational as info
    from .Warning import Warning as warning
    from .Error import Error as error
    from .Help import Help as help


    # convenience function to set the application name
    def application(name):
        """
        Set the application name
        """
        # record the name in the {chronicler} notes
        chronicler.notes["application"] = name
        # all done
        return

    # convenience function to suppress all output
    def quiet():
        """
        Suppress all output
        """
        # make a trash can
        trashcan = trash()
        # set it as the default device
        chronicler.device = trashcan
        # all done
        return

    # convenience function to send all output to a log file
    def logfile(path, mode="w"):
        """
        Send all output to a log file
        """
        # make a file
        logfile = file(path=path, mode=mode)
        # set it as the default device
        chronicler.device = logfile
        # all done
        return


    # convenience function to set the message decoration level
    def decor(level):
        """
        Set the message decoration level
        """
        # set {level} as the default
        chronicler.decor = level
        # all done
        return


    # convenience function to set the maximum message detail level
    def detail(level):
        """
        Set the maximum message detail level
        """
        # set {level} as the default
        chronicler.detail = level
        # all done
        return


# if we have access to the bindings
else:
    # let the c++ library take over
    # pull the convenience methods; their interface is the same as the pure python implementation
    quiet = libjournal.quiet
    logfile = libjournal.logfile
    application = libjournal.application
    decor = libjournal.decor
    detail = libjournal.detail

    # publish the keeper of the global state
    chronicler = libjournal.Chronicler

    # devices
    trash = libjournal.Trash
    cout = libjournal.Console
    cerr = libjournal.ErrorConsole

    # the developer facing channels
    debug = libjournal.Debug
    firewall = libjournal.Firewall
    # the user facing channels
    info = libjournal.Informational
    warning = libjournal.Warning
    error = libjournal.Error
    help = libjournal.Help


# administrative
def copyright():
    """
    Return the journal copyright note
    """
    return print(meta.header)


def license():
    """
    Print the journal license
    """
    # print it
    return print(meta.license)


def version():
    """
    Return the journal version
    """
    return meta.version


def credits():
    """
    Print the acknowledgments
    """
    # print it
    return print(meta.acknowledgments)


# end of file
