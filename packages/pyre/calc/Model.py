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
    def eval(self, program):
        """
        Evaluate the compiled object {program} in the context of my registered nodes
        """
        return eval(program, self._nodes)


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self._nodes = {} # map of identifiers to registered nodes
        self._names = {} # map of node names to identifiers
        return


    # implementation details
    def _register(self, *, identifier, node):
        """
        Add {node} into the model and make it accessible under {name}
        """
        # print("pyre.calc.Model.register: name={!r}, node={}".format(name, node))
        # add the node to the pile
        self._nodes[identifier] = node
        # and return
        return self


    def _resolve(self, name):
        """
        Find the named node
        """
        # attempt to map the {name} into an identifier
        try:
            identifier = self._names[name]
        # if the lookup fails, this is the first request for this name
        except KeyError:
            # create a new identifier
            identifier = "_{}".format(len(self._names))
            # register it
            self._names[name] = identifier
            # build an error indicator
            node = self.unresolved(name)
            # print("pyre.calc.Model.resolve: new unresolved node {!r} {}".format(name, node))
            # add it to the pile
            self._nodes[identifier] = node
        # if it succeeds
        else:
            # look up the actual node
            node = self._nodes[identifier]

        # and return the node and its identifier
        return node, identifier


    # private data
    _nodes = None # map of identifiers to registered nodes
    _names = None # map of node names to python identifiers used in compiling expressions


# end of file 
