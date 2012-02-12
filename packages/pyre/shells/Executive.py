# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# external
import pyre # the framework
import journal # logging
# my interface
from .Shell import Shell as shell


# declaration
class Executive(pyre.component, implements=shell):
    """
    The base class for hosting strategies
    """


    # public data
    home = pyre.properties.str(default=None)
    home.doc = "the process home directory"


    @property
    def hostname(self):
        """
        Retrieve the name of the host on which this process is running
        """
        # use the hostname from {platform}
        import platform
        return platform.node()


    @property
    def platform(self):
        """
        Retrieve the type of host on which this process is running
        """
        # use the string from sys
        import sys
        return sys.platform


    # interface
    @pyre.export
    def launch(self, application, *args, **kwds):
        """
        Invoke the application behavior
        """
        # {Executive} is abstract
        raise NotImplementedError("class {.__name__} must implement 'launch'".format(type(self)))


    # debugging
    _info = journal.info('pyre.shells')
    _warning = journal.warning('pyre.shells')
    _error = journal.error('pyre.shells')
    _debug = journal.debug('pyre.shells')


# end of file 
