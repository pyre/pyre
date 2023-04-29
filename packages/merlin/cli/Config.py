# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin


# declaration
class Config(merlin.shells.command, family="merlin.cli.config"):
    """
    Display configuration information about this package
    """


    # version info
    @merlin.export(tip="the version information")
    def version(self, **kwds):
        """
        Print the version of the merlin package
        """
        # print the version number
        print(f"{merlin.meta.version}")
        # all done
        return 0


    # configuration
    @merlin.export(tip="the top level installation directory")
    def prefix(self, **kwds):
        """
        Print the top level installation directory
        """
        # print the installation location
        print(f"{merlin.prefix}")
        # all done
        return 0


    @merlin.export(tip="the directory with the executable scripts")
    def path(self, **kwds):
        """
        Print the location of the executable scripts
        """
        # print the path to the bin directory
        print(f"{merlin.prefix}/bin")
        # all done
        return 0


    @merlin.export(tip="the directory with the python packages")
    def pythonpath(self, **kwds):
        """
        Print the directory with the python packages
        """
        # print the path to the python package
        print(f"{merlin.home.parent}")
        # all done
        return 0


    @merlin.export(tip="the location of the {merlin} headers")
    def incpath(self, **kwds):
        """
        Print the locations of the {merlin} headers
        """
        # print the path to the headers
        print(f"{merlin.prefix}/include")
        # all done
        return 0


    @merlin.export(tip="the location of the {merlin} libraries")
    def libpath(self, **kwds):
        """
        Print the locations of the {merlin} libraries
        """
        # print the path to the libraries
        print(f"{merlin.prefix}/lib")
        # all done
        return 0


# end of file
