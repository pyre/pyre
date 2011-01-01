# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import collections


class PathHash:
    """
    Implementation of a hash function for hierarchical namespaces with aliased entries.

    PathHash encodes the hierarchical relationships among its contents by having each node in
    the hierarchy store the names of the nodes that are its immediate children. Aliases are
    permitted and they hash to the same key as the original entry.

    PathHash does not provide storage for any values associated with the names of the various
    levelsin the hierarchy; that's the responsibility of the client. One implementation
    strategy is to create a dictionary at the client side that maps the keys generated by
    pathhash to the associated values.
    """


    def hash(self, key):
        """
        Retrieve the node given by {key}, assumed to be an iterable of address segments
        """
        # find the right spot
        node = self
        for part in key:
            node = node.nodes[part]
        # and return it
        return node


    def alias(self, alias, canonical):
        """
        Establish {alias} as alternative to {canonical}

        Each is expected to be an iterable of level names starting from the root of the
        pathhash.
        """
        # find the node that corresponds to the canonical key
        base = self.hash(canonical)
        # retrieve the hash key of the parent node where the alias is to be registered
        parent = self.hash(key=alias[:-1])
        # the new name is the last fragment of the alias path
        newname = alias[-1]
        # save the original key for the alias
        original = parent.nodes[newname]
        # create an entry for it that points to the original
        parent.nodes[newname] = base
        # and return the original node
        return original, base


    def dump(self, graphic=''):
        """
        Dump out the names of all encountered nodes
        """
        for name, node in self.nodes.items():
            print("{}{!r}".format(graphic, name))
            node.dump(graphic=graphic+"  ")
        return


    # meta methods
    def __init__(self):
        self.nodes = collections.defaultdict(PathHash)
        return


    __slots__ = ["nodes"]


# end of file 
