# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# framework
import pyre


# the base manager of specific package installations
class Installation(pyre.component):
    """
    Base class for all package installations
    """

    # constants
    version = "unknown"

    # public state
    prefix = pyre.properties.str()
    prefix.doc = 'the package installation directory'


    # platform specific configuration strategies: these are invoked by the specific package
    # managers; families that require package manager specific configuration can override. the
    # default implementation invokes a category method

    def macports(self, macports):
        """
        Attempt to repair the configuration of this instance assuming a macports host
        """
        # attempt to deduce the package name
        package = macports.identifyPackage(package=self)
        # get the version info
        self.version, _ = macports.info(package=package)
        # get the package contents
        contents = tuple(macports.contents(package=package))

        # all done
        return package, contents


    # framework hooks
    def pyre_configured(self):
        """
        Verify the package configuration
        """
        # chain up
        yield from super().pyre_configured()
        # if i don't have a good version
        if self.version == 'unknown':
            # complain
            yield 'unknown version'

        # check my prefix
        yield from self.verifyFolder(category='prefix', folder=self.prefix)

        # all done
        return


    def pyre_initialized(self):
        """
        Attempt to repair broken configurations
        """
        # grab my configuration errors
        if not self.pyre_configurationErrors:
            # if there weren't any, we are done
            return
        # otherwise, we have work to do; grab the package manager
        manager = self.pyre_externals
        # and attempt
        try:
            # get him to help me repair this configuration
            manager.configure(packageInstance=self)
        # if something went wrong
        except self.ConfigurationError as error:
            # report my errors
            yield from error.errors

        # all done
        return


    # configuration validation
    def verifyFolder(self, category, folder, filenames=()):
        """
        Verify that the folder exists and contains the given {filenames}
        """
        # check there is a value
        if not folder:
            # complain
            yield "no {!r} setting".format(category)
            # and stop
            return
        # check that it is a valid directory
        if not os.path.isdir(folder):
            # complain
            yield "{!r} is not a valid directory".format(folder)
            # and stop
            return
        # verify that the given list of filenames exist
        for filename in filenames:
            # form the path
            path = os.path.join(folder, filename)
            # expand
            candidates = glob.glob(path)
            # check
            if not candidates:
                # complain
                yield "couldn't locate {!r} in {}".format(filename, folder)
                # and stop
                return
        # all done
        return


# end of file
