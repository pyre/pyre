# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import re
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
    def dpkgAlternatives(cls, dpkg):
        """
        Go through the installed packages and identify those that are relevant for providing
        support for my installations
        """
        # get the index of installed packages
        installed = dpkg.installed()
        # look for python packages
        scanner = re.compile(r"^lib(?P<package>python(?P<major>[0-9])\.(?P<minor>[0-9]))-dev$")

        # go through the names of all installed packages
        for key in installed.keys():
            # looking for ones that match my patter
            match = scanner.match(key)
            # once we have a match
            if match:
                # get the package name
                package = match.group('package')
                # get the major and minor versions
                major = int(match.group('major'))
                minor = int(match.group('minor'))
                # form the installation name by removing the dots
                name = 'python{}{}'.format(major, minor)
                # hand back the pyre safe name and the name of the actual package
                yield name, package
        # all done
        return


    @classmethod
    def dpkgChoices(cls, dpkg):
        """
        Provide alternative compatible implementations of python on dpkg machines, starting
        with the package the user has selected as the default
        """
        # ask dpkg for the index of alternatives
        alternatives = dpkg.alternatives(group=cls)
        # now let's go through them
        for name in sorted(alternatives):
            # if this is a 3.x installation
            if name.startswith('python3'):
                # make a package and return it
                yield Python3(name=name)
            # if it's a 2.x installation
            elif name.startswith('python2'):
                # make a package and return it
                yield Python2(name=name)
            # otherwise
            else:
                # this is a bug
                import journal
                # so report it
                journal.firewall('pyre.externals.python').log(
                    "unknown python flavor for package {!r}".format(package))

        # out of ideas
        return


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
        # ask dpkg for help; start by finding out which package supports me
        base = dpkg.identify(installation=self)
        # the actual interpreter executable is in
        minimal = base + '-minimal'
        # the shared library is in
        libpython = 'lib' + base
        #
        # and the headers are in
        dev = libpython + '-dev'

        # ask for the index of installed packages
        installed = dpkg.installed()
        # put them all in a pile
        packages = [ base, minimal, libpython, dev ]
        # find the missing ones
        missing = [ pkg for pkg in packages if pkg not in installed ]
        # if there any missing ones
        if missing:
            # create a report
            msg = '{!r} is not fully installed; please install: {}'.format(
                base, ','.join(missing))
            # and complain
            raise self.ConfigurationError(configurable=self, errors=[msg])

        # get the version info
        self.version, _ = dpkg.info(package=base)

        # the name of the interpreter
        self.interpreter = '{0.category}{0.sigver}m'.format(self)
        # find it in order to identify my {bindir}
        bindir = dpkg.findfirst(target=self.interpreter, contents=dpkg.contents(package=minimal))
        # and save it
        self.bindir = [ bindir ] if bindir else []

        # in order to identify my {incdir}, search for the top-level header file
        header = 'Python.h'
        # find it
        incdir = dpkg.findfirst(target=header, contents=dpkg.contents(package=dev))
        # and save it
        self.incdir = [ incdir ] if incdir else []

        # in order to identify my {libdir}, search for one of my libraries
        stem = '{0.category}{0.sigver}m'.format(self)
        # convert it into the actual file name
        libpython = self.pyre_host.dynamicLibrary(stem)
        # find it
        libdir = dpkg.findfirst(target=libpython, contents=dpkg.contents(package=dev))
        # and save it
        self.libdir = [ libdir ] if libdir else []
        # set my library
        self.libraries = stem

        # now that we have everything, compute the prefix
        self.prefix = self.commonpath(folders=self.bindir+self.incdir+self.libdir)

        # all done
        return


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
        self.interpreter = '{0.category}{0.sigver}m'.format(self)
        # find it in order to identify my {bindir}
        bindir = macports.findfirst(target=self.interpreter, contents=contents)
        # and save it
        self.bindir = [ bindir ] if bindir else []

        # in order to identify my {incdir}, search for the top-level header file
        header = 'Python.h'
        # find it
        incdir = macports.findfirst(target=header, contents=contents)
        # and save it
        self.incdir = [ incdir ] if incdir else []

        # in order to identify my {libdir}, search for one of my libraries
        stem = '{0.category}{0.sigver}m'.format(self)
        # convert it into the actual file name
        libpython = self.pyre_host.dynamicLibrary(stem)
        # find it
        libdir = macports.findfirst(target=libpython, contents=contents)
        # and save it
        self.libdir = [ libdir ] if libdir else []
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
