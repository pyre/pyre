# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import weakref
import collections
import pyre.patterns
import pyre.tracking

from ..calc.AbstractModel import AbstractModel


class Configurator(AbstractModel):
    """
    The keeper of all configurable values maintained by the framework

    This class is a pyre.calc.AbstractModel that maintains the global configuration state of
    the framework. All configuration events encountered are processed by a Configurator
    instance held by the pyre executive and become nodes in the configuration model.
    """


    # constants
    TRAIT_SEPARATOR = '.'
    FAMILY_SEPARATOR = '#'
    DEFAULT_PRIORITY = (-1, -1)
    EXPLICIT_CONFIGURATION = (15, -1) # programmatic overrides


    # types
    from .Slot import Slot


    # public data
    counter = None # the event priority counter
    tracker = None # the node value history tracker
    # build a locator for values that come from trait defaults
    locator = pyre.tracking.newSimpleLocator(source="<defaults>")


    # interface
    def configure(self, configuration, priority):
        """
        Iterate over the {configuration} events and insert them into the model at the given
        {priority} level
        """
        # loop over events
        for event in configuration.events:
            # build the event sequence number, which becomes its priority level
            seq = (priority, self.counter[priority])
            # update the counter
            self.counter[priority] += 1
            # and process the event
            event.identify(inspector=self, priority=seq)
        # all done
        return
 

    # configuration event processing
    def bind(self, key, value, locator=None, priority=DEFAULT_PRIORITY, **kwds):
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
        # run the value through the Slot recognizer
        evaluator = self.Slot.recognize(value=value, configuration=self)
        # print("Calculator.bind: {0!r} <- {1!r} with priority {2}".format(name, value, priority))
        # check whether we have seen this variable before
        try:
            node = self.findNode(name)
        except KeyError:
            # if not, build one
            # print("  first time for {!r}; building a new node".format(name))
            node = self.Slot(value=None, evaluator=evaluator, priority=priority)
            # and register it if a name was given
            if name:
                self.registerNode(name=name, node=node)
        else:
            # hand the information to the existing node and let it decide what to do
            node.assign(value=None, evaluator=evaluator, priority=priority)

        # log the event
        # NYI: this is broken and needs fixin'
        self.tracker.track(key=node, value=(value, locator))

        # return the node
        return node


    def loadConfiguration(self, source, locator, **kwds):
        """
        Ask the pyre {executive} to load the configuration settings in {source}
        """
        # get the executive to kick start the configuration loading
        self.executive.loadConfiguration(uri=source, locator=locator)
        # and return
        return self


    # framework requests
    def configureComponentClass(self, component):
        """
        Look through the configuration store for nodes that correspond to defaults for the
        traits of the given {component} class and configure them
        """
        # get the class inventory
        inventory = component.pyre_inventory
        # get the class family
        family = component.pyre_family
        # if there is no family name we are done
        if not family: return self
        # print("Calculator.configureComponentClass: configuring {!r}, family={!r}".format(
                # component.pyre_name, family))
        # iterate over all traits, both own and inherited
        for trait in component.pyre_getTraitDescriptors():
            # if this is not configurable trait, skip it
            if not trait.pyre_isConfigurable: continue
            # find the inventory node that corresponds to this trait
            node = inventory[trait]
            # build the canonical name of the trait
            canonical = self.TRAIT_SEPARATOR.join(family + [trait.name])
            # print("  trait: name={!r}, canonical={!r}".format(trait.name, canonical))
            # iterate over all possible names of this trait
            for alias in trait.aliases:
                # print("    alias: {!r}".format(alias))
                # build the key for the target node
                key = self.TRAIT_SEPARATOR.join(family + [alias])
                # print("      looking for {!r}".format(key))
                # look for the matching node
                try:
                    existing = self.findNode(key)
                # if there is no match
                except KeyError:
                    # print("        no such configuration node")
                    # move on to the next node
                    continue # but after the finally clause below!
                # if there is a match
                else:
                    # print("      removing the existing configuration node")
                    # clean up the model by removing the aliased node
                    # the actual value transfer will happen through the call to replace below
                    aliasHash = self._hash.hash(key, separator=self.TRAIT_SEPARATOR)
                    del self._nodes[aliasHash]
                    del self._names[aliasHash]
                # either way, make sure we register this alias with the hash table
                # must be done after the call to findNode, otherwise aliasing will make the
                # node inaccessible
                finally:
                    # print("      aliasing {!r} to {!r}".format(key, canonical))
                    self._hash.alias(alias=key, original=canonical, separator=self.TRAIT_SEPARATOR)
                # print("      processing setting: {!r} <- {!r}".format(alias, existing.value))
                node.replace(other=existing)
            # finally, register the node with the model
            # this must be done after the potential name clash has been prevented by removing all
            # nodes that may be aliases of this one
            self.registerNode(name=canonical, node=node)
            # and log the event
            self.tracker.track(key=node, value=(trait.default, self.locator))

        # all done
        return component


    def configureComponentInstance(self, component):
        """
        Initialize the component instance inventory by making the descriptors point to the
        evaluation nodes
        """
        # get the component's family
        family = self.TRAIT_SEPARATOR.join(component.pyre_family)
        # build the component's name
        name = component.pyre_name
        # build the fully qualified name
        fqname = self.FAMILY_SEPARATOR.join(tag for tag in [family,name] if tag)
        # get the component's inventory
        inventory = component.pyre_inventory
        # checkpoint
        # print("Configurator.configureComponentInstance: configuring {!r}, family={!r}".format(
                # component.pyre_name, family))
        # print("  inventory:", inventory)
        # iterate over my traits
        for trait in component.pyre_getTraitDescriptors():
            # skip non-configurable traits
            if not trait.pyre_isConfigurable:
                continue
            # get the node that holds the class default value
            default = component.__class__.pyre_inventory[trait]
            # and its canonical name
            canonical = self.TRAIT_SEPARATOR.join([name, trait.name])
            # print("  trait: name={!r}, canonical={!r}".format(trait.name, canonical))
            # build the authoritative node for this trait
            node = default.newReference()
            # now look for configurations for this trait
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
                    node.replace(other=existing)
            # finally, attach the node as an inventory attribute named after the trait
            inventory[trait] = node
            # register it with the model
            self.registerNode(name=canonical, node=node)
        # all done; hand the component back
        return component


    # convenience
    def validateNode(self, node):
        """
        Verify that {node} contains no circular references

        N.B.: there is also AbstractModel.validate that checks the entire set of nodes
        """
        # remove the node from the known good set
        self._clean.discard(node)
        # traverse the subgraph rooted att his node
        node.validate(clean=self._clean)
        # all is good if no eception was thrown
        return node


    # interface obligations from pyre.calc.AbstractModel
    def addNode(self, name, node):
        """
        Implementation details of the node insertion mechanism: associate {node} with {name}
        and insert it in the model

        If you are looking for a way to insert a node in the model, please use 'registerNode';
        it is a lot smarter and takes care of patching unresolved names
        """
        # hash the name
        key = self._hash.hash(name, separator=self.TRAIT_SEPARATOR)
        # add the node to the node store
        self._nodes[key] = node
        # add the name to the name store
        self._names[key] = name
        # all done
        return


    def findNode(self, name):
        """
        Lookup the model node that is associated with {name}
        """
        return self._nodes[self._hash.hash(name, separator=self.TRAIT_SEPARATOR)]


    def getNodes(self):
        """
        Iterate over the nodes in my graph

        This is expected to return a sequence of ({name}, {node}) tuples, regardles of the node
        storage details implemented by AbstractModel subclasses
        """
        # for each of my registered nodes
        for key in self._nodes.keys():
            # look up the associated name and yield the required value
            yield self._names[key], self._nodes[key]
        # all done
        return


    # meta methods
    def __init__(self, executive, name=None, **kwds):
        name = name if name is not None else "pyre.configurator"
        super().__init__(name=name, **kwds)

        # record the executive
        self.executive = weakref.proxy(executive)

        # model evaluation support
        self._names = {}
        self._nodes = {}
        self._hash = pyre.patterns.newPathHash()

        # the model nodes that are known to be in good state
        self._clean = set()

        # history tracking
        self.tracker = pyre.tracking.newTracker()

        # and the event priority counter
        self.counter = collections.Counter()

        return


    # subscripted access
    def __setitem__(self, key, value):
        """
        Associate {key} with {value} in the configuration store through an explicit assignment
        """
        # let bind do the hard work
        # all we have to do is prepare the key and make up a priority and a locator
        self.bind(
            key=key.split(self.TRAIT_SEPARATOR), value=value,
            priority = self.EXPLICIT_CONFIGURATION,
            locator=pyre.tracking.here(level=1),
            )
        return


    # debugging support
    def _dump(self, pattern=None):
        """
        List my contents
        """
        # build the node name recognizer
        import re
        regex = re.compile(pattern if pattern else '')

        print("model {0!r}:".format(self.name))
        for name, node in sorted(self.getNodes()):
            if regex.match(name):
                print("  {0!r} <- {1!r}".format(name, node.value))
                for value, location in self.tracker.getHistory(node):
                    print("   >> {!r} from {}".format(value, location))
                
        return


# end of file 
