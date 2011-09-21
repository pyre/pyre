# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import weakref
import collections
from pyre.calc.HierarchicalModel import HierarchicalModel


class Model(HierarchicalModel):
    """
    A specialization of a hierarchical model that takes into account that the model nodes have
    priorities attached to them and cannot indiscriminately replace each other
    """


    # constants
    DEFAULT_PRIORITY = (-1, -1)


    # interface for my configurator
    # configuration event processing
    def bind(self, key, value, priority=None, locator=None):
        """
        Build a node with the given {priority} to hold {value}, and register it under {key}
        """
        # dump
        # print("Model.bind:")
        # print("    key={}, value={!r}".format(key, value))
        # print("    from {}".format(locator))
        # print("    with priority {}".format(priority))
        # build the slot name
        name = self.separator.join(key)
        # adjust the priority, if necessary
        if priority is None:
            # get the priority sequence class for explicit settings
            explicit = self.executive.EXPLICIT_CONFIGURATION
            # build the event sequence number, which becomes its priority level
            priority = (explicit, self.counter[explicit])
            # update the counter
            self.counter[explicit] += 1
        # if the priority of this assignment is less that the current priority
        if priority <  self.priorities.get(name, self.DEFAULT_PRIORITY):
            # ignore the request
            return
        # otherwise, adjust the priority
        self.priorities[name] = priority
        # make the assignment
        self[name] = value
        # and return


    def defer(self, assignment, priority):
        """
        Build a node that corresponds to a conditional configuration
        """
        # print("Model.defer:")
        # print("    component={}".format(component))
        # print("    conditions={}".format(conditions))
        # print("    key={}, value={!r}".format(key, value))
        # print("    from {}".format(locator))
        # print("    with priority {}".format(priority))
        # hash the component name
        ckey = self._hash.hash(assignment.component)
        # build a slot
        slot = self.nodeFactory(
            value=None, 
            evaluator=self.recognize(value=assignment.value),
            priority=priority, locator=assignment.locator)

        # get the deferred event store and add the event and the slot to the pile
        self.deferred[ckey].append( (assignment, slot) )

        # all done
        return slot


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


    # meta methods
    def __init__(self, executive, **kwds):
        super().__init__(**kwds)

        # record the executive
        self.executive = weakref.proxy(executive)
        # the list of command requests
        self.commands = []
        # the database of deferred bindings
        self.deferred = collections.defaultdict(list)
        # the configurables that manage their own namespace
        self.configurables = weakref.WeakValueDictionary()
        # the priority table
        self.priorities = {}
        # the event priority counter
        self.counter = collections.Counter()

        # done
        return


    def dump(self, pattern=''):
        super().dump(pattern)
        if self.configurables:
            print("  configurables:")
            for name in self.configurables:
                print("    {!r}".format(name))
        return


# end of file 
