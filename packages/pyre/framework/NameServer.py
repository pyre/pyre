# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# externals
import collections
from .. import tracking # for locators
from ..traits.Property import Property as properties # to get the default trait type
# superclass
from ..calc.Hierarchical import Hierarchical


# my declaration
class NameServer(Hierarchical):
    """
    The manager of the full set of runtime objects that are accessible by name. This includes
    everything from configuration settings to components and interfaces
    """


    # types
    from .Package import Package
    # node storage and metadata
    from .Slot import Slot as node
    from .SlotInfo import SlotInfo as info
    from .Priority import Priority as priority


    # framework object management 
    def configurable(self, name, configurable, locator, priority=None):
        """
        Add {configurable} to the model under {name}
        """
        # get the right priority
        priority = self.priority.package() if priority is None else priority
        # build the node metadata
        info = self.info(model=self, name=name, locator=locator, priority=priority)
        # grab the key
        key = info.key
        # build a slot to hold the {configurable}
        slot = self.variable(key=key, value=configurable)
        # store it in the model
        self._nodes[key] = slot
        self._metadata[key] = info

        # and return the key
        return key


    def package(self, name, executive, locator):
        """
        Retrieve the named package from the model. If there is no such package, instantiate one, 
        configure it, and add it to the model.
        """
        # take {name} apart and extract the package name as the top level identifier
        name = self.split(name)[0]
        # hash it
        key = self._hash[name]
        # if there is a node registered under this key
        try:
            # grab it
            package = self._nodes[key].value
        # if not
        except KeyError:
            # make one
            package = self.Package(name=name)
            # get the right priority
            priority = self.priority.package()
            # attach it to a slot
            slot = self.literal(key=key, value=package)
            # store it in the model
            self._nodes[key] = slot
            self._metadata[key] = self.info(model=self,
                                            name=name, key=key, locator=locator, priority=priority)
            # configure it
            executive.configurePackage(package=package, locator=locator)
        # if it's there
        else:
            # make sure it is a package, and if not
            if not isinstance(package, self.Package):
                # get the journal
                import journal
                # build the report
                complaint = 'name conflict while configuring package {!r}: {}'.format(name, package)
                # complain
                raise journal.error('pyre.configuration').log(complaint)

        # return the package
        return package


    # expansion services
    def evaluate(self, expression):
        """
        Evaluate the given {expression} in my current context
        """
        # attempt to
        try:
            # evaluate the expression
            return self.node.expression.expand(model=self, expression=expression)
        # with empty expressions
        except self.EmptyExpressionError:
            # just return the input
            return expression


    def interpolate(self, expression):
        """
        Interpolate the given {expression} in my current context
        """
        # attempt to
        try:
            # evaluate the expression
            return self.node.interpolation.expand(model=self, expression=expression)
        # with empty expressions
        except self.EmptyExpressionError:
            # just return the input
            return expression


    # override superclass methods
    def alias(self, target, alias, base=None):
        """
        Register the name {alias} as an alternate name for {canonical}
        """
        # chain up
        try:
            # to have most aliasing cases handled by the hierarchical symbol table
            return super().alias(target=target, alias=alias, base=base)
        # which fails when the {alias} and the {target} both exist
        except self.AliasingError as error:
            # resolve by comparing the priorities of the two nodes
            targetInfo = error.targetInfo
            aliasInfo = error.aliasInfo
            # if the alias node is higher priority
            if targetInfo.priority < aliasInfo.priority:
                # get the target
                targetNode = error.targetNode
                # and the alias
                aliasNode = error.aliasNode
                # get the alias to replace the target
                aliasNode.replace(targetNode)
                # adjust the processor
                aliasNode.postprocessor = targetNode.postprocessor
                # make it the node associated with the key
                self._nodes[error.key] = aliasNode
                # adjust the node info
                meta = self._metadata[error.key]
                meta.priority = aliasInfo.priority
                meta.locator = aliasInfo.locator

        # all done
        return 
            

    def insert(self, value, priority, locator, key=None, name=None, factory=None):
        """
        Add {value} to the store
        """
        # if the name is empty
        if name is None:
            # better have a non-empty key...
            pass
        # check whether the name is a string
        elif isinstance(name, str):
            # split it
            split = self.split(name)
            # and hash it, if necessary
            key = key or self._hash.hash(items=split)
        # if it is a collection of fragments
        elif isinstance(name, collections.Iterable):
            # save it
            split = name
            # put the name back together
            name = self.join(*split)
            # and hash it, if necessary
            key = key or self._hash.hash(items=split)
        # if it is already hashed
        elif isinstance(name, type(self._hash)):
            # override the given {key}, if necessary
            key = key or name
            # and clear the others, since they are not derivable 
            name = None
            split = ()
        # anything else is a bug
        else:
            # get the journal
            import journal
            # put together a message
            msg = "unrecognizable name: {!r}".format(name)
            # and complain
            raise journal.firewall('pyre.config').log(msg)

        # if i don't have a key by now, we have found a bug
        if key is None:
            # get the journal
            import journal
            # put together a message
            msg = "both name and key were empty; now what?"
            # and complain
            raise journal.firewall('pyre.config').log(msg)

        # look for metadata
        try:
            # registered under this key
            meta = self._metadata[key]
        # if there's no registered metadata, this is the first time this name was encountered
        except KeyError:
            # if we need to build type information
            if not factory:
                # use instance slots for an identity trait, by default
                factory = properties.identity(name=name).instanceSlot
            # build the info node
            meta = self.info(model=self,
                             name=name, split=split, key=key,
                             priority=priority, locator=locator, factory=factory)
            # and attach it
            self._metadata[key] = meta
        # if there is an existing metadata node
        else:
            # check whether this assignment is of lesser priority, in which case we just leave
            # the value as is
            if priority < meta.priority:
                # but we may have to adjust the trait
                if factory:
                    # which involves two steps: first, update the info node
                    meta.factory = factory
                    # and now look for the existing model node
                    old = self._nodes[key]
                    # so we can update its value postprocessor
                    old.postprocessor = factory.processor
                # in any case, we are done here
                return key
            # ok: higher priority assignment; check whether we should update the descriptor
            if factory: meta.factory = factory
            # adjust the locator and priority of the info node
            meta.locator = locator
            meta.priority = priority

        # if we get this far, we have a valid key, and valid and updated metadata; start
        # processing the value by getting the trait; use the info node, which is the
        # authoritative source of this information
        factory = meta.factory
        # and ask it to build a node for the value
        new = factory(key=key, value=value)

        # if we are replacing an existing node
        try:
            # get it
            old = self._nodes[key]
        # if not
        except KeyError:
            # no worries
            pass
        # otherwise
        else:
            # adjust the dependency graph
            new.replace(old)

        # place the new node in the model
        self._nodes[key] = new

        # and return
        return key

            
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
            node = self.node.unresolved(key=key, request=name)
            # add it to the pile
            self._nodes[key] = node
            self._metadata[key] = self.info(model=self, name=name, key=key)
        # return the node
        return node


    # implementation details
    # adding entries to the model: the highest level interface
    def __setitem__(self, name, value):
        """
        Convert {value} into a node and update the model
        """
        # figure out the location of my caller
        locator = tracking.here(1)
        # make a priority ranking from the explicit category
        priority = self.priority.explicit()

        # add the value to the model
        return self.insert(name=name, value=value, priority=priority, locator=locator)


# end of file 
