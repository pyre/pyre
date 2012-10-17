# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import sys
from ... import tracking
# superclass
from ..Loader import Loader


# declaration
class Importer(Loader):
    """
    This component codec recognizes uris of the form

        import:package.subpackage.factory#name

    The uri is interpreted as if

        from package.subpackage import factory
        factory(name=name)
    
    had been issued to the interpreter. {factory} is expected to be either a component class or
    a function that returns a component class. This class is then instantiated using {name} as
    the sole argument to the constructor. If {name} is not present, the component class is
    returned.
    """

 
    # types
    from .Shelf import Shelf as shelf


    # public data
    scheme = 'import'
    separator = '.' # same as python...


    # interface
    @classmethod
    def load(cls, uri, **kwds):
        """
        Interpret {uri} as a module to be loaded
        """
        # get the module name
        source = uri.address
        # build a simple locator
        locator = tracking.simple(source=str(uri))
        # attempt to 
        try:
            # import the module
            module = __import__(source)
        # the address portion of {uri} is not importable
        except ImportError as error:
            # complain
            raise cls.LoadingError(
                codec=cls, uri=uri, locator=locator, description=str(error)) from error
        # all other exceptions are probably caused by the contents of the module; let them
        # propagate to the user; on success, look up {module} in the global list of modules and
        # return it dressed up as a shelf
        return cls.shelf(module=sys.modules[source], uri=uri, locator=locator)


    # framework support
    @classmethod
    def register(cls, index):
        """
        Register the recognized schemes with {index}
        """
        # register my scheme
        index[cls.scheme] = cls
        # all done
        return


    @classmethod
    def locateShelves(cls, uri, **kwds):
        """
        Locate candidate shelves for the given {uri}
        """
        # try it first
        yield uri
        # get the address part of the uri; it serves as the package specification
        package = uri.address
        # while there is still something left
        while True:
            # attempt to
            try:
                # split it on the rightmost separator
                package, _ = package.rsplit(cls.separator, 1)
            # if it can't be done
            except ValueError:
                # we have exhausted the separators present in {address}
                break
            # set the address portion of the {uri} to the new package
            uri.address = package
            # and send it to the caller
            yield uri
        # no more
        return
            

# end of file 
