# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# support
import os
from .. import tracking
# superclass
from ..patterns.Named import Named


# class declaration
class Package(Named):
    """
    The resting place of information collected while loading packages
    """


    # public data
    # geography
    home = None # the path to the package importable (as given by its {__file__})
    prefix = None # the home of the package installation
    defaults = None # the location of the package configuration files
    # bookkeeping 
    sources = None
    protocols = None # the collection of encountered protocols
    components = None # the collection of encountered components
    

    # interface
    def register(self, executive, file):
        """
        Deduce the package geography based on the location of the importable and add the package
        configuration folder to the pyre configuration path
        """
        # compute {home}
        home = os.path.dirname(file)
        # the prefix is the root of the package installation; in {pyre} standard form, that's
        # two levels up from {home}
        prefix = os.path.abspath(os.path.join(home, os.path.pardir, os.path.pardir))
        # the location of the package configuration files
        defaults = os.path.abspath(os.path.join(prefix, self.DEFAULTS))

        # my system folder name
        system = '{.name}/system'.format(self)
        # get the fileserver
        fileserver = executive.fileserver
        # and the nameserver
        nameserver = executive.nameserver
        # turn the configuration path into a file node
        cfg = fileserver.local(root=defaults).discover()
        # and attach it under the package namespace
        fileserver[system] = cfg

        # build a uri for the package configuration files
        uri = executive.uri().coerce('vfs:/{}'.format(system))
        # get the configuration path
        cfgpath = nameserver['pyre.configpath']
        # add my uri to it
        cfgpath.append(uri)

        # attach
        self.home = home
        self.prefix = prefix
        self.defaults = defaults

        # all done
        return


    def configure(self, executive, locator=None):
        """
        Locate and ask the executive to load my configuration files
        """
        # my configuration priority
        priority = executive.priority.package
        # if I were not given a {locator}, make one
        locator = tracking.here(level=1) if locator is None else locator
        # get the executive to do the rest
        return executive.configure(stem=self.name, priority=priority, locator=locator)


    # meta-methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        # initialize my attributes
        self.sources = []
        self.protocols = set()
        self.components = set()
        # all done
        return


    def __str__(self):
        return 'package {.name!r}'.format(self)


    # implementation details
    DEFAULTS = 'defaults'


# end of file 
