# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
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
        Iterate over the nodes in my graph
        """
        return self._nodes.values()


    def register(self, *, name, node):
        """
        Add {node} into the model and make it accessible through {name}
        """
        # print("pyre.calc.Model.register: name={!r}, node={}".format(name, node))
        # check whether we already have a node registered nuder this name
        try:
            existing = self._nodes[name]
        except KeyError:
            # nope, first time
            # node.dump()
            self._nodes[name] = node
            return self
        # patch the evaluation graph
        # print("pyre.calc.Model.resolve: patching {!r} {}".format(name, existing))
        self.patch(keep=existing, discard=node)
        # and return
        return self


    def resolve(self, name):
        """
        Find the named node
        """
        # attempt to return the node that is registered under {name}
        try:
           return self._nodes[name]
        # not there...
        except KeyError:
            pass
        # otherwise, build an unresolved node
        from .UnresolvedNode import UnresolvedNode
        node = UnresolvedNode(name)
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
