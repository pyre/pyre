# -*- coding: utf-8 -*-
#
# {project.authors}
# (c) {project.span} all rights reserved


# support
import {project.name}


# declaration
class Config({project.name}.shells.command, family="{project.name}.cli.config"):
    """
    Display configuration information about this package
    """


    # version info
    @{project.name}.export(tip="the version information")
    def version(self, **kwds):
        """
        Print the version of the {project.name} package
        """
        # print the version number
        print(f"{{{project.name}.meta.version}}")
        # all done
        return 0


    # configuration
    @{project.name}.export(tip="the top level installation directory")
    def prefix(self, **kwds):
        """
        Print the top level installation directory
        """
        # print the installation location
        print(f"{{{project.name}.prefix}}")
        # all done
        return 0


    @{project.name}.export(tip="the directory with the executable scripts")
    def path(self, **kwds):
        """
        Print the location of the executable scripts
        """
        # print the path to the bin directory
        print(f"{{{project.name}.prefix}}/bin")
        # all done
        return 0


    @{project.name}.export(tip="the directory with the python packages")
    def pythonpath(self, **kwds):
        """
        Print the directory with the python packages
        """
        # print the path to the python package
        print(f"{{{project.name}.home.parent}}")
        # all done
        return 0


    @{project.name}.export(tip="the location of the {{{project.name}}} headers")
    def incpath(self, **kwds):
        """
        Print the locations of the {{{project.name}}} headers
        """
        # print the path to the headers
        print(f"{{{project.name}.prefix}}/include")
        # all done
        return 0


    @{project.name}.export(tip="the location of the {{{project.name}}} libraries")
    def libpath(self, **kwds):
        """
        Print the locations of the {{{project.name}}} libraries
        """
        # print the path to the libraries
        print(f"{{{project.name}.prefix}}/lib")
        # all done
        return 0


# end of file
