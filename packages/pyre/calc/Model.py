# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .AbstractModel import AbstractModel


class Model(AbstractModel):
    """
    Storage and naming services for calc nodes
    """


    # types
    from .Node import Node
    from .Evaluator import Evaluator
    from .Expression import Expression
    from .Literal import Literal


    # interface
    @property
    def nodes(self):
        """
        Iterate over the nodes in my graph. Returns a sequence of ({name}, {node}) tuples.
        """
        return self._nodes.values()


    def register(self, *, name, node):
        """
        Add {node} into the model and make it accessible through {name}
        """
        # resolve the name
        # N.B.: this always succeeds: the first time {name} is encountered we get a node with
        # an UnresolvedNode evaluator
        existing = self.resolve(name)
        # patching time...
        # update the set of observers of the new node
        node.observers.update(existing.observers)
        # notify the old observers of the change
        for observer in existing.observers:
            # domain adjustments
            observer.patch(new=node, old=existing)
        # place the node in the model
        self._nodes[name] = node
        # and return
        return self


    def resolve(self, name):
        """
        Find the named node
        """
        # attempt to return the node that is registered under {name}
        try:
            return self._nodes[name]
        except KeyError:
            pass
        # otherwise, build an unresolved node
        from .UnresolvedNode import UnresolvedNode
        unresolved = self.newNode(evaluator=UnresolvedNode(name))
        # add it to the pile
        self._nodes[name] = unresolved
        # and return it
        return unresolved


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
        self._nodes = {}
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


    # debugging support
    def dump(self, pattern=None):
        """
        List my contents
        """
        # build the node name recognizer
        import re
        regex = re.compile(pattern if pattern else '')

        print("model {0!r}:".format(self.name))
        for name, node in sorted(self._nodes.items()):
            if regex.match(name):
                print("    {0!r}: {1!r}".format(name, node.value))
        return


# end of file 
