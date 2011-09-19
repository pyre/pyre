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

    # public data
    separator = None


    # interface obligations from SymbolTable
    @property
    def nodes(self):
        """
        Iterate over my nodes
        """
        # return the iterator over the registered nodes
        return self._nodes.values()


    # interface
    def eval(self, program):
        """
        Evaluate the compiled object {program} in the context of my registered nodes
        """
        return eval(program, self._nodes)



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
        # iterate over all the fully qualified names in the model
        for key, name in self._fqnames.items():
            # if the name matches the pattern
            if regex.match(name):
                # yield the fully qualified name and the value of the node
                yield name, self._nodes[self._identifiers[key]]
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
            # extract the identifier
            try:
                identifier = self._identifiers[key]
            # if not there...
            except KeyError:
                # it's because the key exists in the model but none of its immediate children
                # are leaf nodes with associated values. this happens often for configuration
                # settings to facilities that have not yet been converted into concrete
                # components; it also happens for configuration settings that are not meant for
                # components at all, such as journal channel activations.
                continue
            # extract the required information
            yield key, identifier, self._names[key], self._fqnames[key], self._nodes[identifier]

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
            aliasId = self._identifiers[aliasHash]
        # if the lookup fails
        except KeyError:
            # no node has been previously registered under this alias, so we are done. if a
            # registration appears, it will be treated as a duplicate and patched appropriately
            return self
        # now, look for the canonical node
        try:
            canonicalId = self._identifiers[canonicalHash]
        # if there was no canonical node
        except KeyError:
            # install the alias as the canonical 
            self._identifiers[canonicalHash] = aliasId
            self._names[canonicalHash] = canonicalKey[-1]
            self._fqnames[canonicalHash] = canonical
            # all done
            return
        # either way clean up after the obsolete aliased node
        finally:
            # clean up the names, but not the identifiers: they may be in use in some
            # expression that was compiled before the aliasing took place
            del self._names[aliasHash]
            del self._fqnames[aliasHash]

        # if we get this far, both preëxisted; the aliased info has been cleared out, the
        # canonical is as it should be. all that remains is to patch the two nodes
        aliasNode = self._nodes[aliasId]
        canonicalNode = self._nodes[canonicalId]
        self._patch(discard=aliasNode, replacement=canonicalNode)
        # and install the canonical node under the alias identifier
        self._nodes[aliasId] = canonicalNode

        # all done
        return self
        

    # meta methods
    def __init__(self, separator=SEPARATOR, **kwds):
        super().__init__(**kwds)

        # the level separator
        self.separator = separator
        self._tag = 0

        # node storage strategy
        self._nodes = {} # maps identifiers to nodes
        self._names = {} # maps hash keys to node name
        self._fqnames = {} # maps hash keys to fully qualified node names
        self._identifiers = {} # maps hash keys to identifiers
        self._hash = pyre.patterns.newPathHash()
        return


    # implementation details
    def _register(self, *, identifier, node):
        """
        Add {node} to the model and make it accessible through {identifier}
        """
        # add the node to the pile
        self._nodes[identifier] = node
        # and return
        return self


    def _resolve(self, *, name):
        """
        Find the named node
        """
        # build the key
        key = name.split(self.separator)
        # hash it
        hashkey = self._hash.hash(key)
        # attempt to map the {hashkey} into an identifier
        try:
            identifier = self._identifiers[hashkey]
        # if the lookup fails, this is the first request for this name
        except KeyError:
            # create a new identifier
            identifier = "_{}".format(self._tag)
            self._tag += 1
            # register it
            self._identifiers[hashkey] = identifier
            # adjust the name indices
            self._names[hashkey] = key[-1] # the name of the node
            self._fqnames[hashkey] = name  # the fqname of the node
            # build an error indicator
            node = self.unresolved(name=name) 
            # install it
            self._nodes[identifier] = node
        # if the lookup succeeded
        else:
            # look up the node
            node = self._nodes[identifier]

        # return the node and its identifier
        return node, identifier


    # debug support
    def dump(self, pattern=''):
        """
        List my contents
        """
        print("model {0!r}:".format(self.name))
        print("  nodes:")
        for name, node in self.select(pattern):
            print("    {!r} <- {!r}".format(name, node.value))
        return


# end of file 
