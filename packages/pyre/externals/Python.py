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


# the python package manager
class Python(Tool, Library, family='pyre.externals.python'):
    """
    The package manager for the python interpreter
    """

    # constants
    category = 'python'

    # user configurable state
    interpreter = pyre.properties.str(default=sys.executable)
    interpreter.doc = 'the name of the interpreter; may be the full path to the executable'


    # configuration verification
    @classmethod
    def checkConfiguration(cls, package):
        """
        Verify that package ins configured correctly
        """
        # get the host
        host = cls.pyre_host
        # check the location of the binaries
        yield from cls.checkBindir(package=package, filenames=[package.interpreter])
        # check the location of the headers
        yield from cls.checkIncdir(package=package, filenames=["Python.h"])
        # all done
        return


    # support for specific package managers
    @classmethod
    def macportsChooseImplementations(cls, macports):
        """
        Provide alternative compatible implementations of python on macports machines, starting
        with the package the user has selected as the default
        """
        # on macports, {python3} and {python2} are separate package groups; try python3.x
        # installations followed by python 2.x
        versions = [ Python3, Python2 ]
        # go through my choices
        for version in versions:
            # ask macports for all available alternatives
            for package in macports.alternatives(group=version.flavor):
                # instantiate each one using the package name and hand it to the caller
                yield version(name=package)

        # out of ideas
        return


    @classmethod
    def macportsConfigureImplementation(cls, macports, instance):
        """
        Configure a python package instance on a macports host
        """
        # get my category
        category = cls.category
        # attempt to identify the package name from the {instance}
        package = macports.identifyPackage(package=instance)
        # get and save the package contents
        contents = tuple(macports.contents(package=package))
        # and the version info
        version, variants = macports.info(package=package)

        # look for the interpreter executable
        interpreter = instance.flavor
        # to identify the {bindir}
        bindir = macports.findfirst(target=interpreter, contents=contents)

        # look for the main header file
        header = 'Python.h'
        # to identify the {incdir}
        incdir = macports.findfirst(target=header, contents=contents)

        # look for my library
        libpython = cls.pyre_host.dynamicLibrary(category + instance.sigver(version))
        # to identify the {libdir}
        libdir = macports.findfirst(target=libpython, contents=contents)

        # compute the prefix
        prefix = os.path.commonpath([bindir, incdir, libdir])

        # apply the configuration
        instance.version = version
        instance.prefix = prefix
        instance.bindir = bindir
        instance.incdir = incdir
        instance.libdir = libdir
        instance.interpreter = os.path.join(bindir, interpreter)

        # all done
        return


# implementation superclasses
from .ToolInstallation import ToolInstallation
from .LibraryInstallation import LibraryInstallation

# the base class for python installations
class Default(
        ToolInstallation, LibraryInstallation,
        family='pyre.externals.python.default', implements=Python):
    """
    The base class for for python instances
    """

    # constants
    flavor = 'unknown'
    category = Python.category

    # public state
    interpreter = pyre.properties.str()
    interpreter.doc = 'the name of the python interpreter'

    # interface
    def sigver(self, version=None):
        """
        Extract the portion of a version number that is used to label my parts
        """
        # if the user didn't specify
        if version is None:
            # use mine
            version = self.version
        # split it into major, minor and the rest
        major, minor, *rest = version.split('.')
        # assemble the significant part
        return '{}.{}'.format(major, minor)


# the python 2.x package manager
class Python2(Default, family='pyre.externals.python.python2'):
    """
    The package manager for python 2.x instances
    """

    # constants
    flavor = Default.category + '2'


# the python 3.x package manager
class Python3(Default, family='pyre.externals.python.python3'):
    """
    The package manager for python 3.x instances
    """

    # constants
    flavor = Default.category + '3'


# end of file
