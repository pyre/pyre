# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#

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
    interpreter = pyre.properties.str()
    interpreter.doc = 'the full path to the interpreter'


    # support for specific package managers
    @classmethod
    def macportsChoices(cls, macports):
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
    flavor = Python.category
    category = Python.category

    # public state
    libraries = pyre.properties.strings()
    libraries.doc = 'the libraries to place on the link line'

    interpreter = pyre.properties.str()
    interpreter.doc = 'the full path to the python interpreter'


    # configuration

    # these methods are invoked after construction if the instance is determined to be in
    # invalid state that was not the user's fault. typically this means that the package
    # configuration is still in its default state. the dispatcher determines the correct
    # package manager and forwards to one of the handlers in this section

    def dpkg(self, dpkg):
        """
        Attempt to repair my configuration
        """
        # NYI
        raise NotImplementedError('NYI!')


    def macports(self, macports):
        """
        Attempt to repair my configuration
        """
        # ask macports for help; start by finding out which package is related to me
        package = macports.identify(installation=self)
        # get the version info
        self.version, _ = macports.info(package=package)
        # and the package contents
        contents = tuple(macports.contents(package=package))

        # the name of the interpreter
        self.interpreter = '{0.category}{0.sigver}'.format(self)
        # find it in order to identify my {bindir}
        self.bindir = macports.findfirst(target=self.interpreter, contents=contents)

        # in order to identify my {incdir}, search for the top-level header file
        header = 'Python.h'
        # find it
        self.incdir = macports.findfirst(target=header, contents=contents)

        # in order to identify my {libdir}, search for one of my libraries
        stem = '{0.category}{0.sigver}m'.format(self)
        # convert it into the actual file name
        libpython = self.pyre_host.dynamicLibrary(stem)
        # find it
        self.libdir = macports.findfirst(target=libpython, contents=contents)
        # set my library
        self.libraries = stem

        # now that we have everything, compute the prefix
        self.prefix = self.commonpath(folders=self.bindir+self.incdir+self.libdir)

        # all done
        return


# the python 2.x package manager
class Python2(Default, family='pyre.externals.python.python2'):
    """
    The package manager for python 2.x instances
    """

    # constants
    flavor = Default.flavor + '2'

    # public state
    defines = pyre.properties.strings(default="WITH_PYTHON2")
    defines.doc = "the compile time markers that indicate my presence"


# the python 3.x package manager
class Python3(Default, family='pyre.externals.python.python3'):
    """
    The package manager for python 3.x instances
    """

    # constants
    flavor = Default.flavor + '3'

    # public state
    defines = pyre.properties.strings(default="WITH_PYTHON3")
    defines.doc = "the compile time markers that indicate my presence"


# end of file
