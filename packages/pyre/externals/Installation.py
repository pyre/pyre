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

    # meta-methods
    def __init__(self, name, **kwds):
        # chain up
        super().__init__(name=name, **kwds)
        # if there were any configuration errors
        if self.pyre_configurationErrors:
            # ask the host for a dispatch to the platform specific handler and attempt to repair
            self.pyre_host.identifyDistribution(package=self)
        # all done
        return


    # platform specific configuration strategies
    def macports(self, host):
        """
        Attempt to repair the configuration of this instance assuming a macports host
        """
        # ask my protocol to configure me for a macports host
        self.pyre_implements.macportsConfigureInstance(host=host, package=self)
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
