# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
This package contains the implementation of the readers and writers of the various
configuration file formats supported by pyre.

"""


# factories
def newCodecManager(**kwds):
    """
    Factory for the manager of installed codecs
    """
    from .CodecManager import CodecManager
    return CodecManager(**kwds)


def newCommandLineParser(**kwds):
    """
    Factory for the command line processor
    """
    from .CommandLine import CommandLine
    return CommandLine(**kwds)


def newConfigurator(**kwds):
    """
    Factory for the model that holds the frameowrk configuration state
    """
    from .Configurator import Configurator
    return Configurator(**kwds)


def newConfiguration(**kwds):
    """
    Factory for the temporary holding place for configuration information
    """
    from .Configuration import Configuration
    return Configuration(**kwds)


# end of file
