# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import collections


class PathHash:
    """
    Implementation of a hash function for hierarchical namespaces with aliased entries.

    PathHash encodes the hierarchical relationships among its contents by having each node in
    the hierarchy store the names of the nodes that are its immediate children. Aliases are
    permitted and they hash to the same key as the original entry.

    PathHash does not provide storage for any values associated with the names; that's the
    responsibility of the client. One implementation strategy is to create a dictionary at the
    client side that maps the nodes retrieved by searching into the namespace to the associated
    values.
    """


    def hash(self, name, separator):
        """
        Retrieve the node given by {name}.
        """
        # build the path
        path = name.split(separator) if separator else (name,)
        # find the right spot
        node = self
        for part in path:
            node = node.nodes[part]
        # and return it
        return node


    def alias(self, alias, original, separator):
        """
        Establish {alias} as alternative to {original}
        """
        # take the alias apart
        path = alias.split(separator) if separator else (alias,)
        # the address of the alias is everythin except the last entry in this path
        address = path[:-1]
        # the new name of the original node is the last chunk of the path
        alias = path[-1]
        # hunt down the right parent node
        parent = self
        for part in address:
            parent = parent.nodes[part]
        # now find the original node
        node = self.hash(original, separator)
        # create an entry named after the last chunk of the alias that points to the original
        parent.nodes[alias] = node
        # and return the original node
        return node


    def dump(self, graphic=''):
        """
        Dump out the names of all encountered nodes
        """
        for name, node in self.nodes.items():
            print("{0}{1!r}".format(graphic, name))
            node.dump(graphic=graphic+"  ")
        return
                  


    # meta methods
    def __init__(self):
        self.nodes = collections.defaultdict(PathHash)
        return


    __slots__ = ["nodes"]


# end of file 
