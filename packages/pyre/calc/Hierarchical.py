# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
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


    # types
    from .exceptions import AliasingError
    from .NodeInfo import NodeInfo as info


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
        # print("Hierarchical.children: key={}".format(key))
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


    def find(self, pattern='', key=None):
        """
        Generate a sequence of (name, node) pairs for all nodes in the model whose name
        matches the supplied {pattern}. Careful to properly escape periods and other characters
        that may occur in the name of the requested keys that are recognized by the {re}
        package. The order in which the nodes are returned is controlled by {key}.
        """
        # check whether i have any nodes
        if not self._nodes: return
        # build the name recognizer
        regex = re.compile(pattern)
        # we need a key, since slots are not orderable
        key = operator.attrgetter('name') if key is None else key
        # iterate over my nodes
        for info in sorted(self._metadata.values(), key=key):
            # if the name matches
            if regex.match(info.name):
                # yield the name and the node
                yield info, self._nodes[info.key]
        # all done
        return


    # storing and retrieving nodes
    def alias(self, target, alias, base=None):
        """
        Within the context of {base}, register the name {alias} as an alternate name for
        {target}. The net effect is to make {base.alias} point to {target}.

        parameters:
          {target}: the canonical name/key that owns the associated node
           {alias}: the alternate name, a string with no implied structure
            {base}: the context name/key within which the alias is established;
                    defaults to global scope

        If both {target} and {alias} exist, an exception is raised; if the caller ignores this
        exception, the net effect is to make the {target} value accessible under both names,
        and discard the value previously registered under {alias}.
        """
        # hash the target
        targetKey = self.hash(target)
        # deduce the base context
        baseKey = self._hash if base is None else self.hash(base)
        # ask the base to alias the two names and return the key under which the alias might
        # have been registered originally
        aliasKey = baseKey.alias(target=targetKey, alias=alias)

        # now that the two names are aliases of each other, we must resolve the potential node
        # conflict: only one of these is accessible by name any more

        # look for a preëxisting node under the alias
        aliasNode = self._nodes.get(aliasKey)
        # and one under the canonical key
        targetNode = self._nodes.get(targetKey)

        # if there is no node that has been previously registered under this alias, we are
        # done. if a registration appears, it will be treated as a duplicate and patched
        # appropriately
        if aliasNode is None:
            # all done
            return
        # grab the alias metadata
        aliasInfo = self._metadata[aliasKey]
        # clean up after the obsolete node
        del self._nodes[aliasKey] # not accessible any more
        del self._metadata[aliasKey] # assuming the alias meta-data was not authoritative...
        # if there is no node under the canonical name
        if targetNode is None:
            # install the alias node as the canonical
            return self.replaceCanonical(key=targetKey, target=target, alias=alias,
                                         aliasNode=aliasNode, aliasInfo=aliasInfo)

        # if we get this far, both preëxisted; the aliased info has been cleared out, the
        # canonical is as it should be. all that's missing is a basis for picking which one to
        # keep; grab the target info
        targetInfo = self._metadata[targetKey]
        # and see if someone know what to do
        return self.resolveAliasingConflict(
            key=targetKey, target=target, alias=alias,
            targetNode=targetNode, targetInfo=targetInfo, aliasNode=aliasNode, aliasInfo=aliasInfo)


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


    def insert(self, key, value, name=None):
        """
        Register the new {node} in the model under {name}
        """
        # convert value into a node
        node = self.interpolation(value=value)
        # attempt to
        try:
            # retrieve the existing one
            old = self._nodes[key]
        # if it's not there
        except KeyError:
            # this is a new registration; fill out the node id
            name, split, key = self.info.fillNodeId(model=self, key=key, name=name)
            # update the node metadata
            self._metadata[key] = self.info(key=key, name=name, split=split)
        # if it's there
        else:
            # replace it
            node.replace(old)

        # either way, update the model
        self._nodes[key] = node

        # all done
        return key, node


    def getInfo(self, key):
        """
        Retrieve the metadata of the node registered under {key}
        """
        # look it up in my info map
        return self._metadata[key]


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
        # look it up in my info map
        return self._metadata[key].name


    def getSplitName(self, key):
        """
        Retrieve the sequence of fragments in the name of the node registered under {key}
        """
        # look it up in my info map
        return self._metadata[key].split


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
            # fill out the node id
            name, split, key = self.info.fillNodeId(model=self, key=key, name=name)
            # add it to the pile
            self._nodes[key] = node
            self._metadata[key] = self.info(key=key, name=name, split=split)
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
        return self.separator.join(filter(None, levels))


    # meta-methods
    def __init__(self, separator=separator, **kwds):
        # chain up
        super().__init__(**kwds)
        # record my separator
        self.separator = separator
        # initialize my name hash
        self._hash = patterns.newPathHash()
        # and the node metadata
        self._metadata = {}
        # all done
        return


    def __contains__(self, name):
        """
        Check whether {item} is present in the table
        """
        # check whether the hashed name is present in my node index
        return self.hash(name) in self._nodes


    def __setitem__(self, name, value):
        """
        Convert {value} into a node and update the model
        """
        # hash the name
        key = self.hash(name)
        # delegate
        return self.insert(name=name, key=key, value=value)


    # implementation details
    # private data
    _hash = None
    _info = None


    # aliasing
    def replaceCanonical(self, key, target, alias, aliasNode, aliasInfo):
        """
        Replace the canonical node under {target} with the associated information from {alias}
        """
        # replace the node
        self._nodes[key] = aliasNode
        # adjust its metadata
        aliasInfo.key = key
        aliasInfo.name = target
        # and register it under its new key
        self._metadata[key] = aliasInfo
        # all done
        return


    def resolveAliasingConflict(self,
              key, target, alias, targetNode, targetInfo, aliasNode, aliasInfo):
        # i don't know what to do
        raise self.AliasingError(
            key=key, target=target, alias=alias,
            targetNode=targetNode, targetInfo=targetInfo, aliasNode=aliasNode, aliasInfo=aliasInfo)


    # debug support
    def dump(self, pattern=''):
        """
        List my contents
        """
        print("model {}:".format(self))
        print("  nodes:")
        for info, node in self.find(pattern):
            node.dump(indent=' '*4, name=info.name)
            print("      slot: {}".format(type(node).__name__))
        return


# end of file
