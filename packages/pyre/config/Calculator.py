# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import pyre.patterns
import pyre.tracking
from ..calc.AbstractModel import AbstractModel

from .Variable import Variable
from ..calc.Expression import Expression


class Calculator(AbstractModel):
    """
    The keeper of all configurable values maintained by the framework

    It is implemented as pyre.calc.AbstractModel
    """


    # constants
    TRAIT_SEPARATOR = '.'
    FAMILY_SEPARATOR = '#'
    DEFAULT_PRIORITY = (-1, -1)

    # build a locator for values that come from trait defaults
    locator = pyre.tracking.newSimpleLocator(source="<defaults>")

    # interface
    def configureComponentClass(self, executive, component):
        """
        Initialize the component class inventory by making the descriptors point to the
        evaluation nodes
        """
        # get the class inventory
        inventory = component._pyre_Inventory
        # get the component family; it has already been split on '.' at construction
        family = component._pyre_family
        # checkpoint
        # print("Calculator.configureComponentClass: configuring {!r}, family={!r}".format(
                # component.__name__, family))
        # iterate over all the properties, both own and inherited
        for trait, source in component.pyre_traits(categories=component._pyre_CONFIGURABLE_TRAITS):
            # build the authoritative node for this trait
            # if this is a trait declared by this component
            if source == component:
                # print("  trait: {.name!r}, one of mine".format(trait))
                # establish a default value with the lowest possible priority
                node = Variable(value=trait.default, evaluator=None)
            # otherwise, build a reference to the ancestor's node
            else:
                # print("  trait: {.name!r}, inherited from {.__name__!r}".format(trait, source))
                # get the configuration node that corresponds to this inherited trait
                # this can't fail since the ancestor has been through this process already
                referent = getattr(source._pyre_Inventory, trait.name)
                # build a reference to it
                # NYI: with what priority? this is correct by accident...
                node = referent.newReference()
            # attach the node as an inventory attribute named after the trait
            setattr(inventory, trait.name, node)
            # if this component class did not declare a family we are done configuring this trait
            if not family: continue
            # build the canonical name of this node
            canonical = self.TRAIT_SEPARATOR.join(family + [trait.name])
            # otherwise, look through the model for configurations for this trait
            for alias in trait.aliases:
                # print("    alias: {!r}".format(alias))
                # form the name of the potential node
                key = self.TRAIT_SEPARATOR.join(family + [alias])
                # look for the node
                # print("      looking for {!r}".format(key))
                try:
                    existing = self.findNode(key)
                # if not there
                except KeyError:
                    # print("        no such configuration node")
                    # move on to the next alias
                    continue
                # if the node is there
                else:
                    # print("      removing the existing configuration node")
                    # clean up the model
                    aliasHash = self._hash.hash(key, separator=self.TRAIT_SEPARATOR)
                    del self._nodes[aliasHash]
                    del self._names[aliasHash]
                # either way,  make sure we register this alias with the hash table
                # must be done after the call to findNode, otherwise aliasing will make the
                # node incaccessible
                finally:
                    # print("      aliasing {!r} to {!r}".format(key, canonical))
                    self._hash.alias(alias=key, original=canonical, separator=self.TRAIT_SEPARATOR)
                # print("      processing setting: {!r} <- {!r}".format(alias, existing.value))
                node.replace(other=existing, alias=key)
            # finally, register the node with the model
            # this must be done after the potential name clash has been prevented by removing all
            # nodes that may be aliases of this one
            self.registerNode(name=canonical, node=node)
            # and log the event
            self._tracker.track(key=node, value=(trait.default, self.locator))

        # all done
        return component


    def configureComponentInstance(self, executive, component):
        """
        Initialize the component instance inventory by making the descriptors point to the
        evaluation nodes
        """
        # get the component's family
        family = self.TRAIT_SEPARATOR.join(component._pyre_family)
        # build the component's name
        name = component._pyre_name
        # build the fully qualified name
        fqname = self.FAMILY_SEPARATOR.join(tag for tag in [family,name] if tag)
        # get the component's inventory
        inventory = component._pyre_inventory
        # checkpoint
        # print("Calculator.configureComponentInstance: configuring {!r}, family={!r}".format(
                # component._pyre_name, family))
        # iterate over my traits
        for trait, source in component.pyre_traits(categories=component._pyre_CONFIGURABLE_TRAITS):
            # get the node that holds the class default value
            default = getattr(inventory, trait.name)
            # build the authoritative node for this trait
            node = default.newReference()
            # and its canonical name
            canonical = self.TRAIT_SEPARATOR.join([name, trait.name])
            # now look for confingurations for this trait
            for alias in trait.aliases:
                # print("    alias: {!r}".format(alias))
                # form the name of the potential node
                # first the unqualified name
                uqKey = self.TRAIT_SEPARATOR.join([name, alias])
                # and now the fully qualified name
                fqKey = self.TRAIT_SEPARATOR.join([fqname, alias])
                # for either of these names
                for key in [fqKey, uqKey]:
                    # look for the node
                    # print("      looking for {!r}".format(key))
                    try:
                        existing = self.findNode(key)
                    # if not there
                    except KeyError:
                        # print("      no such configuration node")
                        continue
                    # if the node is there
                    else:
                        # print("      removing the existing configuration node")
                        # clean up the model
                        aliasHash = self._hash.hash(key, separator=self.TRAIT_SEPARATOR)
                        del self._nodes[aliasHash]
                        del self._names[aliasHash]
                    # either way, make sure we register this alias with the has table
                    finally:
                        # print("      aliasing {!r} to {!r}".format(key, canonical))
                        self._hash.alias(
                            alias=key, original=canonical, separator=self.TRAIT_SEPARATOR)
                    # print("      processing setting: {!r} <- {!r}".format(alias, existing.value))
                    node.replace(other=existing, alias=key)
            # finally, attach the node as an inventory attribute named after the trait
            setattr(inventory, trait.name, node)
            # register it with the model
            self.registerNode(name=canonical, node=node)
        # all done; hand the component back
        return component


    def bind(self, key, value, locator, priority):
        """
        Construct a node to hold {value} and register it with the model under a name derived
        from {key}

        If there is no existing variable by this name, build one and register it with the
        model. Otherwise, just update the existing node. The contents of {value} can refer to
        other variables in the model by following the rules in pyre.calc.Expression, and may
        make certain calls to the python runtime. The exact details are being worked out...
        """
        # make sure not to bail out when {name} is empty; nameless traits still need a Variable
        # built for them, since subclasses access them
        name = self.TRAIT_SEPARATOR.join(key)
        # print("Calculator.bind: {0!r} <- {1!r} with priority {2}".format(name, value, priority))
        # check whether we have seen this variable before
        try:
            node = self.findNode(name)
        except KeyError:
            # if not, build one
            # print("  first time for {!r}; building a new node".format(name))
            node = Variable(value=None, evaluator=None)
            # and register it if a name was given
            if name:
                self.registerNode(name=name, node=node)
        # if the existing node has higher priority
               
        # print("  checking priority: current={}, binding={}".format(node.priority, priority))
        if node.priority > priority:
            # leave it alone
            # print("  existing node has higher priority; skipping")
            return node
        # print("  existing node has lower priority; assigning new value")

        # set the new node priority
        node.priority = priority
        # and let the variable deal with the value processing
        node.value = value

        # log the event
        # NYI: this is broken and needs fixin'
        self._tracker.track(key=node, value=(value, locator))

        # return the node
        return node


    # interface obligations from the abstract base class
    def addNode(self, name, node):
        """
        Implementation details of the mechanism for node insertion in the model: associate
        {node} with {name} and insert into the model

        If you are looking to insert a node in the model, please use 'registerNode',
        which is a lot smarter and takes care of patching unresolved names.
        """
        # hash the name
        key = self._hash.hash(name, separator=self.TRAIT_SEPARATOR)
        # add the node the node store
        self._nodes[key] = node
        # add the name to the name store
        self._names[key] = name
        # all done
        return


    def findNode(self, name):
        """
        Locate the node in the model that matches {name}.
        """
        return self._nodes[self._hash.hash(name, separator=self.TRAIT_SEPARATOR)]
        

    def getNodes(self):
        """
        Iterate over the nodes in my graph.

        This is expected to return a sequence of ({name}, {node}) tuples, regardless of the
        node storage details implemented by AbstractModel descendants
        """
        # for each of my registered nodes
        for key, node in self._nodes.items():
            # look up the associated name and yield the required value
            yield self._names[key], node
        # all done
        return


    # meta methods
    def __init__(self, name=None, **kwds):
        name = name if name is not None else "pyre.evaluator"
        super().__init__(name=name, **kwds)

        # model evaluation support
        self._names = {}
        self._nodes = {}
        self._hash = pyre.patterns.newPathhash()

        # history tracking
        self._tracker = pyre.tracking.newTracker()

        return


    def __setitem__(self, name, value):
        self.bind(key=[name], value=value, locator=self.locator, priority=self.DEFAULT_PRIORITY)
        return


# end of file 
