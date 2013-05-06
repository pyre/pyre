# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
# import weakref
from .. import tracking
from .. import algebraic
from .Package import Package


# my declaration
class NameServer(algebraic.hierarchicalModel):
    """
    The manager of the full set of runtime objects that are accessible by name. This includes
    everything from configuration settings to components and interfaces
    """


    # types
    from .Slot import Slot as node
    from .Priority import Priority as priority


    # framework object management 
    def configurable(self, name, configurable, locator, priority=None):
        """
        Add {configurable} to the model under {name}
        """
        # hash the name
        key = self._hash.hash(items=name.split(self.separator))
        # get the right priority
        priority = self.priority.package() if priority is None else priority
        # build a slot to hold the {configurable}
        slot = self.variable(key=key, value=configurable, priority=priority, locator=locator)
        # store it in the model
        self._nodes[key] = slot
        self._names[key] = name
        # and return the key
        return key


    def package(self, name, executive, locator):
        """
        Retrieve the named package from the model. If there is no such package, instantiate one, 
        configure it, and add it to the model.
        """
        # take {name} apart and extract the package name as the top level identifier
        name = name.split(self.separator)[0]
        # hash it
        key = self._hash[name]
        # if there is a node registered under this key
        try:
            # grab it
            package = self._nodes[key].value
            # make sure it is a package
            if not isinstance(package, Package):
                # complain
                complaint = 'name conflict while configuring package {!r}: {}'.format(name, package)
                # log the error
                import journal
                error = journal.error('pyre.configuration')
                error.log(complaint)
                # and punt
                raise ValueError(complaint)
        # if not
        except (KeyError, ValueError):
            # make one
            package = Package(name=name)
            # get the right priority
            priority = self.priority.package()
            # attach it to a slot
            slot = self.literal(key=key, value=package, locator=locator, priority=priority)
            # store it in the model
            self._nodes[key] = slot
            self._names[key] = name
            # configure it
            executive.configurePackage(package=package, locator=locator)
        # and return it
        return package


    # access to my indices
    def registerTrait(self, key, strategy):
        """
        Register {trait} under {key}
        """
        # associate the trait with the key
        self._traits[key] = strategy
        # if there is already a slot under this key
        try:
            # get it
            slot = self._nodes[key]
        # if not there
        except KeyError:
            # no worries
            pass
        # if there
        else:
            # adjust it
            slot.macro, slot.converter = strategy(model=self)

        # all done
        return


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


    # override the literal slot factory to provide a default priority
    def literal(self, key=None, priority=None, locator=None, **kwds):
        """
        Build a literal node
        """
        # adjust the priority
        priority = self.priority.uninitialized() if priority is None else priority
        # easy enough
        return self.node.literal(key=key, priority=priority, locator=locator, **kwds)


    # override superclass methods
    def alias(self, target, alias, base=None):
        """
        Register the name {alias} as an alternate name for {canonical}
        """
        # chain up
        targetKey, aliasKey, survivorSlot = super().alias(target=target, alias=alias, base=base)
        # if there is no survivor
        if survivorSlot is None:
            # this must have been an aliasing of nodes for which there is no configuration
            # state yet; nothing further to do
            return targetKey, aliasKey, survivorSlot

        # otherwise, adjust the slot key
        survivorSlot.key = targetKey
        # check whether
        try:
            # this is an alias for a trait
            strategy = self._traits[targetKey]
        # if not
        except KeyError:
            # no worries
            pass
        # if the key corresponds to a trait
        else:
            # ask it for its value conversion strategy
            _, converter = strategy(model=self)
            # attach the converter to the surviving slot
            survivorSlot.converter = converter
            # and mark it as dirty so its value is recomputed
            survivorSlot.dirty = True

        # return the pair of keys and the surviving node
        return targetKey, aliasKey, survivorSlot


    def buildNode(self, key, value, priority, locator):
        """
        Build a node to hold {value}
        """
        # if the key is associate with a trait
        try:
            # get the evaluation strategy left behind during trait registration
            strategy = self._traits[key]
        # if not a trait node
        except KeyError:
            # by default, make interpolations
            macro = self.interpolation
            # use the default converter
            converter = self.node.converter.identity.coerce
        # if it a trait node
        else:
            # invoke it to get the node factory and schema
            macro, converter = strategy(model=self)

        # build and return the slot
        return macro(key=key, value=value, priority=priority, locator=locator, converter=converter)

            
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
            self._names[key] = name
        # return the node
        return node


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # build the index of slots that are traits
        self._traits = {}

        # all done
        return


    # implementation details
    # adding entries to the model: the highest level interface
    def __setitem__(self, name, value):
        """
        Convert {value} into a node and update the model
        """
        # hash the {name}
        key = self.hash(name)
        # figure out the location of my caller
        locator = tracking.here(1)
        # make priorities from the explicit category
        priority = self.priority.explicit

        # make the slot
        new = self.buildNode(key=key, value=value, priority=priority(), locator=locator)
        # add it to the model
        return self.insert(name=name, key=key, node=new)


    # private data
    _traits = None


# end of file 
