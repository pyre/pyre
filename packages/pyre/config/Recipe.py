# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the configuration of a component, as it was configured
class Recipe:
    """
    The configuration of components, and of everything they reference, as sections of plain
    values: what a configuration file would have to say to rebuild them

    Each section records the configured traits of one component, keyed by the component's
    name. Properties appear as plain values: scalars as they are, containers as lists, paths
    and uris as strings. Facilities appear as the specification, family and name, of the
    component they are bound to, which then gets a section of its own, so the recipe follows
    references until it has described everything the components lean on. Traits that took
    their default are left out, so the recipe says what was configured rather than freezing
    every default, and so are traits marked as not persistent, e.g. state a component derives
    at runtime and would derive again
    """

    # interface
    def add(self, component):
        """
        Describe {component} and everything it references
        """
        # the workload: the components still to describe
        workload = [component]
        # while there is work
        for item in workload:
            # a component described already contributes nothing more
            if item.pyre_name in self.sections:
                # so move on
                continue
            # describe it, collecting the components it references on the workload
            self.sections[item.pyre_name] = self._describe(component=item, workload=workload)
            # and record its family, for whoever lists it by specification
            self.families[item.pyre_name] = item.pyre_family()
        # all done
        return self

    def section(self, name):
        """
        Retrieve the section of the component called {name}, if it has one
        """
        # look it up
        return self.sections.get(name)

    def spec(self, name):
        """
        Build the specification, family and name, of the component called {name}
        """
        # get the family
        family = self.families.get(name)
        # a component without a family is specified by its name alone
        return name if not family else f"{family}#{name}"

    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # the sections, keyed by component name, in the order the components were met
        self.sections = {}
        # the families of the described components, keyed by name
        self.families = {}
        # all done
        return

    # implementation details
    def _describe(self, component, workload):
        """
        Build the section of {component}, adding the components it references to {workload}
        """
        # make the section
        section = {}
        # get the inventory
        inventory = component.pyre_inventory
        # go through the configurable traits
        for trait in component.pyre_configurables():
            # state the component derives at runtime is not configuration
            if not getattr(trait, "persistent", True):
                # so leave it out
                continue
            # find out whether the trait was configured; this must come before the value is
            # read, since reading a facility that is still unbound binds its default and
            # restamps the slot
            configured = self._configured(inventory=inventory, trait=trait)
            # then get the value
            value = inventory.getTraitValue(trait=trait)
            # facilities
            if trait.isFacility:
                # bound to a component
                if value is not None and hasattr(value, "pyre_name"):
                    # are followed, so what the component was configured with is described
                    workload.append(value)
                    # and appear by specification, when the binding itself was configured
                    if configured:
                        # so the loader binds the same component
                        section[trait.name] = value.pyre_spec
                # either way, move on
                continue
            # properties that took their default
            if not configured:
                # are left out
                continue
            # the rest appear as plain values
            section[trait.name] = self._plain(trait=trait, value=value)
        # hand off the section
        return section

    def _configured(self, inventory, trait):
        """
        Check whether the value of {trait} in {inventory} was assigned rather than defaulted
        """
        # get the priority of the last assignment
        priority = inventory.getTraitPriority(trait=trait)
        # a trait nobody touched has no priority, or one of the categories the framework
        # reserves for defaults
        return priority is not None and priority.name not in ("uninitialized", "defaults")

    def _plain(self, trait, value):
        """
        Reduce {value}, the value of {trait}, to plain values a configuration file can hold
        """
        # let the trait render what it knows how to, e.g. paths and uris as strings
        rendered = trait.json(value)
        # and flatten whatever structure is left
        return self._flatten(value=rendered)

    def _flatten(self, value):
        """
        Reduce {value} to scalars, lists, and tables of them
        """
        # scalars travel as they are
        if value is None or isinstance(value, (bool, int, float, str)):
            # untouched
            return value
        # tables, entry by entry
        if isinstance(value, dict):
            # with string keys
            return {str(key): self._flatten(value=item) for key, item in value.items()}
        # sequences of every kind become lists
        if isinstance(value, (list, tuple, set, frozenset)):
            # item by item
            return [self._flatten(value=item) for item in value]
        # anything else travels as its string form
        return str(value)


# end of file
