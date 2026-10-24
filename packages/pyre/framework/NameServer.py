# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
from .. import tracking  # for locators
from ..traits.Property import Property as properties  # to get the default trait type

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

    # node storage and meta-data
    from .Slot import Slot as node
    from .SlotInfo import SlotInfo as info
    from .Priority import Priority as priority

    # public data
    @property
    def configpath(self):
        """
        Return an iterable over my configuration path
        """
        # the answer is in my store
        return self["pyre.configpath"]

    # framework object management
    def configurable(self, name, configurable, locator, priority):
        """
        Add {configurable} to the model under {name}
        """
        # add the {configurable} to the store
        # N.B: let {insert} choose the slot factory; this used to specify a {literal} as the
        # slot factory, but this appears to have been misguided: there are paths when replacing
        # an existing node that invoked the slot factory with more arguments than
        # {self.literal} could handle...
        key, _, _ = self.insert(name=name, value=configurable, priority=priority, locator=locator)
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
            node = self._nodes[key]
        # if not
        except KeyError:
            # if I do not have a locator, point to my caller
            locator = tracking.here(level=1) if locator is None else locator
            # make one
            package = self.createPackage(name=name, locator=locator)
            # configure it
            package.configure(executive=executive)
        # if there is a node there already
        else:
            # what the store records about it
            info = self._metadata[key]
            # if the node is a marker left by a request for a name nobody has set
            if isinstance(node, self.node.unresolved):
                # the package takes its place
                package = self.createPackage(name=name, locator=locator)
                # configure it
                package.configure(executive=executive)
            # if the node holds a value someone set, rather than one the framework registered
            elif not isinstance(info.priority, self.priority.framework):
                # the name belongs to the package, so complain
                self.refuseValue(name=name, kind="a package", locator=info.locator)
                # if the firewall is not fatal, the package takes its name
                package = self.createPackage(name=name, locator=locator)
                # configure it
                package.configure(executive=executive)
            # otherwise, the framework registered it
            else:
                # get the value of the node
                package = node.value
                # make sure it is a package, and if not
                if not isinstance(package, self.Package):
                    # get the journal
                    import journal

                    # build the report
                    complaint = f"name conflict while configuring package '{name}': {package}"
                    # and complain
                    raise journal.error("pyre.configuration").log(complaint)

        # return the package
        return package

    def reserve(self, name):
        """
        Check that nobody set a value at {name}, the family of a protocol or a component that is
        about to be registered: family names belong to the framework
        """
        # hash the name
        key = self.hash(name)
        # attempt to
        try:
            # look up what the store records at {name}
            info = self._metadata[key]
        # if there is nothing
        except KeyError:
            # the name is free
            return
        # if the node is a marker left by a request for a name nobody has set, or a family the
        # framework registered before, as when a class is declared again
        if isinstance(self._nodes[key], self.node.unresolved) or isinstance(
            info.priority, self.priority.framework
        ):
            # the registration may take it
            return
        # otherwise, someone set a value there, so complain
        self.refuseValue(name=name, kind="a family", locator=info.locator)
        # if the firewall is not fatal, the registration takes the name
        return

    def refuseValue(self, name, kind, locator):
        """
        Fire the firewall for a value set at {name}, which names {kind}, a package or a family;
        these names belong to the framework, and a value there is a mistake, such as a typo in a
        family name
        """
        # get the journal
        import journal

        # make a channel
        channel = journal.firewall("pyre.configuration")
        # say what is wrong
        channel.line(f"'{name}' names {kind}, so it can't be given a value")
        # and where the value was set
        channel.line(f"the value was set at {locator}")
        # and complain
        channel.log()
        # all done
        return

    def kind(self, key):
        """
        Say what the node at {key}, which the framework registered, names: a package, or the
        family of a protocol or a component
        """
        # the node holds what the framework put there, so its value is at hand
        value = self._nodes[key].value
        # name it
        return "a package" if isinstance(value, self.Package) else "a family"

    # auxiliary object management
    def createPackage(self, name, locator):
        """
        Build a new package node and attach it to the model
        """
        # make one
        package = self.Package(name=name, locator=locator)
        # hash the name
        key = self._hash[name]
        # get the right priority: package names belong to the framework
        priority = self.priority.framework()
        # attach it to a slot
        slot = self.literal(key=key, value=package)
        # fill out the node info
        name, split, key = self.info.fillNodeId(model=self, key=key, name=name)
        # store it in the model
        self._nodes[key] = slot
        # along with its metadata
        self._metadata[key] = self.info(
            name=name, key=key, split=split, locator=package.locator, priority=priority
        )
        # and return it
        return package

    # expansion services
    def evaluate(self, expression):
        """
        Evaluate the given {expression} in my current context
        """
        # attempt to
        try:
            # evaluate the expression
            value = self.node.expression.expand(model=self, expression=expression)
        # with empty expressions
        except self.EmptyExpressionError as error:
            # use the expanded text, since the input may have contained escaped braces
            value = error.expression
        # all done
        return value

    def interpolate(self, expression):
        """
        Interpolate the given {expression} in my current context
        """
        # attempt to
        try:
            # evaluate the expression
            node = self.node.interpolation.expand(model=self, expression=expression)
        # with empty expressions
        except self.EmptyExpressionError as error:
            # return the expanded text, since it the input may have contained escaped braces
            node = error.expression
        # all done
        return node

    # override superclass methods
    def insert(
        self, value, priority, locator, key=None, name=None, split=None, factory=None, claim=False
    ):
        """
        Add {value} to the store; with {claim}, {value} takes the node whatever the priority of
        what is there, and keeps {priority} for the assignments that follow
        """
        # N.B.: presenting a {value} to be inserted into the model under {key} involves using
        # the {factory} to create a slot. the {factory} used is either the one supplied by the
        # caller, or whatever is registered as metadata for this {key}. the metadata, i.e. the
        # locator and the assignment priority must be correctly associated with the key before
        # the {factory} is invoked because the {tracker}, and other observers, may query the
        # name server for it as part of the slot creation. if the call to the {factory} throws
        # an exception, the metadata must be rolled back to what it was before the failed node
        # insertion.

        # figure out the node info
        name, split, key = self.info.fillNodeId(model=self, key=key, split=split, name=name)

        # check we have full node info
        if name is None or split is None or key is None:
            # grab the journal
            import journal

            # make a bug report
            bug = f"incomplete node info: name={name}, {locator}"
            # and submit it
            raise journal.firewall("pyre.framework").log(bug)

        # look for the node registered under this key
        old = self._nodes.get(key, None)
        # and its metadata
        meta = self._metadata.get(key)

        # if this is the first time this name was encountered
        if meta is None:
            # we shouldn't have an {old} node either
            if old is not None:
                # if we do, it's a bug, so get the journal
                import journal

                # build a bug report
                bug = f"{name}: found a node with no metadata"
                # and complain
                raise journal.firewall("pyre.nameserver").log(bug)

            # if we were not given a slot factory
            if factory is None:
                # use instance slots for a generic trait
                factory = properties.identity(name=name).instanceSlot

            # speculative: update the metadata
            # build the info node
            meta = self.info(
                name=name, split=split, key=key, priority=priority, locator=locator, factory=factory
            )
            # and attach it to the meta-data store, ahead of node creation so it is available to
            # anything that asks for it while the node is being built
            self._metadata[key] = meta

            # gingerly
            try:
                # build the new node
                new = factory(key=key, value=value)
            # if anything at all goes wrong, an interrupt included
            except BaseException:
                # the store must not keep the metadata of a node that was never built
                del self._metadata[key]
                # but the error is not mine to handle, so pass it on
                raise
            # otherwise, we are all good; attach the node
            self._nodes[key] = new
            # and return the insertion info
            return key, new, old

        # getting this far implies we've bumped into this key before; remember the factory that
        # builds its nodes, so it can be put back if the new node can't be built
        installed = meta.factory
        # if the caller has supplied a specific factory
        if factory:
            # install it
            meta.factory = factory

        # if the assignment happens during component configuration
        if priority.category == priority.defaults.category:
            # verify a factory was prescribed
            if factory is None:
                # if not, it's a bug
                import journal

                # build a report
                bug = f"{name}: trait configuration without a factory"
                # and complain
                raise journal.firewall("pyre.nameserver").log(bug)

            # we have already updated the factory; remember the rank and the provenance of the
            # existing node, in case the new one can't be built
            mark = (meta.priority, meta.locator)
            # if the default claims the node, the setting is given up, as when a trait is
            # deleted; if the existing node ranks below this default, nobody has set the name:
            # the node is the placeholder a reference left behind, which has no value, or the
            # default of a component that this one replaces, which is not this component's; if it
            # ranks the same, it is this very default applied again, as when a map that is rebuilt
            # files its entries, which refreshes its value
            if claim or not priority < meta.priority:
                # so the default takes over the setting, along with its rank
                meta.priority = priority
                # and its provenance
                meta.locator = locator
                # and the new node is built out of the default
                source = value
            # otherwise, the existing setting outranks the default, and keeps its rank and its
            # provenance
            else:
                # the existing node is not the correct type, so the new one is built out of its
                # value, which must be correct, because {defaults} is the lowest possible priority
                source = old.value
                # text that was evaluated already
                if isinstance(source, str):
                    # must reach the new node as it is, rather than be evaluated a second time
                    source = self.node.interpolation.escape(source)
            # gingerly
            try:
                # build the new node
                new = factory(key=key, value=source, current=old)
            # if anything at all goes wrong, an interrupt included
            except BaseException:
                # the store must not keep a factory that could not build the node
                meta.factory = installed
                # nor the rank and the provenance of a default that never took over
                meta.priority, meta.locator = mark
                # but the error is not mine to handle, so pass it on
                raise
            # otherwise, register the new node; no need to adjust the graph since the slot
            # factory now takes care of this
            self._nodes[key] = new
            # and we are done
            return key, new, old

        # if the new assignment claims the node, is higher priority than the existing one, or is
        # the existing one applied again, which refreshes its value
        if claim or not priority < meta.priority:
            # save the current metadata so we can roll it back if we have to
            mark = self.info(
                name=name,
                split=split,
                key=key,
                priority=meta.priority,
                locator=meta.locator,
                factory=installed,
            )
            # record the assignment metadata so whoever is watching for this assignment
            # has access to the current information; save the priority
            meta.priority = priority
            # and the assignment locator
            meta.locator = locator
            # now, gingerly
            try:
                # make a new node using the registered node factory
                new = meta.factory(key=key, value=value, current=old)
            # if anything at all goes wrong, an interrupt included
            except BaseException:
                # the store must not keep the metadata of an assignment that never happened
                meta.locator = mark.locator
                meta.priority = mark.priority
                meta.factory = mark.factory
                # but the error is not mine to handle, so pass it on
                raise
            # otherwise, we are all good; register the new node
            self._nodes[key] = new
            # and we are done
            return key, new, old

        # the only remaining case is an assignment of lower priority than the existing one that
        # is also not happening during component configuration; if the existing one is a node
        # the framework registered, the name of a package or a family, the assignment is a
        # mistake
        if isinstance(meta.priority, self.priority.framework):
            # so complain
            self.refuseValue(name=name, kind=self.kind(key=key), locator=locator)
        # otherwise, there is nothing to do in this case
        return key, None, old

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
            # fill out the node info
            name, split, key = self.info.fillNodeId(model=self, key=key, name=name)
            # build an error marker
            node = self.node.unresolved(key=key, request=name)
            # add it to the pile
            self._nodes[key] = node
            # along with its metadata
            self._metadata[key] = self.info(name=name, split=split, key=key)
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

    # handling of content and topological changes to the store
    def store(self, key, name, node, info):
        """
        Associate {name}, {node} and {info} with {key}
        """
        # adjust the node key
        node.key = key
        # attach the node
        self._nodes[key] = node
        # adjust the metadata
        info.key = key
        info.name = name
        # and register it under key
        self._metadata[key] = info
        # all done
        return

    def replace(self, key, name, oldNode, oldInfo, newNode, newInfo):
        """
        Choose which settings to retain
        """
        # if the new node has higher priority
        if newInfo.priority > oldInfo.priority:
            # replace the old node in its evaluation graph
            newNode.replace(oldNode)
            # adjust the key in the new node
            newNode.key = key
            # if somebody has set the old name, its node carries the value processors of its
            # trait; a placeholder that a reference left behind has none
            if oldInfo.priority.category != self.priority.uninitialized.category:
                # so carry them over
                newNode.preprocessor = oldNode.preprocessor
                # both of them
                newNode.postprocessor = oldNode.postprocessor
            # attach it to the store
            self._nodes[key] = newNode
            # adjust the metadata
            oldInfo.priority = newInfo.priority
            oldInfo.locator = newInfo.locator

        # all done
        return

    # aliasing
    def pullGlobalSettingsIntoScope(self, scope, symbols):
        """
        Merge settings for {symbols} between global scope and the given {scope}
        """
        # go through the symbols
        for symbol in symbols:
            # if the {scope} name and the {symbol} are identical
            if scope == symbol:
                # the aliasing will fail, so skip it before we damage the symbol table
                continue
            # otherwise, build the alias
            self.alias(target=self.join(scope, symbol), alias=symbol)

        # all done
        return

    # meta-methods
    def __init__(self, name="pyre::nameserver", **kwds):
        # chain up
        super().__init__(**kwds)
        # record my name
        self._modelName = name
        # all done
        return

    def __str__(self):
        """
        Identify me by name
        """
        # easy enough
        return self._modelName


# end of file
