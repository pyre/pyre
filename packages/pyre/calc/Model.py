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
        # check whether this name has already been registered
        try:
            unresolved = self._nodes[name]
        except KeyError:
            # nope, this is the first time
            self._nodes[name] = node
            return
        # so, we have seen this name before
        # if it does not belong to an unresolved node
        if name not in self._unresolvedNames:
            # this is a name collision
            raise self.DuplicateNodeError(model=self, name=name, node=unresolved)
        # patching time...
        unresolved.cede(replacement=node)
        # remove the name from the unresolved pile
        self._unresolvedNames.remove(name)
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
        unresolved = self.newErrorNode(evaluator=UnresolvedNode(name))
        # add it to the pile
        self._nodes[name] = unresolved
        # and store the name so we can track these guys down
        self._unresolvedNames.add(name)
        # and return it
        return unresolved


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self._nodes = {}
        return


    # debugging support
    def _dump(self, pattern=None):
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
