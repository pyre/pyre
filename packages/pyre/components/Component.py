# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import collections.abc
import uuid
from .. import tracking

# superclass
from .Configurable import Configurable

# metaclass
from .Actor import Actor


# class declaration
class Component(Configurable, metaclass=Actor, internal=True):
    """
    The base class for all components
    """

    # types
    from .PublicInventory import PublicInventory
    from .PrivateInventory import PrivateInventory
    from ..constraints.exceptions import ConstraintViolationError

    # framework data
    pyre_inventory = None  # my inventory management strategy
    pyre_implements = None  # my protocol
    pyre_isComponent = True  # i am a component
    pyre_cooked = False  # whether i am fully built

    # introspection
    @property
    def pyre_key(self):
        """
        Look up my key
        """
        # get my inventory
        inventory = self.pyre_inventory
        # and ask it for my key
        key = inventory.key if inventory is not None else None
        # all done
        return key

    @property
    def pyre_name(self):
        """
        Look up my name
        """
        # get my inventory
        inventory = self.pyre_inventory
        # and ask it for my name; if i don't have one bail
        return inventory.name if inventory is not None else None

    @classmethod
    def pyre_family(cls):
        """
        Deduce my family name
        """
        # get my inventory
        inventory = cls.pyre_inventory
        # ask it for my name; if i don't have one, bail
        return inventory.name if inventory is not None else None

    @classmethod
    def pyre_familyFragments(cls):
        """
        Deduce my family name
        """
        # get my inventory
        inventory = cls.pyre_inventory
        # ask it for my name; if i don't have one, bail
        return inventory.fragments if inventory is not None else ()

    @property
    def pyre_spec(self):
        """
        Build my configuration specification
        """
        # get my name
        name = self.pyre_name or "<none>"
        # and my family name
        family = self.pyre_family() or "<none>"
        # build the spec and return it
        return f"{family}#{name}"

    @classmethod
    def pyre_normalizeInstanceName(cls, name):
        """
        Give a component a chance to normalize the {name} of an instance that is about to
        be created
        """
        # by default, leave it alone
        return name

    @classmethod
    def pyre_package(cls):
        """
        Deduce my package name
        """
        # get my inventory to answer this
        return cls.pyre_inventory.package

    @classmethod
    def pyre_isPublicClass(cls):
        """
        Check whether this component class is public
        """
        # by definition, check the class inventory key
        return cls.pyre_inventory and cls.pyre_inventory.key is not None

    @classmethod
    def pyre_public(cls):
        """
        Generate the sequence of my public ancestors, i.e. the ones that have a non-trivial family
        """
        # filter public ancestors from my pedigree
        yield from (ancestor for ancestor in cls.pyre_pedigree if ancestor.pyre_isPublicClass())
        # all done
        return

    # trait access with optional metadata
    def pyre_setTrait(self, alias, value, priority=None, locator=None):
        """
        Assign {value} to the trait named {alias}
        """
        # identify the trait descriptor
        trait = self.pyre_trait(alias)
        # build a locator
        locator = tracking.here(level=1) if locator is None else locator
        # build a priority
        priority = self.pyre_executive.priority.explicit() if priority is None else priority
        # set the value
        new, old = self.pyre_inventory.setTraitValue(
            trait=trait, factory=trait.instanceSlot, value=value, priority=priority, locator=locator
        )

        # if an actual assignment took place
        if new is not None and self.pyre_cooked:
            # invoke the hook
            self.pyre_traitModified(trait=trait, new=new, old=old)

        # all done
        return

    def pyre_deleteTrait(self, alias, locator=None):
        """
        Give up the value of the trait named {alias}, so that it follows my class again
        """
        # identify the trait descriptor
        trait = self.pyre_trait(alias)
        # build a locator
        locator = tracking.here(level=1) if locator is None else locator
        # get my inventory
        inventory = self.pyre_inventory
        # the priority of the defaults
        defaults = self.pyre_executive.priority.defaults
        # and the priority of the last assignment
        priority = inventory.getTraitPriority(trait)
        # a trait that was never set, or that holds what it started with
        if priority is None or priority.category == defaults.category:
            # has no value of its own to give up
            raise self.TraitUnsetError(configurable=self, name=trait.name)
        # replace the value with what the trait started with, whatever ranks the value had
        new, old = inventory.setTraitValue(
            trait=trait,
            factory=trait.instanceSlot,
            value=inventory.instanceSeed(trait=trait, instance=self),
            priority=defaults(),
            locator=locator,
            claim=True,
        )
        # if i am fully built
        if self.pyre_cooked:
            # invoke the hook
            self.pyre_traitModified(trait=trait, new=new, old=old)
        # all done
        return

    def pyre_getTrait(self, alias):
        """
        Retrieve the value and meta-data associated with the trait named {alias}
        """
        # identify the trait descriptor
        trait = self.pyre_trait(alias)
        # get my inventory
        inventory = self.pyre_inventory
        # ask it for the value
        value = inventory.getTraitValue(trait)
        # and the locator
        locator = inventory.getTraitLocator(trait)
        # pass them on
        return value, locator

    # configuration errors
    @property
    def pyre_configurationErrors(self):
        """
        The errors in the pile of the executive that are about me
        """
        # the executive knows
        return self.pyre_executive.configurationErrors(configurable=self)

    @classmethod
    def pyre_classConfigurationErrors(cls):
        """
        The errors in the pile of the executive that are about my class
        """
        # the executive knows
        return cls.pyre_executive.configurationErrors(configurable=cls)

    def pyre_validateConfiguration(self, visited=None):
        """
        Check my configuration by reading each of my traits, and those of the components they
        hold, record the values they refuse in the pile of the executive, and return them; the
        framework never calls this, and a component may override it to check more, or less
        """
        # unless this is part of a larger check, nothing has been checked yet
        visited = set() if visited is None else visited
        # if i have been checked already
        if self in visited:
            # there is nothing new to find
            return []
        # otherwise, mark me as checked
        visited.add(self)
        # the refusals found here
        errors = []
        # go through my traits
        for trait in self.pyre_configurables():
            # attempt to
            try:
                # read the value
                value = getattr(self, trait.name)
            # if anything is refused
            except self.TraitValueError as error:
                # and it is not already attributed, it surfaced while reading my trait
                if error.configurable is None:
                    # so it is mine
                    error.configurable = self
                # record it against whoever it is about, and add it to the ones found here
                errors.append(self.pyre_recordRefusal(error=error, configurable=error.configurable))
                # and move on
                continue
            # find the components it holds, itself or its entries
            held = list(self.pyre_componentsIn(value=value))
            # go through the components the value holds
            for component in held:
                # and check them too
                errors.extend(component.pyre_validateConfiguration(visited=visited))
        # all done
        return errors

    @classmethod
    def pyre_classValidateConfiguration(cls):
        """
        Check the configuration of my class by reading each of its traits, record the values
        they refuse in the pile of the executive, and return them; the framework never calls this
        """
        # the refusals found here
        errors = []
        # go through my traits
        for trait in cls.pyre_configurables():
            # attempt to
            try:
                # read the value
                getattr(cls, trait.name)
            # if it is refused
            except cls.TraitValueError as error:
                # record it against my class, and add it to the ones found here
                errors.append(cls.pyre_recordRefusal(error=error, configurable=cls))
        # all done
        return errors

    @classmethod
    def pyre_recordRefusal(cls, error, configurable):
        """
        Record {error}, a refusal a check found in a trait of {configurable}, unless an earlier
        check recorded it already, and return the refusal that is in the pile
        """
        # get the executive
        executive = cls.pyre_executive
        # go through the errors recorded against {configurable}
        for known in executive.configurationErrors(configurable=configurable):
            # if one of them is the same refusal
            if error.repeats(other=known):
                # it is the one in the pile
                return known
        # otherwise, it is new, so record it
        executive.recordConfigurationError(error=error, configurable=configurable)
        # and hand it back
        return error

    def pyre_showConfigurationErrors(self, channel=None):
        """
        Report the errors that are about me in one entry on {channel}, by default the
        {pyre.configuration} info channel; the framework never calls this
        """
        # get my errors
        errors = self.pyre_configurationErrors
        # if there are none
        if not errors:
            # there is nothing to report
            return self
        # get the journal
        import journal

        # unless the caller has a channel in mind, make one
        channel = journal.info("pyre.configuration") if channel is None else channel
        # say what this is about
        channel.line(f"configuration errors of {self}:")
        # go through the errors
        channel.indent()
        # each one
        for error in errors:
            # in as many lines as it takes
            channel.report(report=str(error).splitlines())
        # done with the errors
        channel.outdent()
        # and flush
        channel.log()
        # all done
        return self

    @classmethod
    def pyre_componentsIn(cls, value):
        """
        Generate the component instances {value} holds: itself, or the entries of a container
        """
        # a map holds its values
        if isinstance(value, collections.abc.Mapping):
            # so they are the candidates
            candidates = value.values()
        # a sequence or a set holds its items, but text, which is a sequence, holds no components
        elif isinstance(value, (list, tuple, set, frozenset)):
            # so they are the candidates
            candidates = value
        # anything else
        else:
            # is the only candidate
            candidates = [value]
        # go through the candidates
        for candidate in candidates:
            # and pick the component instances
            if isinstance(candidate, Component):
                # hand it over
                yield candidate
        # all done
        return

    # framework notifications
    @classmethod
    def pyre_staged(cls, name, locator, implicit):
        """
        Pre-instantiation hook invoked right before the instance is created
        """
        # grab my protocol
        protocol = cls.pyre_implements
        # if i don't have one
        if protocol is None:
            # bail
            return cls

        # if the instance that's about to be created is named and was requested explicitly
        if name and not implicit:
            # ask my protocol to load any {name} specific configuration files
            protocol.pyre_configure(name=name, locator=locator)

        # and nothing further
        return cls

    def pyre_registered(self):
        """
        Hook that gets invoked by the framework after the component instance has been
        registered but before any configuration events
        """
        # nothing to do
        return self

    def pyre_configured(self):
        """
        Hook that gets invoked by the framework after the component instance has been
        configured but before the binding of any of its traits
        """
        # return the list of errors encountered while checking the configuration
        return []

    def pyre_initialized(self):
        """
        Hook that gets invoked by the framework right before the component is put into
        action. The component is configured, but its traits are evaluated when they are first
        read, so a value one of them refuses surfaces then, or when its configuration is
        checked. This is the place where the component should acquire whatever further
        resources it requires.
        """
        # return the list of errors encountered while checking the instance state and acquiring
        # resources; by default, there aren't any
        return []

    def pyre_traitModified(self, trait, new, old):
        """
        Hook that gets invoked by the framework right after a trait value has been modified.
        """
        # nothing to do
        return self

    def pyre_finalized(self):
        """
        Hook that gets invoked by the framework right before the component is decommissioned.
        The instance should release all acquired resources.
        """
        # nothing to do
        return self

    # introspection
    @classmethod
    def pyre_getExtent(cls):
        """
        Return the extent of this class, i.e. the set of its instances
        """
        # the registrar knows
        return cls.pyre_registrar.components[cls]

    def pyre_slot(self, attribute=None):
        """
        Return the slot associated with {attribute}; if no attribute is given, return the slot with
        the component instance itself
        """
        # if the caller did not specify an attribute
        if attribute is None:
            # get my key
            key = self.pyre_key
            # if i don't have a key
            if key is None:
                # not sure what to do
                return None
            # otherwise, get my nameserver to retrieve my slot
            return self.pyre_nameserver.getNode(key)

        # if we have an {attribute} name, find the associated trait descriptor
        trait = self.pyre_trait(alias=attribute)
        # look up the slot associated with this trait and return it
        return self.pyre_inventory[trait]

    def pyre_how(self, attribute):
        """
        Return the priority associated with {attribute}
        """
        # find the trait descriptor associated with this {attribute}
        trait = self.pyre_trait(alias=attribute)
        # and return its meta-data
        return self.pyre_inventory.getTraitPriority(trait)

    def pyre_where(self, attribute=None):
        """
        Return the locator associated with {attribute}; if no attribute name is given, return
        the locator of the component instance
        """
        # if no name is given
        if attribute is None:
            # return my locator
            return self.pyre_locator
        # otherwise, find the trait descriptor associated with this {attribute}
        trait = self.pyre_trait(alias=attribute)
        # and return its meta-data
        return self.pyre_inventory.getTraitLocator(trait)

    @classmethod
    def pyre_classWhere(cls, attribute=None):
        """
        Return the component class locator
        """
        # if no name is given
        if attribute is None:
            # return my locator
            return cls.pyre_locator
        # otherwise, find the trait descriptor associated with this {attribute}
        trait = cls.pyre_trait(alias=attribute)
        # and return its meta-data
        return cls.pyre_inventory.getTraitLocator(trait)

    # meta methods
    def __new__(cls, name, locator, implicit, pyre_values=None, **kwds):
        # build the instance; in order to accommodate components with non-trivial constructors,
        # we have to swallow any extra arguments passed to {__new__}; unfortunately, this
        # places some restrictions on how components participate in class hierarchies: no
        # ancestor of a user component can implement a {__new__} with non-trivial signature,
        # since it will never get its arguments. Sorry...

        # NYI: a possible work-around is to introduce a dummy class in the ancestry whose only
        # job is to swallow all extra arguments; this class can be injected automatically at
        # the end of the list of bases by {Actor}, making this entire process transparent to
        # the user
        instance = super().__new__(cls)

        # record the locator
        instance.pyre_locator = locator
        # deduce the visibility of this instance
        inventory = cls.PrivateInventory if name is None else cls.PublicInventory
        # ask the inventory to initialize the instance
        inventory.initializeInstance(instance=instance, name=name, implicit=implicit)
        # deposit the trait values the constructor was handed; only an anonymous instance gets
        # any, since a named one finds its values in the nameserver, and they must be in place
        # before the configuration hooks run, the way they are for a named instance
        for trait, value in (pyre_values or {}).items():
            # through the inventory, at construction priority, from where the caller stood
            instance.pyre_setTrait(
                alias=trait.name,
                value=value,
                priority=cls.pyre_executive.priority.construction(),
                locator=locator,
            )
        # configure it, and collect what the configuration hooks find wrong
        errors = list(inventory.configureInstance(instance))
        # if they found anything
        if errors:
            # record it against the instance, which is built anyway
            cls.pyre_executive.recordConfigurationError(
                error=cls.ConfigurationError(configurable=instance, errors=errors),
                configurable=instance,
            )

        # all done
        return instance

    def __init__(self, name, locator, implicit, pyre_values=None, **kwds):
        # chain up, but first swallow the extra arguments that are used by my metaclass
        super().__init__(**kwds)
        # make me an id
        self.pyre_id = uuid.uuid1()
        # all done
        return

    def __str__(self):
        # accumulate the name fragments here
        fragments = []
        # get my name
        name = self.pyre_name
        # if i have one:
        if name is not None:
            # use it
            fragments.append(f"component '{name}'")
        # get my family name
        family = self.pyre_family()
        # if i have one
        if family:
            # use it
            fragments.append(f"an instance of '{family}'")
        # otherwise
        else:
            # find the name of my class
            marker = type(self).__name__
            # and use it
            fragments.append(f"an instance of '{marker}'")
        # assemble
        return ", ".join(fragments)

    def __getattr__(self, name):
        """
        Trap attribute lookup errors and attempt to resolve the name in my inventory's name
        map. This makes it possible to get the value of a trait by using any of its aliases.
        """
        # attempt to
        try:
            # normalize the name
            normal = self.pyre_namemap[name]
        # if it's not one of my traits
        except KeyError:
            # get someone else to do the work
            raise AttributeError(f"{self} has no attribute '{name}'") from None

        # if the normalized name is the same as the original
        if normal == name:
            # nothing further to do but complain: this is almost certainly a framework bug;
            # build an error message
            error = self.TraitNotFoundError(configurable=self, name=name)
            # get the journal
            import journal

            # complain
            raise journal.firewall("pyre.components").log(str(error))

        # if we got this far, restart the attribute lookup using the canonical name
        # N.B.: don't be smart here; let {getattr} do its job, which involves invoking the
        # trait descriptors if necessary
        return getattr(self, normal)

    def __setattr__(self, name, value):
        """
        Trap attribute assignment and attempt to normalize the name before making the assignment
        """
        # with {__setattr__} defined, all assignments come through here; therefore, there is no
        # need for the trait descriptors to define {__set__}: it would never get called unless
        # we chain up here after normalizing the name. this might be ok, if it weren't for the
        # fact that it is impossible to guarantee that the locator will be correct in all cases

        # we must record the location of the caller; {pyre_setTrait} doesn't know the correct
        # stack depth whenever this method is involved
        locator = tracking.here(level=1)
        # attempt to
        try:
            # set the trait
            self.pyre_setTrait(alias=name, value=value, locator=locator)
        # if this fails
        except self.TraitNotFoundError:
            # this must be a non-trait attribute
            super().__setattr__(name, value)

        # all done
        return

    def __delattr__(self, name):
        """
        Trap attribute deletion, so that a trait gives up its value and follows my class again
        """
        # we must record the location of the caller; {pyre_deleteTrait} doesn't know the correct
        # stack depth whenever this method is involved
        locator = tracking.here(level=1)
        # attempt to
        try:
            # give up the value of the trait
            self.pyre_deleteTrait(alias=name, locator=locator)
        # if this fails
        except self.TraitNotFoundError:
            # this must be a non-trait attribute
            super().__delattr__(name)

        # all done
        return

    # instantiation prep
    # compatibility check
    @classmethod
    def pyre_isCompatible(cls, spec, fast=True):
        """
        Check whether {cls} is assignment compatible with {spec}, i.e. whether it provides at
        least the properties and behaviors specified by {spec}
        """
        # chain up
        report = super().pyre_isCompatible(spec=spec, fast=fast)
        # if an incompatibility were detected and we are not interested in the full picture
        if fast and not report.isClean:
            # we are done
            return report

        # if {spec} is not a protocol
        if not spec.pyre_isProtocol:
            # we are done
            return report

        # grab my protocol
        protocol = cls.pyre_implements
        # if i don't have one, or i'm checking my own
        if not protocol or protocol == spec:
            # we are done
            return report

        # now, check that my protocol and {spec} are type compatible
        if not protocol.pyre_isTypeCompatible(spec):
            # build an error description
            error = cls.ProtocolCompatibilityError(configurable=cls, protocol=spec)
            # add it to the report
            report.incompatibilities[spec].append(error)
            # if we are in fast mode
            if fast:
                # bail out
                return report

        # all done
        return report


# end of file
