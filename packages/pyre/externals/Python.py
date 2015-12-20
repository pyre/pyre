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
    def generic(cls):
        """
        Provide a default implementation of python on platforms that are not handled explicitly
        """
        # grab the support for python 3.x
        from .Python3 import Python3
        # and return it
        return Python3


    @classmethod
    def macportsChooseImplementations(cls, macports):
        """
        Provide alternative compatible implementations of python on macports machines, starting
        with the package the user has selected as the default
        """
        # grab the support for python 3.x
        from .Python3 import Python3
        # form the python3 flavor
        flavor = Python3.flavor
        # this is a macports host; ask it for all the python3 package choices
        for package in macports.alternatives(group=flavor):
            # instantiate each one using the package name and hand it to the caller
            yield Python3(name=package)

        # if we get this far, try this
        yield cls.generic()

        # out of ideas
        return


    @classmethod
    def macportsConfigureImplementation(cls, macports, instance):
        """
        Configure a python package instance on a macports host
        """
        # get the package group
        group = instance.flavor
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
        # find my {interpreter}
        interpreter = os.path.join(prefix, smap['bin/{}'.format(group)])
        # extract my {bindir}
        bindir,_ = os.path.split(interpreter)

        # the header regex
        header = "(?P<incdir>.*)/Python.h$"
        # search for it in contents
        incdir = macports.incdir(regex=header, contents=contents)

        # my library regex
        libpython = '(?P<libdir>.*)/lib{}.+\.dylib$'.format(group)
        # find the folder
        libdir = macports.libdir(regex=libpython, contents=contents)

        # apply the configuration
        instance.version = version
        instance.prefix = prefix
        instance.bindir = bindir
        instance.incdir = incdir
        instance.libdir = libdir
        instance.interpreter = interpreter

        # all done
        return


# end of file
