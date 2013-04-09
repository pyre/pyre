# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import re
import operator
import collections
from .. import patterns
# my base class
from .SymbolTable import SymbolTable


# declaration
class Hierarchical(SymbolTable):
    """
    Storage and naming services for algebraic nodes

    This class assumes that the node names form a hierarchy, very much like path
    names. Subclasses define what the level separator is; {Hierarchical} is shielded from this
    decision by expecting names to be iterables of strings specifying the name of each level.

    {Hierarchical} provides support for links, entries that are alternate names for other
    folders.
    """


    # public data
    separator = '.'


    # interface
    # model traversal
    def children(self, key):
        """
        Given the address {key} of a node, iterate over all the canonical nodes that are
        its logical children
        """
        # hash the root key
        # print("HierarchicalModel.children: key={}".format(key))
        hashkey = self.hash(key)
        # extract the unique hashed keys (to avoid double counting aliases)
        unique = set(hashkey.nodes.values())
        # iterate over the unique keys
        for childkey in unique:
            # print("  looking for:", key)
            # extract the node
            try:
                childnode = self._nodes[childkey]
            # if not there...
            except KeyError:
                # it's because the key exists in the model but none of its immediate children
                # are leaf nodes with associated values. this happens often for configuration
                # settings to facilities that have not yet been converted into concrete
                # components; it also happens for configuration settings that are not meant for
                # components at all, such as journal channel activations.
                continue
            # extract the required information
            yield childkey, childnode

        # all done
        return


    def find(self, pattern=''):
        """
        Generate a sequence of (name, node) pairs for all nodes in the model whose name
        matches the supplied {pattern}. Careful to properly escape periods and other characters
        that may occur in the name of the requested keys that are recognized by the {re}
        package
        """
        # check whether i have any nodes
        if not self._nodes: return
        # build the name recognizer
        regex = re.compile(pattern)
        # iterate over my nodes
        for key, name in sorted(self._names.items(), key=operator.itemgetter(1)):
            # if the name matches
            if regex.match(name):
                # yield the name and the node
                yield name, self._nodes[key]
        # all done
        return

    
    # storing and retrieving nodes
    def alias(self, target, alias, base=None):
        """
        Register the name {alias} as an alternate name for {target}
        """
        # build the keys
        target = self.hash(target)
        base = self._hash if base is None else self.hash(base)
        # ask the hash to alias the two names and retrieve the original key
        alias = base.alias(alias=alias, target=target)
        
        # now that the two names are aliases of each other, we must resolve the potential node
        # conflict: only one of these is accessible by name any more

        # look for a preëxisting node under the canonical hash
        canonicalNode = self._nodes.get(target)
        # and one under the alias
        aliasNode = self._nodes.get(alias)

        # if there is no node that has been previously registered under this alias, we are
        # done. if a registration appears, it will be treated as a duplicate and patched
        # appropriately
        if aliasNode is None:
            # return the canonical node, whether it exists or not; the latter case corresponds
            # to aliasing among names that do not yet have a configuration node built
            return target, alias, canonicalNode
        # clean up after the obsolete node
        del self._nodes[alias]
        del self._names[alias] # this was missing; oversight?
        # if there is no node under the canonical name
        if canonicalNode is None:
            # install the alias node as the canonical
            self._nodes[target] = aliasNode
            # and return the alias node
            return target, alias, aliasNode

        # if we get this far, both preëxisted; the aliased info has been cleared out, the
        # canonical is as it should be. all that remains is to patch the two nodes and return
        # the survivor
        survivor = self.node.select(model=self, existing=aliasNode, replacement=canonicalNode)
        # update the model
        self._nodes[target] = survivor
        # all done
        return target, alias, survivor


    def hash(self, name):
        """
        Split a multilevel {name} into its parts and return its hash
        """
        # if {name} is already a hash key
        if isinstance(name, type(self._hash)):
            # leave it alone
            return name
        # if {name} is a string
        if isinstance(name, str):
            # hash it
            return self._hash.hash(items=name.split(self.separator))
        # if it is an iterable
        if isinstance(name, collections.Iterable):
            # skip the split, just hash
            return self._hash.hash(items=name)
        # otherwise
        raise ValueError("can't hash {!r}".format(name))


    def insert(self, key, node, name=None):
        """
        Register the new {node} in the model under {name}
        """
        # attempt to
        try:
            # retrieve the existing one
            old = self._nodes[key]
        # if it's not there
        except KeyError:
            # this is a new registration
            self._nodes[key] = node
            self._names[key] = name
        # if it's there
        else:
            # choose the survivor
            node = self.node.select(model=self, existing=old, replacement=node)
            # update the model
            self._nodes[key] = node
        # all done
        return key, node
                    

    def getNode(self, key):
        """
        Retrieve the node registered under {key}
        """
        # look it up in my node map
        return self._nodes[key]


    def getName(self, key):
        """
        Retrieve the name of the node registered under {key}
        """
        # look it up in my name map
        return self._names[key]


    def lookup(self, key):
        """
        Retrieve the node registered under {key}, raising a {KeyError} if no such node exists
        """
        # look it up in my nodemap and return it
        return self._nodes[key], self._names[key]


    def retrieve(self, name):
        """
        Retrieve the node registered under {name}. If no such node exists, an error marker will
        be built, stored in the symbol table under {name}, and returned.
        """
        # hash the {name}
        key = self.hash(name)
        # if a node is already registered under this key
        try:
            # grab it
            node = self._nodes[key]
        # otherwise
        except KeyError:
            # build an error marker
            node = self.node.unresolved(request=name)
            # add it to the pile
            self._nodes[key] = node
            self._names[key] = name
        # return the node
        return node


    def split(self, name):
        """
        Take {name} apart using my separator
        """
        # easy enough
        return name.split(self.separator)


    def join(self, *levels):
        """
        Form the canonical name of a key by joining {levels} using my separator
        """
        # easy enough
        return self.separator.join(levels)


    # meta-methods
    def __init__(self, separator=separator, **kwds):
        super().__init__(**kwds)
        # record my separator
        self.separator = separator
        # initialize my name hash
        self._hash = patterns.newPathHash()
        # and my name map
        self._names = {}
        # all done
        return


    def __contains__(self, name):
        """
        Check whether {item} is present in the table
        """
        # check whether the hashed name is present in my node index
        return self.hash(name) in self._nodes


    def __getitem__(self, name):
        """
        Get the node associate with {name}
        """
        # find the node
        node = self.retrieve(name)
        # and return its value
        return node.value


    def __setitem__(self, name, value):
        """
        Convert {value} into a node and update the model
        """
        # hash the name
        key = self.hash(name)
        # convert value into a node
        new = self.interpolation(value=value)
        # delegate
        return self.insert(name=name, key=key, node=new)


    # implementation details
    # private data
    _hash = None
    _names = None


    # debug support
    def dump(self, pattern=''):
        """
        List my contents
        """
        print("model {}:".format(self))
        print("  nodes:")
        for name, node in self.find(pattern):
            node.dump(indent=' '*4, name=name)
            print("      slot: {}".format(type(node).__name__))
        return


# end of file 
