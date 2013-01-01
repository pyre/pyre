# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
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
    from ..schema import uri
    from .Actor import Actor as actor
    from .Component import Component as component


    # framework data
    pyre_key = None


    # override this in your protocols to provide the default implementation
    @classmethod
    def pyre_default(cls):
        """
        The preferred implementation of this protocol, in case the user has not provided an
        alternative
        """
        # actual protocols should override
        return None


    # override this in your protocols to provide custom translations of symbols to component
    # specifications
    @classmethod
    def pyre_convert(cls, value):
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
        _, family = cls.pyre_executive.nameserver.lookup(cls.pyre_key)
        # and return the family name
        return family


    @classmethod
    def pyre_package(cls):
        """
        Deduce my package name
        """
        # get the name server
        ns = cls.pyre_executive.nameserver
        # if i don't have a key, i don't have a package
        if cls.pyre_key is None: return None
        # otherwise, ask the nameserver
        _, family = ns.lookup(cls.pyre_key)
        # split the family name apart; the package name is the zeroth entry
        pkgName = family.split(ns.separator)[0]
        # use it to look up the package
        return ns[pkgName]


    # support for framework requests
    @classmethod
    def pyre_find(cls, uri, symbol, searchpath=None):
        """
        Participate in the search for shelves consistent with {uri}
        """
        # get my family name
        family = cls.pyre_family()
        # access the executive
        executive = cls.pyre_executive
        # the nameserver
        nameserver = cls.pyre_nameserver
        # and the fileserver
        fileserver = cls.pyre_fileserver

        # deduce my context path
        contextpath = nameserver.split(family) if family else ['']
        # if not supplied, use the nameserver search path, which is already a list of uris
        searchpath = nameserver['pyre.configpath'] if searchpath is None else searchpath

        # the choices of leading segments
        roots = (p.address for p in reversed(searchpath))
        # sub-folders built out of progressively shorter leading portions of the family name
        folders = (
            fileserver.join(*contextpath[:marker])
            for marker in reversed(range(0, len(contextpath)+1)))

        # and the address specification from the {uri}, with and without the {symbol}
        address = [uri.address, fileserver.join(uri.address, '{}.py'.format(symbol))]
        # with all possible combinations of these three sequences
        for fragments in itertools.product(roots, folders, address):
            # assemble the path
            path = fileserver.join(*fragments)
            # build a better uri
            uri = cls.uri(scheme='vfs', address=path)
            # and yield it
            yield uri

        # out of ideas
        return
        

# end of file 
