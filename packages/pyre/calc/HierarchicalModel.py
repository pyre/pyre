# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# packages
import re
import itertools
import pyre.patterns
# super-class
from .SymbolTable import SymbolTable


# declaration
class HierarchicalModel(SymbolTable):
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
    class slot:
        # public data
        name = None
        node = None
        

    # public data
    separator = None


    # interface obligations from SymbolTable
    @property
    def nodes(self):
        """
        Iterate over my nodes
        """
        # iterate over my slots
        for slot in self.slots.values():
            # yield the associated node
            yield slot.node
        # all done
        return


    # interface
    # model traversal
    def select(self, pattern=''):
        """
        Generate a sequence of (name, value) pairs for all nodes in the model whose name
        matches the supplied {pattern}. Careful to properly escape periods and other characters
        that may occur in the name of the requested keys that are recognized by the {re}
        package
        """
        # check whether i have any nodes
        if not self.slots: return
        # build the name recognizer
        regex = re.compile(pattern)
        # iterate over my slots
        for slot in self.slots:
            # get the name of the slot
            name = slot.name
            # if the name matches
            if regex.match(name):
                # yield the name and the node
                yield name, slot.node
        # all done
        return


    def children(self, root=None, rootKey=None):
        """
        Given the name {root}, iterate over all the canonical nodes that are its logical
        children
        """
        # build the root key
        rootKey = rootKey if rootKey is not None else root.split(self.separator)
        # hash it
        # print("HierarchicalModel.children: rootKey={}".format(rootKey))
        rootKey = self._hash.hash(rootKey)
        # print("   names: {}".format(rootKey.nodes.items()))
        # extract the unique hash subkeys
        unique = set(rootKey.nodes.values())
        # iterate over the unique keys
        for key in unique:
            # print("  looking for:", key)
            # extract the slot
            try:
                slot = self.slots[key]
            # if not there...
            except KeyError:
                # it's because the key exists in the model but none of its immediate children
                # are leaf nodes with associated values. this happens often for configuration
                # settings to facilities that have not yet been converted into concrete
                # components; it also happens for configuration settings that are not meant for
                # components at all, such as journal channel activations.
                continue
            # extract the required information
            yield key, slot

        # all done
        return


    # alternative node access
    def alias(self, *, alias, canonical):
        """
        Register the name {alias} as an alternate name for {canonical}
        """
        # build the multikeys
        aliasKey = alias.split(self.separator)
        canonicalKey = canonical.split(self.separator)
        # ask the hash to alias the two names and retrieve the corresponding hash keys
        aliasHash, canonicalHash = self._hash.alias(alias=aliasKey, canonical=canonicalKey)

        # now that the two names are aliases of each other, we must resolve the potential node
        # conflict: only one of these is accessible by name any more

        # look for a preëxisting node under the alias
        try:
            aliasSlot = self.slots[aliasHash]
        # if the lookup fails
        except KeyError:
            # no node has been previously registered under this alias, so we are done. if a
            # registration appears, it will be treated as a duplicate and patched appropriately
            return self
        # now, look for the canonical node
        try:
            canonicalSlot = self.slots[canonicalHash]
        # if there was no canonical node
        except KeyError:
            # install the alias as the canonical 
            self.slots[canonicalHash] = aliasSlot
            # all done
            return
        # either way clean up after the obsolete aliased node
        finally:
            # nothing could hash to {aliasHash} any more, so clear out the entry
            del self.slots[aliasHash]

        # if we get this far, both preëxisted; the aliased info has been cleared out, the
        # canonical is as it should be. all that remains is to patch the two nodes
        aliasNode = aliasSlot.node
        canonicalNode = canonicalSlot.node
        self._update(identifier=canonicalHash, existing=aliasNode, replacement=canonicalNode)

        # all done
        return self
        

    # meta methods
    def __init__(self, separator=SEPARATOR, **kwds):
        super().__init__(**kwds)

        # the level separator
        self.separator = separator

        # node storage strategy
        self.slots = {} # maps hash keys to slots
        self._hash = pyre.patterns.newPathHash()
        return


    # implementation details
    def _resolve(self, *, name):
        """
        Find the named node
        """
        # build the key
        key = name.split(self.separator)
        # hash it
        hashkey = self._hash.hash(key)
        # attempt to map the {hashkey} into a slot
        try:
            slot = self.slots[hashkey]
        # if the lookup fails, this is the first request for this name
        except KeyError:
            # create a new slot
            slot = self.slot()
            # attach the name
            slot.name = name
            # build an error indicator
            slot.node = self.unresolved(name=name) 
            # install it
            self.slots[hashkey] = slot
        # if the lookup succeeded
        else:
            # look up the node
            slot = self.slots[hashkey]

        # return the node and its identifier
        return slot.node, hashkey


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
            # get the matching slot
            slot = self.slots[identifier]
            # check that it is the right one
            assert slot.node is existing
            # place the new node in the slot
            slot.node = replacement
            # patch the node dependencies
            self._patch(identifier, existing, replacement)
        # all done
        return self


    # debug support
    def dump(self, pattern=''):
        """
        List my contents
        """
        print("model {0!r}:".format(self.name))
        print("  nodes:")
        for name, node in self.select(pattern):
            try: 
                value = node.value
            except self.UnresolvedNodeError:
                value = "unresolved"
            print("    {!r} <- {!r}".format(name, value))
        return


# end of file 
