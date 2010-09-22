# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import pyre.patterns
from .AbstractModel import AbstractModel


class HierarchicalModel(AbstractModel):
    """
    Storage and naming services for calc nodes

    This class assumes that the node names form a hierarchy, very much like path names. They
    are expected to be given as tuples of strings that specify the names of the "folders" at
    each level.

    HierarchicalModel provides support for links, entries that are alternate names for other
    folders.
    """


    # constants
    SEPARATOR = '.'

    # public data
    separator = None


    # interface obligations from AbstractModel
    @property
    def nodes(self):
        """
        Iterate over my nodes
        """
        # return the iterator over the registered nodes
        return self._nodes.values()


    # interface
    def alias(self, alias, canonical):
        """
        """
        print("Hierarchical.alias:")
        # ask the hash to alias the two names and retrieve the corresponding hash keys
        aliasKey, canonicalKey = self._hash.alias(
            alias=alias.split(self.separator), canonical=canonical.split(self.separator))
        try:
            existing = self._nodes[canonicalKey]
        except KeyError:
            existing = None
        print("  canonical={!r}".format(canonical))
        print("     key={!r}".format(canonicalKey))
        print("     node={!r}".format(existing))
        
        try:
            obsolete = self._nodes[aliasKey]
        except KeyError:
            obsolete = None
        print("   alias={!r}".format(alias))
        print("       key={!r}".format(aliasKey))
        print("       node={!r}".format(obsolete))
        

    # AbstractModel obligations 
    def register(self, *, name, node):
        """
        Add {node} into the model and make it accessible through {name}
        """
        # split the name into its parts and hash it
        key = self._hash.hash(name.split(self.separator))
        # check whether we have a node registered under this name
        try:
            existing = self._nodes[key]
        except KeyError:
            # nope, first time
            self._nodes[key] = node
            self._names[key] = name
            return self
        # patch the evaluation graph
        self.patch(old=existing, new=node)
        # place the node in the model
        self._nodes[key] = node
        # and return
        return self
            
            
    def resolve(self, name):
        """
        Find the named node
        """
        # split the name into its parts and hash it
        key = self._hash.hash(name.split(self.separator))
        # attempt to return the node that is registered under {name}
        try:
            node = self._nodes[key]
        except KeyError:
            # otherwise, build an unresolved node
            from .UnresolvedNode import UnresolvedNode
            node = self.newNode(evaluator=UnresolvedNode(name))
            # add it to the pile
            self._names[key] = name
            self._nodes[key] = node
        # and return it
        return node


    # meta methods
    def __init__(self, separator=SEPARATOR, **kwds):
        super().__init__(**kwds)

        # the level separator
        self.separator = separator

        # node storage strategy
        self._names = {}
        self._nodes = {}
        self._hash = pyre.patterns.newPathHash()
        return


# end of file 
