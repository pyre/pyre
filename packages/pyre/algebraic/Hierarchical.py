# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# packages
import re
import pyre.patterns
# super-class
from .SymbolTable import SymbolTable


# declaration
class Hierarchical(SymbolTable):
    """
    Storage and naming services for algebraic nodes

    This class assumes that the node names form a hierarchy, very much like path names. They
    are expected to be given as tuples of strings that specify the names of the "folders" at
    each level.

    HierarchicalModel provides support for links, entries that are alternate names for other
    folders.
    """


    # types
    # my node type
    from .Node import Node


    # public data
    separator = '.'


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
        if not self._nodes: return
        # build the name recognizer
        regex = re.compile(pattern)
        # iterate over my nodes
        for node in self.nodes:
            # get the name of the node
            name = node.name
            # if the name matches
            if regex.match(name):
                # yield the name and the node
                yield name, node
        # all done
        return


    def children(self, key):
        """
        Given the address {key} of a node, iterate over all the canonical nodes that are
        its logical children
        """
        # hash the root key
        # print("HierarchicalModel.children: key={}".format(key))
        hashkey = self._hash.hash(key)
        # print("   names: {}".format(key.nodes.items()))
        # extract the unique hashed keys (to avoid double counting aliases)
        unique = set(hashkey.nodes.values())
        # iterate over the unique keys
        for key in unique:
            # print("  looking for:", key)
            # extract the node
            try:
                node = self._nodes[key]
            # if not there...
            except KeyError:
                # it's because the key exists in the model but none of its immediate children
                # are leaf nodes with associated values. this happens often for configuration
                # settings to facilities that have not yet been converted into concrete
                # components; it also happens for configuration settings that are not meant for
                # components at all, such as journal channel activations.
                continue
            # extract the required information
            yield key, node

        # all done
        return


    # alternative node access
    def alias(self, *, alias, canonical):
        """
        Register the name {alias} as an alternate name for {canonical}
        """
        # build the keys
        aliasKey = alias.split(self.separator)
        canonicalKey = canonical.split(self.separator)
        # delegate
        return self._alias(alias=aliasKey, canonical=canonicalKey)


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)

        # name hashing algorithm storage strategy
        self._hash = pyre.patterns.newPathHash()

        return


    def __contains__(self, name):
        """
        Check whether {name} is present in the table without modifying the table as a side-effect
        """
        # build the key
        key = name.split(self.separator)
        # hash it
        hashkey = self._hash.hash(key)
        # and check whether it is already present in my node index
        return hashkey in self._nodes


    # implementation details
    def _alias(self, *, alias, canonical):
        """
        Establish the key {alias} as an alternate to {canonical}
        """
        # print(" * algebraic.Hierarchical._alias")
        # print("     canonical: {}".format(canonical))
        # print("     alias: {}".format(alias))
        # ask the hash to alias the two names and retrieve the corresponding hash keys
        aliasHash, canonicalHash = self._hash.alias(alias=alias, canonical=canonical)

        # now that the two names are aliases of each other, we must resolve the potential node
        # conflict: only one of these is accessible by name any more

        # look for a preëxisting node under the canonical hash
        canonicalNode = self._nodes.get(canonicalHash)
        # and one under the alias
        aliasNode = self._nodes.get(aliasHash)
        # print(" ++  canonical node: {}".format(canonicalNode))
        # canonicalNode.dump()
        # print(" ++  alias node: {}".format(aliasNode))
        # aliasNode.dump()

        # if there is no node that has been previously registered under this alias, we are
        # done. if a registration appears, it will be treated as a duplicate and patched
        # appropriately
        if aliasNode is None:
            # return the canonical node, whether it exists or not; the latter case corresponds
            # to aliasing among names that do not yet have a configuration node built, which is
            # currently doable only programmatically
            return canonicalNode
        # clean up after the obsolete node
        del self._nodes[aliasHash]
        # if there is no node under the canonical name
        if canonicalNode is None:
            # install the alias node as the canonical
            self._nodes[canonicalHash] = aliasNode
            # and return the alias node
            return aliasNode

        # if we get this far, both preëxisted; the aliased info has been cleared out, the
        # canonical is as it should be. all that remains is to patch the two nodes and return
        # the survivor
        return canonicalNode.setValue(value=aliasNode)


    def _resolve(self, name):
        """
        Find the named node
        """
        # find and return the node and its identifier
        return self._retrieveNode(key=name.split(self.separator), name=name)


    def _retrieveNode(self, key, name):
        """
        Retrieve the node associated with {name}
        """
        # hash it
        hashkey = self._hash.hash(key)
        # attempt
        try:
            # to retrieve and return the node
            return self._nodes[hashkey], hashkey
        # if not there
        except KeyError:
            # no worries
            pass

        # build the name
        name = self.separator.join(key)
        # create a new node
        node = self._buildPlaceholder(name=name, identifier=hashkey if key else None)
        # if the request happened with a valid key
        if key:
            # register the new node
            self._nodes[hashkey] = node
        # and return the node and its identifier
        return node, hashkey


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
