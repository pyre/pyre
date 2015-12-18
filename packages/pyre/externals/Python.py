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
    def generic(cls, host):
        """
        Provide a default implementation of python on platforms that are not handled explicitly
        """
        # grab the support for python 3.x
        from .Python3 import Python3
        # and return it
        return Python3


    @classmethod
    def macports(cls, host):
        """
        Identify the default implementation of python on macports machines
        """
        # grab the support for python 3.x
        from .Python3 import Python3
        # form the python3 flavor
        python3 = Python3.flavor
        # this is a macports host; ask it for the selected python3 package
        selection, alternatives = host.selected(python3)
        # if the selection is a python3 installation
        if selection.startswith(python3):
            # and return it
            return Python3

        # if we get this far, not much else to do
        return cls.generic(host=host)


    @classmethod
    def macportsConfigureInstance(cls, package, host):
        """
        Configure a python package instance on a macports host
        """
        # ask the package manager for its installation location
        prefix = host.prefix()
        # ask the package manager for information about my category
        selection, alternatives = host.selected(group=package.flavor)
        # get my name
        name = package.pyre_name
        # if my name is not one of the alternatives:
        if name not in alternatives:
            # go through what's there
            for alternative in alternatives:
                # and check whether any of them are implementations of my flavor
                if alternative.startswith(package.flavor):
                    # set the target package name to this alternative
                    name = alternative
                    # and bail out
                    break
            # if we run out of options
            else:
                # this must be a poorly user configured instance; complain
                raise cls.ConfigurationError(
                    component=package, errors=package.pyre_configurationErrors)

        # get my selection info
        packageName, contents, smap = host.provider(group=package.flavor, alternative=name)

        # find my {interpreter}
        interpreter = os.path.join(prefix, smap['bin/python3'])
        # extract my {bindir}
        bindir,_ = os.path.split(interpreter)

        # find my header
        header = "Python.h"
        # search for it in contents
        for path in contents:
            # split it
            folder, filename = os.path.split(path)
            # if the filename is a match
            if filename == header:
                # save the folder
                incdir = folder
                # and bail
                break
        # otherwise
        else:
            # leave it blank; we will complain below
            incdir = ''

        # find my library
        libpython = 'libpython'
        # search for it in contents
        for path in contents:
            # split it
            folder, filename = os.path.split(path)
            # if the filename is a match
            if filename.startswith(libpython):
                # save the folder
                libdir = folder
                # and bail
                break
        # otherwise
        else:
            # leave it blank; we will complain below
            libdir = ''

        # apply the configuration
        package.prefix = prefix
        package.bindir = bindir
        package.incdir = incdir
        package.libdir = libdir
        package.interpreter = interpreter

        # all done
        return


# end of file
