# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# supporting packages
import weakref
import itertools
import collections
import pyre.tracking
import pyre.patterns


# base class
from ..algebraic.Hierarchical import Hierarchical


class Model(Hierarchical):
    """
    A specialization of a hierarchical model that takes into account that the model nodes have
    priorities attached to them and cannot indiscriminately replace each other
    """


    # constants
    from .levels import DEFAULT_CONFIGURATION, EXPLICIT_CONFIGURATION


    # types
    from .Slot import Slot as node


    # public data
    counter = None # the event priority counter
    separator = '.' # the level separator in the node names
    # build a locator for values that come from trait defaults
    locator = pyre.tracking.newSimpleLocator(source="<defaults>")


    # interface for my configurator
    def default(self, key, value):
        """
        Build a new slot with {value}

        This is called during the component trait initialization to establish the default value
        of a trait.
        """
        # build special {priority} and {locator}, and delegate to {assign}
        return self.assign(
            key=key, value=value,
            priority=self.collate(category=self.DEFAULT_CONFIGURATION),
            locator=self.locator)


    # configuration event processing
    def assign(self, key, value, priority, locator=None):
        """
        Build a node with the given {priority} to hold {value}, and register it under {key}
        """
        # dump
        # print("Model.assign:")
        # print("    key={}, value={!r}".format(key, value))
        # print("    from {}".format(locator))
        # print("    with priority {}".format(priority))
        # build the slot name
        name = self.separator.join(key)
        # get the existing slot
        existing, hashkey = self._retrieveNode(key=key, name=name)

        # convert the value into a node
        node = self._recognize(value)
        # adjust the meta data
        node.key = hashkey
        node.name = name
        node.locator = locator
        node.priority = priority
        # if this is one of the nodes I care about
        if key:
            # add me as an observer
            node.addObserver(self)

        # adjust the value
        node = existing.setValue(value=node)
        # all done
        return node


    def defer(self, assignment, priority):
        """
        Build a node that corresponds to a conditional configuration
        """
        # dump
        # print("Model.defer:")
        # print("    component={0.component}".format(assignment))
        # print("    conditions={0.conditions}".format(assignment))
        # print("    key={0.key}, value={0.value!r}".format(assignment))
        # print("    from {0.locator}".format(assignment))
        # print("    with priority {}".format(priority))

        # hash the component name
        ckey = self._hash.hash(assignment.component)
        # get the deferred event store and add the assignment to the pile
        self.deferred[ckey].append(assignment)
        # all done
        return self


    def execute(self, command, priority, locator):
        """
        Record a request to execute a command
        """
        # record the command and its context
        self.commands.append((priority, command, locator))
        # all done
        return self


    def load(self, source, locator, **kwds):
        """
        Ask the pyre {executive} to load the configuration settings in {source}
        """
        # get the executive to kick start the configuration loading
        self.executive.loadConfiguration(uri=source, locator=locator)
        # and return
        return self


    def collate(self, category=None):
        """
        Build a collation index for the next event in {category}
        """
        # adjust the optional input
        category = category if category is not None else self.EXPLICIT_CONFIGURATION
        # build and return the collation sequence
        return (category, next(self.counter[category]))


    # obligations as an observer of nodes
    def pyre_updatedDependent(self, node):
        """
        Handler invoked when one of my dependents changes value
        """
        # ignore it
        return


    def pyre_substituteDependent(self, current, replacement, clean=None):
        """
        Replace {current} with {replacement} in my node index
        """
        # get the hashkeys
        chash = current.key
        rhash = replacement.key
        assert chash == rhash
        
        # if the current node was registered
        if chash in self._nodes:
            # replace the existing slot with the new one
            self._nodes[chash] = replacement

        # and return
        return


    # meta methods
    def __init__(self, executive, **kwds):
        super().__init__(**kwds)

        # the event priority counter
        self.counter = collections.defaultdict(itertools.count)

        # record the executive
        self.executive = weakref.proxy(executive)
        # the list of command requests
        self.commands = []
        # the database of deferred bindings
        self.deferred = collections.defaultdict(list)
        # the configurables that manage their own namespace
        self.configurables = weakref.WeakValueDictionary()

        # name hashing strategy
        self._hash = pyre.patterns.newPathHash()

        # done
        return


    def __setitem__(self, name, value):
        """
        Add/update the named configuration setting with the given value
        """
        # print("Model: setting {!r} <- {!r}".format(name, value))
        # build the key
        key = name.split(self.separator)
        # set the priority
        priority = self.collate(category=self.EXPLICIT_CONFIGURATION)
        # build a locator for the source of the assignment
        locator = pyre.tracking.here(level=1)
        # make the assignment
        return self.assign(key=key, value=value, priority=priority, locator=locator)


    # implementation details
    def _buildPlaceholder(self, name, identifier, **kwds):
        """
        Build an unresolved node as a place holder for new requests
        """
        # make the node
        node = self.node.unresolved(name=name, key=identifier, request=name)
        # add me as its observer
        node.addObserver(self)
        # and return it
        return node
        

    # debugging support
    def dump(self, pattern=''):
        """
        List my nodes
        """
        print("model {0!r}:".format(self.name))
        print("  nodes:")
        for name, slot in self.select(pattern):
            try: 
                value = slot.value
            except self.UnresolvedNodeError:
                value = "unresolved"
            print("    {!r} <- {!r}".format(name, value))
            print("        from {}".format(slot.locator))

        if self.configurables:
            print("  configurables:")
            for name in self.configurables:
                print("    {!r}".format(name))

        return


# end of file 
