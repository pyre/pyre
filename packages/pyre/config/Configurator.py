# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


# externals
import weakref # for access to my executive
import collections # for defaultdict
from .. import tracking


# class declaration
class Configurator:
    """
    The manager of the configuration store
    """


    # types
    from . import events
    from . import exceptions

    # constants
    locator = tracking.simple('during pyre startup') # the default locator

    # public data
    codecs = None


    # interface
    def loadConfiguration(self, uri, source, locator, priority):
        """
        Use {uri} to find a codec that can process {source} into a stream of configuration
        events
        """
        # record the attempt to load this configuration
        self.sources.append((uri, priority))

        # initialize the pile of encountered errors
        errors = []
        # get the address
        address = uri.address
        # deduce the encoding
        encoding = address[address.rfind('.')+1:]
        # attempt to
        try:
            # find the appropriate reader
            reader = self.codecs[encoding]
        # if not there
        except KeyError:
            # build an error indicator
            error = self.exceptions.UnknownEncodingError(
                uri=uri, encoding=encoding, locator=locator)
            # add it to my pile
            errors.append(error)
            # and get out of here
            return errors

        # convert the input source into a stream of events
        events = reader.decode(uri, source, locator)
        # process it
        errors.extend(self.processEvents(events=events, priority=priority))
        # and return the errors
        return errors


    # access to codecs
    def codec(self, encoding):
        """
        Retrieve the codec associated with the given {encoding}
        """
        # easy enough
        return self.codecs[encoding]


    def register(self, codec):
        """
        Add {codec} to my registry
        """
        # easy enough
        self.codecs[codec.encoding] = codec
        # all done
        return


    def encodings(self):
        """
        Return the registered encodings
        """
        # easy enough
        return self.codecs.keys()


    # event processing
    def processEvents(self, events, priority):
        """
        Iterate over the {configuration} events and insert them into the model at the given
        {priority} level
        """
        # error accumulator
        errors = []
        # loop over events
        for event in events:
            # process the event
            # print("pyre.config.Configurator.configure:", event)
            event.identify(inspector=self, priority=priority)
        # all done
        return errors


    def assign(self, assignment, priority):
        """
        Process {assignment} by building a slot and placing it in the nameserver
        """
        # get the key
        split = assignment.key
        # unpack the value
        value = assignment.value
        # get the locator
        locator = assignment.locator
        # instantiate a priority ranking
        priority = priority()

        # get the model
        nameserver = self.executive.nameserver
        # insert the value in the model
        key, _, _ = nameserver.insert(split=split, value=value, locator=locator, priority=priority)
        # and return the associated key
        return key


    def defer(self, assignment, priority):
        """
        Process a conditional assignment
        """
        # build the key
        key = self.executive.nameserver.hash(name=assignment.component)
        # compute the priority
        priority = priority()
        # add it to the pile
        self.deferred[key].append((assignment, priority))

        # dump
        # print("Configurator.defer:")
        # print("    component={0.component}".format(assignment))
        # print("    conditions={0.conditions}".format(assignment))
        # print("    key={0.key}, value={0.value!r}".format(assignment))
        # print("    from {0.locator}".format(assignment))
        # print("    with priority {}".format(priority))

        # all done
        return self


    def execute(self, command, priority):
        """
        Record a request to execute a command
        """
        # adjust the command priority
        command.priority = priority()
        # record the command and its context
        self.commands.append(command)
        # all done
        return self


    def load(self, request, priority):
        """
        Ask the pyre executive to load the configuration settings in {source}
        """
        # extract the source
        source = request.source
        # extract the locator
        locator = request.locator
        # get the executive to kick start the configuration loading
        self.executive.loadConfiguration(uri=source, locator=locator, priority=priority)
        # and return
        return self


    # implementation details for component configuration
    def configureComponentClass(self, component):
        """
        The last step in the configuration of a component class
        """
        # notify each trait
        for trait in component.pyre_traits():
            # that the component class is configured
            trait.classConfigured(component=component)

        # and return the class record
        return component


    def configureComponentInstance(self, instance):
        """
        The last step in the configuration of a component instance
        """
        # go through all deferred assignments that were meant for {instance}
        for assignment, priority in self.retrieveDeferredAssignments(instance=instance):
            # get the name of the trait
            alias = assignment.key[0]
            # get the value
            value = assignment.value
            # and the locator
            locator = assignment.locator
            # ask the instance to set the value
            instance.pyre_setTrait(alias=alias, value=value, priority=priority, locator=locator)

        # notify each trait
        for trait in instance.pyre_traits():
            # that the component instance is configured
            trait.instanceConfigured(instance=instance)

        # all done
        return instance


    def retrieveDirectAssignments(self, key):
        """
        Locate the direct configuration assignment under {key}
        """
        # access the nameserver
        nameserver = self.executive.nameserver

        # go through all the children of this key
        for child, node in nameserver.children(key):
            # get the name of the node
            name = nameserver.getName(child)
            # yield the name and the current value of the node
            yield name, node

        # all done
        return


    def retrieveDeferredAssignments(self, key=None, instance=None):
        """
        Locate the deferred assignments that are relevant to the component instance associated
        with the supplied configuration {key}
        """
        # MGA: 20190624
        #
        # N.B.: the original api required only {key}; {instance} was added to accommodate what
        # appears to be a fundamental problem with early evaluation: the configuration store is
        # not ready to answer questions about components that are nested inside others since
        # the parent nodes have not been created yet
        #
        # the solution here is just a temporary band aid

        # get the configuration key
        key = instance.pyre_key if key is None else key
        # access the nameserver
        nameserver = self.executive.nameserver

        # go through all deferred assignment that were meant for this instance
        for assignment, priority in self.deferred[key]:
            # check all the conditions
            for name, family in assignment.conditions:
                # hash the conditions
                name = nameserver.hash(name)
                family = nameserver.hash(family)
                # if the hashed name matches the instance we are configuring
                if name is key:
                    # no need to look it up; chances are good it's not there yet anyway
                    ref = instance
                # otherwise
                else:
                    # look up the referenced component
                    ref = nameserver.getNode(key=name).value
                # get the type
                cls = type(ref)
                # if the family names don't match
                if cls.pyre_inventory.key is not family:
                    # bail
                    break
            # iff all assignment conditions are satisfied
            else:
                # hand this assignment to the caller
                yield assignment, priority

        # all done
        return


    # bootstrapping
    def initializeNamespace(self):
        """
        Place my default settings in the global namespace
        """
        from ..traits import properties
        # get the nameserver
        nameserver = self.executive.nameserver
        # and the fileserver
        fileserver = self.executive.fileserver

        # the name of the configuration path slot
        name = 'pyre.configpath'
        # the default value
        value = [ 'vfs:{}'.format(folder) for folder in fileserver.systemFolders ]
        # get the locator
        locator = self.locator
        # build a priority
        priority = nameserver.priority.defaults()
        # make a trait; give it a name since it won't be attached to anybody
        configpath = properties.uris(name=name, default=value)

        # place the trait in the model
        nameserver.insert(name=name, value=value,
                          factory=configpath.instanceSlot,
                          priority=priority, locator=locator)

        # all done
        return self


    # meta-methods
    def __init__(self, executive=None, **kwds):
        # chain up
        super().__init__(**kwds)

        # remember my executive
        self.executive = None if executive is None else weakref.proxy(executive)

        # initialize my codecs
        self.codecs = self._indexDefaultCodecs()

        # configuration events
        self.commands = []
        self.deferred = collections.defaultdict(list)

        # the record of configuration sources in the order they were encountered
        self.sources = []

        # all done
        return


    # implementation details
    def _indexDefaultCodecs(self):
        """
        Initialize the codec index
        """
        # make an empty index
        index = {}

        # add the {pml} codec
        from .pml import pml
        index[pml.encoding] = pml

        # add the {cfg} codec
        from .cfg import cfg
        index[cfg.encoding] = cfg

        # add the {pfg} codec
        from .pfg import pfg
        index[pfg.encoding] = pfg

        # add the {yaml} codec
        from .yaml import yaml
        index[yaml.encoding] = yaml

        # all done
        return index


# end of file
