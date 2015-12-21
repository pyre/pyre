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
    def generic(cls):
        """
        Provide a default implementation of cython on platforms that are not handled explicitly
        """
        # return the support for cython
        return Default


    @classmethod
    def macportsChooseImplementations(cls, macports):
        """
        Provide alternative compatible implementations of cython on macports machines, starting
        with the package the user has selected as the default
        """
        # this is a macports host; ask it for all the cython3 package choices
        for package in macports.alternatives(group=cls.category):
            # instantiate each one using the package name and hand it to the caller
            yield Default(name=package)

        # if we get this far, try this
        yield cls.generic()

        # out of ideas
        return


    @classmethod
    def macportsConfigureImplementation(cls, macports, instance):
        """
        Configure a cython package instance on a macports host
        """
        # get the package group
        group = cls.category
        # ask the package manager for information about my category
        alternatives = macports.alternatives(group=group)
        # get my name
        name = instance.pyre_name
        # if my name is not one of the alternatives:
        if name not in alternatives:
            # go through what's there
            for alternative in alternatives:
                # and check whether any of them are implementations of my flavor
                if alternative.startswith(group):
                    # set the target package name to this alternative
                    name = alternative
                    # and bail out
                    break
            # if we run out of options
            else:
                # this must be a poorly user configured instance; complain
                raise cls.ConfigurationError(
                    component=instance, errors=instance.pyre_configurationErrors)

        # get the selection info
        packageName, contents, smap = macports.getSelectionInfo(group=group, alternative=name)
        # get the package info
        version, variants = macports.info(package=packageName)

        # ask macports for its installation location
        prefix = macports.prefix()
        # find my {compiler}
        compiler = os.path.join(prefix, smap['bin/{}'.format(group)])
        # extract my {bindir}
        bindir,_ = os.path.split(compiler)

        # apply the configuration
        instance.version = version
        instance.prefix = prefix
        instance.bindir = bindir
        instance.compiler = compiler

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
    compiler = pyre.properties.str(default=category)
    compiler.doc = 'the name of the cython compiler'



# end of file
