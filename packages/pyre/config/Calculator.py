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


    # interface
    def configureComponentClass(self, executive, component):
        """
        Initialize the component class inventory by making the descriptors point to the
        evaluation nodes
        """
        # access the locator factories
        import pyre.tracking
        # build a locator for values that come from trait defaults
        locator = pyre.tracking.newSimpleLocator(source="<defaults>")
        # get the class inventory
        inventory = component._pyre_Inventory
        # get the component family
        family = component._pyre_family

        # iterate over all the properties, both local and inherited
        for trait,source in component.pyre_traits(categories=component._pyre_CONFIGURABLE_TRAITS):
            # if the component declared a family, build the node key out of the component
            # family and the trait name
            key = self.TRAIT_SEPARATOR.join([family, trait.name]) if family else ''
            # check whether a configuration node is available
            try:
                node = self.findNode(key)
            except KeyError:
                # not there; build one
                # for locally declared properties, just make a new binding
                if source == component:
                    node = self.bind(
                        key.split(self.TRAIT_SEPARATOR),
                        trait.default, locator, 
                        priority=(executive.PACKAGE_CONFIGURATION, -1))
                # otherwise, it is an inherited property
                else:
                    # get the configuration node that corresponds to this inherited trait
                    # this can't fail since the ancestor has been through this process already
                    referent = getattr(source._pyre_Inventory, trait.name)
                    # build a reference to it
                    node = referent.newReference(priority=(executive.PACKAGE_CONFIGURATION, -1))
                    # register the reference
                    if key:
                        self.registerNode(name=key, node=node)

            # now, attach the node as an inventory attribute named after the trait
            setattr(inventory, trait.name, node)
            # process the trait aliases
            for alias in trait.aliases:
                print("{0._pyre_family}.{1.name}: alias {2!r}".format(component, trait, alias))
                # build the alias key out of the component family and the trait name
                aliasKey = self.TRAIT_SEPARATOR.join([family, alias]) if family else ''
                try:
                    other = self.findNode(aliasKey)
                except KeyError:
                    # no previous configuration under an alias
                    print(" --- alias {!r} not seen previously".format(aliasKey))
                    if key and aliasKey:
                        self._hash.alias(
                            alias=aliasKey, original=key, separator=self.TRAIT_SEPARATOR)
                    continue

                print(" --- found aliased node")
                print(" --- canonical.name={0!r}, alias.name={1!r}".format(key, aliasKey))
                print(" --- canonical.value={0.value!r}, alias.value={1.value!r}".format(node, other))
                print(" --- canonical.priority={0.priority!r}, alias.priority={1.priority!r}".format(node, other))
                # check whether we should 
                if node.priority < other.priority:
                    print(" --- alias is higher priority")
                    node.value = other.value
                    # node.evaluator = other.evaluator
                    node.priority = other.priority

                node._observers |= other._observers
                for client in other._observers:
                    client._replace(old=other, new=node)
                if key and aliasKey:
                    hashKey = self._hash.hash(aliasKey, separator=self.TRAIT_SEPARATOR)
                    del self._nodes[hashKey]
                    del self._names[hashKey]
                    self._hash.alias(
                        alias=aliasKey, original=key, separator=self.TRAIT_SEPARATOR)

        # all done
        return component


    def configureComponentInstance(self, executive, component):
        """
        Initialize the component instance inventory by making the descriptors point to the
        evaluation nodes
        """
        # get the component's name
        # name = component._pyre_name
        name = self.FAMILY_SEPARATOR.join(
            tag for tag in [component._pyre_family, component._pyre_name] if tag)
        # get the component's inventory
        inventory = component._pyre_inventory
        # iterate over my traits
        for trait, ancestor in component.pyre_traits(categories={"properties"}):
            # create the node key
            key = self.TRAIT_SEPARATOR.join([name, trait.name])
            # check whether there is an existing configuration node by this name
            try:
                node = self.findNode(key)
            except KeyError:
                # grab the trait node from the class record
                # this is guaranteed to succeed since the class record has been through this
                # process already
                default = getattr(inventory, trait.name)
                # create a reference to it
                node = default.newReference()
                # and register the new node
                self.registerNode(name=key, node=node)
            # and add it to the inventory
            setattr(inventory, trait.name, node)

        # all done; hand the component back
        return component


    def bind(self, key, value, locator, priority):
        """
        Bind the variable {name} to {value}.

        If there is no existing variable by this name, build one and register it with the
        model. Otherwise, just update the existing node. The contents of {value} can refer to
        other variables in the model by following the rules in pyre.calc.Expression, and may
        make certain calls to the python runtime. The exact details are being worked out...
        """
        # make sure not to bail out when {name} is empty; nameless traits still need a Variable
        # built for them, since subclasses access them
        name = self.TRAIT_SEPARATOR.join(key)
        print("Calculator.bind: {0!r} <- {1!r} with priority {2}".format(name, value, priority))
        # check whether we have seen this variable before
        try:
            node = self.findNode(name)
        except KeyError:
            # if not, build one
            print(" --- first time for {!r}; building a new node".format(name))
            node = Variable(value=None, evaluator=None)
            # and register it if a name was given
            if name:
                self.registerNode(name=name, node=node)
        # if the existing node has higher priority
               
        print(" --- checking priority: current={}, binding={}".format(node.priority, priority))
        if node.priority > priority:
            # leave it alone
            print(" --- existing node has higher priority; bailing out")
            return node

        # set the new node proority
        node.priority = priority
        # print("NYI: literal/macro/function interpretation of trait value")
        # build an evaluator
        # figure out if this value contains references to other nodes
        if value and isinstance(value, str) and Expression._scanner.match(value):
            evaluator = Expression(expression=value, model=self)
            value = None
        else:
            evaluator = None

        # figure where to attach the evaluator
        if evaluator:
            node.evaluator = evaluator
        else:
            node.value = value

        # log the event
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


# end of file 
