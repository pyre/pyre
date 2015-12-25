# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# framework
import pyre


# the openmpi package manager
class Installation(pyre.component):
    """
    Base class for all package installations
    """

    # constants
    version = "unknown"

    # public state
    prefix = pyre.properties.str()
    prefix.doc = 'the package installation directory'


    # meta-methods
    def __init__(self, name, **kwds):
        # chain up
        super().__init__(name=name, **kwds)
        # if there were any configuration errors
        if self.pyre_configurationErrors:
            # get the package manager
            packager = self.pyre_externals
            # and ask to dispatch to the platform specific handler so we can attempt to repair
            packager.configure(packageInstance=self)
        # all done
        return


    # platform specific configuration strategies
    def macports(self, macports):
        """
        Attempt to repair the configuration of this instance assuming a macports host
        """
        # get my category manager
        category = self.pyre_implements
        # ask my protocol to configure me for a macports host
        category.macportsConfigureImplementation(macports=macports, instance=self)
        # check my configuration again
        errors = self.pyre_configured()
        # and if there are errors
        if errors:
            # complain
            raise self.ConfigurationError(component=self, errors=errors)
        # all done
        return


    def dpkg(self, dpkg):
        """
        Attempt to repair the configuration of this instance assuming a dpkg host
        """
        print("Installation.dpkg: {}".format(self))
        # ask my protocol to configure me for a dpkg host
        self.pyre_implements.dpkgConfigureImplementation(dpkg=dpkg, instance=self)
        # check my configuration again
        errors = self.pyre_configured()
        # and if there are errors
        if errors:
            # complain
            raise self.ConfigurationError(component=self, errors=errors)
        # all done
        return


    # framework hooks
    def pyre_configured(self):
        """
        Verify and correct the package configuration
        """
        # initialize the list of errors
        errors = super().pyre_configured()
        # check the configuration and record any reported errors
        errors += list(self.pyre_implements.checkConfiguration(package=self))
        # return the list of errors
        return errors


# end of file
