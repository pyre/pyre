# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import os
# access to the framework
import pyre
# superclass
from .Library import Library


# the vtk package manager
class VTK(Library, family='pyre.externals.vtk'):
    """
    The package manager for VTK packages
    """

    # constants
    category = 'vtk'


    # support for specific package managers
    @classmethod
    def macportsChoices(cls, macports):
        """
        Identify the default implementation of VTK on macports machines
        """
        # there is only one variation of this
        yield Default(name=cls.category)
        # and nothing else
        return


# superclass
from .LibraryInstallation import LibraryInstallation
# the implementation
class Default(LibraryInstallation, family='pyre.externals.vtk.default', implements=VTK):
    """
    A generic VTK installation
    """

    # constants
    category = VTK.category


    # configuration
    def dpkg(self, dpkg):
        """
        Attempt to repair my configuration
        """
        # NYI
        raise NotImplementedError('NYI!')


    def macports(self, macports, **kwds):
        """
        Attempt to repair my configuration
        """
        # chain up
        package, contents = super().macports(macports=macports, package=self.category, **kwds)
        # compute the prefix
        self.prefix = macports.prefix()
        # all done
        return package, contents


    # interface
    @pyre.export
    def defines(self):
        """
        Generate a sequence of compile time macros that identify my presence
        """
        # just one
        yield "WITH_" + self.category.upper() + self.major()
        # all done
        return


    # interface
    @pyre.export
    def headers(self, **kwds):
        """
        Generate a sequence of required header files
        """
        # my main header
        yield 'vtkVersion.h'
        # all done
        return


    @pyre.export
    def libraries(self, **kwds):
        """
        Generate a sequence of required libraries
        """
        # my implementations
        yield 'vtkCommonCore-{}'.format(self.sigver())
        # all done
        return


    # interface
    def major(self):
        """
        Extract the portion of a version number that is used to label my parts
        """
        # split it into major, minor and the rest
        major, *rest = self.version.split('.')
        # assemble the significant part
        return major


    def sigver(self):
        """
        Extract the portion of a version number that is used to label my parts
        """
        # split it into major, minor and the rest
        major, minor, *rest = self.version.split('.')
        # assemble the significant part
        return '{}.{}'.format(major, minor)


# end of file
