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

    # public data
    separator = None


    # interface obligations from AbstractModel
    @property
    def nodes(self):
        """
        Iterate over my nodes
        """
        # return the iterator over the registered nodes
        return self._nodes.values()


    # interface
    def alias(self, alias, canonical):
        """
        """
        # ask the hash to alias the two names and retrieve the corresponding hash keys
        aliasKey, canonicalKey = self._hash.alias(
            alias=alias.split(self.separator), canonical=canonical.split(self.separator))
        # now that the two names are aliases of each other, we must resolve the potential node
        # conflict: only one of these is accessible by name any more
        # look for a preëxisting node under the alias
        try:
            aliasNode = self._nodes[aliasKey]
        except KeyError:
            # if no node has been previously registered under the alias we are done
            # if a registration appears, it will be treated as a duplicate by regiter, and
            # patched appropriately
            return self
        # now, look for the canonical node
        try:
            canonicalNode = self._nodes[canonicalKey]
        except KeyError:
            canonicalNode = None
        # now, there are two cases to handle depending on whether canonical node was registerd
        # already; either way clean up after the obsolete aliased node
        del self._names[aliasKey]
        del self._nodes[aliasKey]
        # first, if there was no canonical node
        if canonicalNode is None:
            # install the alias as the canonical 
            self._names[canonicalKey] = canonical
            self._nodes[canonicalKey] = aliasNode
            # all done
            return
        # finally, both preëxisted; the aliased info has been cleared out, the canonical is as
        # it should be. all that remains is to patch the two nodes
        self.patch(old=aliasNode, new=canonicalNode)
        # all done
        return self
        

    # AbstractModel obligations 
    def register(self, *, name, node):
        """
        Add {node} into the model and make it accessible through {name}
        """
        # split the name into its parts and hash it
        # N.B.: when multiple names hash to the same key, the code below does not alter the
        # name database. this is as it should so that aliases are handled correctly. make sure
        # to repsect this invariant when modifying what follows
        key = self._hash.hash(name.split(self.separator))
        # check whether we have a node registered under this name
        try:
            existing = self._nodes[key]
        except KeyError:
            # nope, first time
            self._nodes[key] = node
            self._names[key] = name
            return self
        # patch the evaluation graph
        self.patch(old=existing, new=node)
        # place the node in the model
        self._nodes[key] = node
        # and return
        return self
            
            
    def resolve(self, name):
        """
        Find the named node
        """
        # split the name into its parts and hash it
        key = self._hash.hash(name.split(self.separator))
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


    # meta methods
    def __init__(self, separator=SEPARATOR, **kwds):
        super().__init__(**kwds)

        # the level separator
        self.separator = separator

        # node storage strategy
        self._names = {}
        self._nodes = {}
        self._hash = pyre.patterns.newPathHash()
        return


    # debug support
    def dump(self, pattern=None):
        """
        List my contents
        """
        # build the node name recognizer
        import re
        regex = re.compile(pattern if pattern else '')

        print("model {0!r}:".format(self.name))
        for key in self._nodes.keys():
            name = self._names[key]
            if regex.match(name):
                node = self._nodes[key]
                print("  {0!r} <- {1!r}".format(name, node.value))
                
        return


# end of file 
