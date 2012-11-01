# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
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
    def pyre_resolve(cls, value, locator):
        """
        Resolve {value} into a component that is compatible with me
        """
        # for recognizing components and their class records
        component, actor = cls.component, cls.actor

        # otherwise, convert it to a uri
        uri = cls.uri.coerce(value)
        # if there is a fragment, extract it to use as the instance name
        instanceName = uri.fragment

        # for each potential resolution by the executive
        for candidate in self.pyre_executive.retrieveComponentDescriptor(uri=uri, protocol=cls):
            # if it's neither a component class nor a component record
            if not (isinstance(candidate, actor) or isinstance(candidate, component)):
                # it must be a callable that returns one
                try:
                    # evaluate it
                    candidate = candidate()
                # if that fails
                except TypeError:
                    # move on
                    continue
                # if it succeeded, check the return type
                if not (isinstance(candidate, actor) or isinstance(candidate, component)):
                    # and move on if it's not a component
                    continue
                # if it is a component class and we have been asked to instantiate it
                if instanceName and isinstance(candidate, actor):
                    # make a locator
                    this = tracking.simple('while resolving {!r}'.format(uri.uri))
                    locator = tracking.chain(this=this, next=locator)
                    # instantiate
                    candidate = candidate(name=instanceName, locator=locator)

                # if it is compatible with me
                if candidate.pyre_isCompatible(protocol=cls):
                    # it has to be the one
                    yield candidate

        # out of ideas
        return


    @classmethod
    def pyre_find(cls, uri):
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

        # the nameserver knows the search path, already a list of uris
        searchpath = nameserver['pyre.configpath']
        # deduce my context path
        contextpath = nameserver.split(family) if family else ['']

        # the choices of leading segments
        roots = (p.address for p in reversed(searchpath))
        # sub-folders built out of progressively shorter leading portions of the family name
        folders = (
            fileserver.join(*contextpath[:marker])
            for marker in reversed(range(0, len(contextpath)+1)))
        # and the address specification from the {uri}
        address = [uri.address]
        # with all possible combinations of these three sequences
        for address in itertools.product(roots, folders, address):
            # build a better uri and return it
            yield cls.uri(scheme=vfs, address=fileserver.join(*address))

        # out of ideas
        return
        

# end of file 
