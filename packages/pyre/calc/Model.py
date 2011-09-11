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


    # interface
    def register(self, *, name, node):
        """
        Add {node} into the model and make it accessible under {name}
        """
        # print("pyre.calc.Model.register: name={!r}, node={}".format(name, node))
        # add the node to the pile
        self._nodes[name] = node
        # and return
        return self


    def resolve(self, name):
        """
        Resolve {name} into a node and return its value
        """
        # attempt to find the node that is registered under {name}
        try:
            # and return it
            return self._nodes[name]
        # otherwise
        except KeyError:
            pass
        # build an error indicator
        node = self.unresolved(name)
        # print("pyre.calc.Model.resolve: new unresolved node {!r} {}".format(name, node))
        # add it to the pile
        self._nodes[name] = node
        # and return it
        return node


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self._nodes = {}
        return


# end of file 
