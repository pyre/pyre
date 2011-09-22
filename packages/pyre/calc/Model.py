# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .SymbolTable import SymbolTable


class Model(SymbolTable):
    """
    A {SymbolTable} implementation that uses a dictionary for node storage
    """


    # public data
    @property
    def nodes(self):
        """
        Build an iterable over the nodes in my graph

        This is expected to return the complete sequence of nodes, regardless of the storage
        details implemented by AbstractModel descendants
        """
        # easy enough...
        return self._nodes.values()


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self._nodes = {} # map of names to registered nodes
        return


    # implementation details
    def _resolve(self, name):
        """
        Find the named node
        """
        # attempt to map the {name} into a node
        try:
            node = self._nodes[name]
        # if the lookup fails, this is the first request for this name
        except KeyError:
            # build an error indicator
            node = self.unresolved(name)
            # print("pyre.calc.Model.resolve: new unresolved node {!r} {}".format(name, node))
            # add it to the pile
            self._nodes[name] = node

        # and return the node and its identifier
        return node, name


    def _update(self, *, identifier, existing, replacement):
        """
        Update the model by resolving the name conflict among the two nodes, {existing} and
        {replacement}
        """
        # bail out if the two nodes are identical
        if existing is replacement: return self
        # if they are both {var} instances
        if isinstance(existing, self.var) and isinstance(replacement, self.var):
            # just transfer the value
            existing.value = replacement.value
        # otherwise
        else:
            # place the new node in the model
            self._nodes[identifier] = replacement
            # patch the node dependencies
            self._patch(identifier, existing, replacement)
        # all done
        return self


    # private data
    _nodes = None # map of names to registered nodes


# end of file 
