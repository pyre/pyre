# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import os, sys
# access to the framework
import pyre
# superclass
from .Tool import Tool
from .Library import Library


# the cython package manager
class Cython(Tool, family='pyre.externals.cython'):
    """
    The package manager for the cython interpreter
    """

    # constants
    category = 'cython'

    # user configurable state
    compiler = pyre.properties.str()
    compiler.doc = 'the name of the compiler; may be the full path to the executable'


    # configuration verification
    @classmethod
    def checkConfiguration(cls, package):
        """
        Verify that package ins configured correctly
        """
        # check the location of the binaries
        yield from cls.checkBindir(package=package, filenames=[package.compiler])
        # all done
        return


    # support for specific package managers
    @classmethod
    def macportsChooseImplementations(cls, macports):
        """
        Provide alternative compatible implementations of cython on macports machines, starting
        with the package the user has selected as the default
        """
        # this is a macports host; ask it for all the cython3 package choices
        for alternative in macports.alternatives(group=cls.category):
            # convert the selection alias into the package name that provides it
            package = macports.getSelectionInfo(group=cls.category, alternative=alternative)
            # instantiate each one using the package name and hand it to the caller
            yield Default(name=package)

        # out of ideas
        return


    @classmethod
    def macportsConfigureImplementation(cls, macports, instance):
        """
        Configure a cython package instance on a macports host
        """
        # get the package group
        category = cls.category
        # attempt to identify the package name from the {instance}
        package = macports.identifyPackage(package=instance)
        # get and save the package contents
        contents = tuple(macports.contents(package=package))
        # and the version info
        version, variants = macports.info(package=package)

        # find my {compiler}
        compiler = category
        # extract my {bindir}
        bindir = macports.findfirst(target=compiler, contents=contents)

        # compute the prefix
        prefix, _ = os.path.split(bindir)

        # apply the configuration
        instance.version = version
        instance.prefix = prefix
        instance.bindir = bindir
        instance.compiler = os.path.join(bindir, compiler)

        # all done
        return


# superclass
from .ToolInstallation import ToolInstallation

# the cython package manager
class Default(
        ToolInstallation,
        family='pyre.externals.cython.default', implements=Cython):
    """
    The package manager for cython instances
    """

    # constants
    category = Cython.category

    # public state
    compiler = pyre.properties.str()
    compiler.doc = 'the name of the cython compiler'



# end of file
