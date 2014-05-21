# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# externals
import itertools
from .. import tracking
# metaclass
from .Role import Role
# superclass
from .Configurable import Configurable


# class declaration
class Protocol(Configurable, metaclass=Role, internal=True):
    """
    The base class for requirement specifications
    """


    # types
    from ..schemata import uri
    from .exceptions import ResolutionError
    from .Actor import Actor as actor
    from .Component import Component as component


    # framework data
    pyre_key = None


    # override this in your protocols to provide the default implementation
    @classmethod
    def pyre_default(cls, **kwds):
        """
        The preferred implementation of this protocol, in case the user has not provided an
        alternative
        """
        # actual protocols should override
        return None


    # override this in your protocols to provide custom translations of symbols to component
    # specifications
    @classmethod
    def pyre_convert(cls, value, **kwds):
        """
        Hook to enable protocols to translate the component specification in {value} into a
        canonical form
        """
        # by default, do nothing
        return value


    # introspection
    @classmethod
    def pyre_family(cls):
        """
        Look up my family name
        """
        # if i don't have a key, i don't have a family
        if cls.pyre_key is None: return None
        # otherwise, ask the nameserver
        return cls.pyre_nameserver.getName(cls.pyre_key)


    @classmethod
    def pyre_familyFragments(cls):
        """
        Look up my family name
        """
        # if i don't have a key, i don't have a family
        if cls.pyre_key is None: return ()
        # otherwise, ask the nameserver
        return cls.pyre_nameserver.getSplitName(cls.pyre_key)


    @classmethod
    def pyre_package(cls):
        """
        Deduce my package name
        """
        # get the name server
        ns = cls.pyre_executive.nameserver
        # if i don't have a key, i don't have a package
        if cls.pyre_key is None: return None
        # otherwise, ask the nameserver for the split family name
        family = ns.getSplitName(cls.pyre_key)
        # the package name is the zeroth entry
        pkgName = family[0]
        # use it to look up the package
        return ns[pkgName]


    # support for framework requests
    @classmethod
    def pyre_resolveSpecification(cls, spec, **kwds):
        """
        Attempt to resolve {spec} into a component that implements me; {spec} is
        assumed to be a string
        """
        # get the executive
        executive = cls.pyre_executive
        # and ask it to resolve {value} into component candidates; this will handle correctly
        # uris that resolve to a retrievable component, as well as uris that mention an
        # existing instance
        for candidate in executive.resolve(uri=spec, protocol=cls, **kwds):
            # if it is compatible with my protocol
            if candidate.pyre_isCompatible(cls):
                # we are done
                return candidate

        # if we get this far, i just couldn't pull it off
        raise cls.ResolutionError(protocol=cls, value=spec)


    @classmethod
    def pyre_formCandidates(cls, uri, symbol, searchpath=None, **kwds):
        """
        Participate in the search for shelves consistent with {uri}
        """
        print("Protocol.pyre_formCandidates:")
        print("    uri: {.uri!r}".format(uri))
        print("    symbol: {}".format(symbol))
        print("    searchpath: {}".format(searchpath))
        # print("    kwds: {}".format(kwds))
        # get my resolver
        resolver = cls.pyre_contextResolver()
        # if no {searchpath} is supplied, use my default
        prefices = cls.pyre_contextPath() if searchpath is None else searchpath
        # sub-folders to append
        folders = cls.pyre_contextFolders()
        # specification fragments
        specs = cls.pyre_contextSpec(uri)
        # and symbol containers
        containers = cls.pyre_symbolContainers(symbol)

        # form all possible combinations of these
        product = itertools.product(prefices, folders, specs, containers)

        # with all possible combinations of these three sequences
        for prefix, folder, spec, container in product:
            # print('{} : {!r} : {!r} : {!r}'.format(prefix, folder, spec, container))
            # assemble the address portion of the uri; we are only looking for files, so it's
            # ok to hardwire the extension
            path = resolver.join(prefix.address, folder, spec, container) + cls.EXTENSION
            print('trying {!r}'.format(path))
            # build a better uri
            uri = cls.uri.locator(scheme=prefix.scheme, address=path)
            # and yield it
            yield uri

        # out of ideas
        return


    @classmethod
    def pyre_contextResolver(cls):
        """
        Return the entity responsible for normalizing uris
        """
        # by default, it's my fileserver
        return cls.pyre_fileserver
        

    @classmethod
    def pyre_contextPath(cls):
        """
        Return an iterable over the starting points for hunting down component implementations
        """
        # easy enough
        return cls.pyre_nameserver.configpath


    @classmethod
    def pyre_contextFolders(cls):
        """
        Return an iterable over portions of my family name
        """
        # get my family name split into fragments; empty family names must be converted to a
        # sequence with an empty string, otherwise {itertools.product} does not work correctly
        path = cls.pyre_familyFragments()
        # check whether the path is empty
        if not path:
            # return a normalized sequence so that {itertools.product} works correctly
            yield ''
            # all done
            return

        # get my resolver
        resolver = cls.pyre_contextResolver()

        # build a progressively shorter sequence of portions of my family name
        for marker in reversed(range(0, len(path)+1)):
            # splice it together and return it
            yield resolver.join(*path[:marker])

        # all done
        return


    @classmethod
    def pyre_contextSpec(cls, uri):
        """
        Build path contributions from the specification supplied by the resolution client
        """
        # get the address in the uri
        address = uri.address
        # if the address is empty
        if not address:
            # return a normalized sequence so that {itertools.product} works properly
            yield ''
            # all done
            return

        # otherwise, return the address
        yield address
        # do not attempt to transform this in any other way; it is conceptually wrong to ignore
        # an explicit specification provided by the user....
        return


    @classmethod
    def pyre_symbolContainers(cls, symbol):
        """
        Build a sequence of symbol containers to try
        """
        # first, involve the {symbol} in the uri search
        yield symbol
        # if that didn't work, let's see whether the 'parent' is not a folder but a container
        yield ''
        # out of ideas
        return


    # constants
    EXTENSION = '.py'


# end of file 
