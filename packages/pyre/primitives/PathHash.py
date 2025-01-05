# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2025 all rights reserved
#


import collections


class PathHash:
    """
    Implementation of a hash function for hierarchical namespaces with aliased entries.

    PathHash encodes the hierarchical relationships among its contents by having each node in
    the hierarchy store the names of the nodes that are its immediate children. Aliases are
    permitted and they hash to the same key as the original entry.

    PathHash does not provide storage for any values associated with the names of the various
    levels in the hierarchy; that's the responsibility of the client. One implementation
    strategy is to create a dictionary at the client side that maps the keys generated by
    PathHash to the associated values.
    """


    def hash(self, items):
        """
        Hash {item}, assumed to be an iterable of address segments, and return its key
        """
        # starting with me
        node = self
        # go through the entries in {items}
        for part in items:
            # find the right spot
            node = node[part]
        # and return it
        return node


    def alias(self, target, alias):
        """
        Make the node {target} accessible under the name {alias}
        """
        # save the current hash key of {alias}, if any; check carefully so as not to disturb
        # the hash unnecessarily
        original = None if alias not in self else self[alias]
        # make {target} accessible as {alias}
        self[alias] = target
        # and return the original key
        return original


    # metamethods
    def __init__(self):
        # initialize the table of nodes
        self.nodes = collections.defaultdict(PathHash)
        # all done
        return


    def __contains__(self, name):
        """
        Check whether i have a hash key for {name}
        """
        # easy enough
        return name in self.nodes


    def __getitem__(self, name):
        """
        Hash {name}
        """
        # easy enough
        return self.nodes[name]


    def __setitem__(self, name, key):
        """
        Make {name} hash to {key}
        """
        # easy enough
        self.nodes[name] = key
        # all done
        return


    # debugging support
    def dump(self, graphic=''):
        """
        Dump out the names of all encountered nodes
        """
        # go through my nodes
        for name, node in self.nodes.items():
            # show me the name
            print("{}{!r}".format(graphic, name))
            # show me the contents
            node.dump(graphic=graphic+'  ')
        # all done
        return


    # implementation details
    # narrow down the footprint
    __slots__ = ["nodes"]


# end of file
