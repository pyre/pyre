# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


# locators
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
    config = None # the location of the package configuration files
    # bookkeeping
    locator = None # my birthplace
    sources = None
    protocols = None # the collection of encountered protocols
    components = None # the collection of encountered components


    # interface
    def register(self, executive, file):
        """
        Deduce the package geography based on the location of the importable and add the package
        configuration folder to the pyre configuration path
        """
        # This should be done very carefully because multiple packages may share a common
        # installation folder. For example, this is true of the packages that ship with the
        # standard pyre distribution. The registration procedure takes care not to mount
        # redundant filesystems in the virtual namespace.

        # compute {home}; guaranteed to exist
        home = file.parent

        # the prefix is the root of the package installation; in {pyre} standard form, that's
        # two levels up from {home}: {prefix}/packages/{home}/{file}
        prefix = home.parent.parent
        # hopefully, it also exists
        if prefix.isDirectory():
            # in which case, here is the location of the package configuration files
            config = prefix / self.CONFIG / self.name
            # if this doesn't exist
            if not config.isDirectory():
                # we have no configuration folder
                config = None
        # if {prefix} does not exist
        else:
            # we have no prefix
            prefix = None
            # and no configuration folder
            config = None

        # show me
        # print('pyre.framework.Package.register: name={.name!r}'.format(self))
        # print('  home={!r}'.format(str(home)))
        # print('  prefix={!r}'.format(str(prefix)))
        # print('  config={!r}'.format(str(config)))

        # attach
        self.home = home
        self.prefix = prefix
        self.config = config

        # register with the fileserver
        executive.fileserver.registerPackage(package=self)

        # all done
        return


    def layout(self):
        """
        Easy access to the package folders
        """
        # form a triplet and return it
        return self.home, self.prefix, self.config


    def configure(self, executive):
        """
        Locate and ask the executive to load my configuration files
        """
        # load configurations with my name as the {namespace}
        return executive.configure(namespace=self.name, locator=self.locator)


    # meta-methods
    def __init__(self, locator, **kwds):
        # chain up
        super().__init__(**kwds)
        # remember the location of the package registration
        self.locator = locator
        # initialize my attributes
        self.sources = []
        self.protocols = set()
        self.components = set()
        # all done
        return


    def __str__(self):
        return 'package {.name!r}'.format(self)


    # implementation details
    CONFIG = 'share' # the path to the configuration folder relative to {prefix}


# end of file
