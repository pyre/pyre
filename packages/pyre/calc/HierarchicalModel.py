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


    # types
    from .Node import Node
    from .Evaluator import Evaluator
    from .Expression import Expression
    from .Literal import Literal


    # interface obligations from AbstractModel
    @property
    def nodes(self):
        """
        Iterate over my nodes
        """
        # return the iterator over the registered nodes
        return self._nodes.values()


    def register(self, *, name, node):
        """
        Add {node} into the model and make it accessible through {name}
        """
        # split the name into its parts and hash it
        key = self._hash.hash(name.split(self.SEPARATOR))
        # check whether we have a node registered under this name
        try:
            existing = self._nodes[key]
        except KeyError:
            # nope, first time
            self._nodes[key] = node
            self._names[key] = name
            return self
        # patching time
        # update the observers of the new node
        node.observers.update(existing.observers)
        # notify the old obervers of the change
        for observer in existing.observers:
            # domain adjustments
            observer.patch(new=node, old=existing)
        # place the node in the model
        self._nodes[key] = node
        # and return
        return self
            
            
    def resolve(self, name):
        """
        Find the named node
        """
        # split the name into its parts and hash it
        key = self._hash.hash(name.split(self.SEPARATOR))
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


    # factory for my nodes
    def newNode(self, evaluator):
        """
        Create a new error node with the given evaluator
        """
        # why is this the right node factory?
        # subclasses should override this to provide their own nodes to host the evaluator
        from .Node import Node
        return Node(value=None, evaluator=evaluator)


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)

        # node storage strategy
        self._names = {}
        self._nodes = {}
        self._hash = pyre.patterns.newPathHash()
        return


    # subscripted access
    def __getitem__(self, name):
        #  this is easy: get resolve to hunt down the node associated with {name}
        return self.resolve(name)


    def __setitem__(self, name, value):
        # identify what kind of value we were given
        # if {value} is another node
        if isinstance(value, self.Node): 
            # easy enough
            node = value
        # if {value} is an evaluator 
        elif isinstance(value, self.Evaluator):
            # build a node with this evaluator
            node = self.newNode(evaluator=value)
        # if it is a string
        elif isinstance(value, str):
            # check whether it is an expression
            try:
                expression = self.Expression.parse(expression=value, model=self)
            except self.NodeError:
                # treat it like a literal
                node = self.newNode(evaluator=self.Literal(value=value))
            else:
                # build a node with this evaluator
                node = self.newNode(evaluator=expression)
        # otherwise
        else:
            # build a literal
            node = self.newNode(evaluator=self.Literal(value=value))
        # now, let register do its magic
        self.register(name=name, node=node)
        # all done
        return


# end of file 
