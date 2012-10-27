# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# superclass
from .Facility import Facility


# declaration
class Map(Facility):
    """
    Dictionary of properties
    """


    # value coercion
    def coerce(self, node, value, **kwds):
        """
        A no-op to get around the class inventory constraints
        """
        return value


    def instantiate(self, configurable, node, value, **kwds):
        """
        Attach a component catalog as my trait value
        """
        # initialize the component index, a {dict} for now; it's not useful to remember the
        # order in which these settings were encountered, because what you really want is a
        # container sorted by the priorities of the settings
        index = dict()
        # get my target key
        key = node.key
        # if it unregistered
        if not key:
            # nothing to do
            return index

        # the executive
        executive = self.executive
        # the nameserver
        nameserver = executive.nameserver
        # and the configurator
        configurator = executive.configurator

        _, slotName = nameserver.lookup(node.key)

        # go through the children of this key
        for childKey, childNode in nameserver.children(key):
            # look up the name of the node
            _, childName = nameserver.lookup(childKey)
            # take it apart and keep the trailing part
            tag = nameserver.split(childName)[-1]
            # store the (tag, value) pair in my index
            index[tag] = self.schema.coerce(value=childNode.value)

        # now, for the deferred assignments
        for assignment, priority in configurator.deferred[key]:
            # for each condition
            for name, family in assignment.conditions:
                # hash them
                name = nameserver.hash(name)
                family = nameserver.hash(family)
                # get the class record of the referenced component
                target = type(nameserver[name])
                # verify
                if target.pyre_inventory.key is not family: break
            # if they all passed
            else:
                # get the name of this entry
                tag = nameserver.join(*assignment.key)
                # place it in the index
                index[tag] = self.schema.coerce(value=assignment.value)

        # store the index as my value
        return index


    # framework support
    def initialize(self, configurable, **kwds):
        # chain up
        super().initialize(configurable=configurable, **kwds)
        # all i care about is access to the executive
        self.executive = configurable.pyre_executive
        # all done
        return


    # support for constructing instance slots
    def macro(self, model):
        """
        Return my choice of macro evaluator so the caller can build appropriate slots
        """
        # my schema knows...
        return self.schema.macro(model=model)


    # meta-methods
    def __init__(self, schema, **kwds):
        super().__init__(protocol=schema(), default=schema.default, **kwds)
        return


# end of file 
