# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import os # for path
import collections # for defaultdict and OrderedDict
from .. import schema
from .. import tracking


# class declaration
class Configurator:
    """
    The manager of the configuration store
    """


    # types
    from . import events
    from . import exceptions


    # defaults
    locator = tracking.simple('during pyre startup')
    configpath = ['vfs:/pyre/system', 'vfs:/pyre/user', 'vfs:/pyre/startup']


    # public data
    codecs = None


    # interface
    def loadConfiguration(self, executive, uri, source, locator, priority):
        """
        Use {uri} to find a codec that can process {source} into a stream of configuration
        events
        """
        # initialize the pile of encountered errors
        errors = []

        # extract the file extension
        _, extension = os.path.splitext(uri.address)
        # deduce the encoding
        encoding = extension[1:]
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
        events = self.codecs[encoding].decode(uri, source, locator)
        # process it
        errors.extend(self.processEvents(executive=executive, events=events, priority=priority))
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
    def processEvents(self, executive, events, priority):
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
            event.identify(inspector=self, executive=executive, priority=priority)
        # all done
        return errors


    def assign(self, executive, assignment, priority):
        """
        Process {assignment} by building a slot and placing it in {model}
        """
        # get the nameserver
        model = executive.nameserver
        # unpack the value
        value = assignment.value
        # get the locator
        locator = assignment.locator
        # hash the assignment key
        key = model._hash.hash(items=assignment.key)
        # ask the nameserver to make a slot for me
        slot = model.buildNode(key=key, value=value, priority=priority(), locator=locator)
        # add it to the model and return the (key, slot) pair; note that the slot returned is
        # the survivor of the priority context, hence not necessarily the slot we made here
        return model.insert(name=model.join(*assignment.key), key=key, node=slot)


    def defer(self, executive, assignment, priority):
        """
        Process a conditional assignment
        """
        # build the key
        key = executive.nameserver.hash(name=assignment.component)
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


    def execute(self, executive, command, priority):
        """
        Record a request to execute a command
        """
        # adjust the command priority
        command.priority = priority()
        # record the command and its context
        self.commands.append(command)
        # all done
        return self


    def load(self, executive, request, priority):
        """
        Ask the pyre {executive} to load the configuration settings in {source}
        """
        # extract the source
        source = request.source
        # extract the locator
        locator = request.locator
        # get the executive to kick start the configuration loading
        executive.loadConfiguration(uri=source, locator=locator, priority=priority)
        # and return
        return self


    # implementation details for component configuration
    def configureComponentClass(self, component):
        """
        The last step in the configuration of a component class
        """
        # not much to do 
        return component


    def configureComponentInstance(self, instance):
        """
        The last step in the configuration of a component instance
        """
        # go through all deferred assignment that were meant for {instance}
        for assignment, priority in self.retrieveDeferredAssignments(instance=instance):
            # find the trait
            trait = instance.pyre_trait(assignment.key[0])
            # ask it to set the value
            trait.setInstanceTrait(
                configurable=instance, value=assignment.value,
                priority=priority, locator=assignment.locator)
        # all done
        return instance


    def retrieveDeferredAssignments(self, instance):
        """
        Locate the deferred assignments that are relevant to {instance}
        """
        # get the executive
        executive = instance.pyre_executive
        # and the nameserver
        nameserver = executive.nameserver
        # ask the {instance} for its registration key
        key = instance.pyre_key
        # go through all deferred assignment that were meant for {instance}
        for assignment, priority in self.deferred[key]:
            # check all the conditions
            for name, family in assignment.conditions:
                # hash the conditions
                name = nameserver.hash(name)
                family = nameserver.hash(family)
                # compute the intended instance safely: avoid the infinite recursion caused by
                # asking the nameserver for the value of the slot whose value we are in the
                # middle of building...
                target = instance if name is key else nameserver[name]
                # check the family
                if target.pyre_familyKey is not family: break
            # this is executed iff all assignment conditions are true
            else:
                # hand this assignment to the caller
                yield assignment, priority
        # all done
        return


    # bootstrapping
    def initializeNamespace(self, nameserver):
        """
        Place my default settings in the global namespace
        """
        # the name of the configuration path slot
        name = 'pyre.configpath'
        # make its key
        key = nameserver.hash(name)
        # build the configuration path slot
        slot = nameserver.variable(
            key=key,
            value=self.configpath, 
            converter=schema.list(schema.uri).coerce, 
            priority=nameserver.priority.defaults(), locator=self.locator)
        # place it in the model
        nameserver.insert(name=name, key=key, node=slot)
        # all done
        return


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # initialize my codecs
        self.codecs = self._indexDefaultCodecs()

        # configuration events
        self.commands = []
        self.deferred = collections.defaultdict(list)

        # all done
        return


    # implementation details
    def _indexDefaultCodecs(self):
        """
        Initialize the codec index
        """
        # make an empty index
        index = collections.OrderedDict()

        # add the {cfg} codec
        from .cfg import cfg
        index[cfg.encoding] = cfg

        # add the {pml} codec
        from .pml import pml
        index[pml.encoding] = pml

        # all done
        return index


# end of file 
