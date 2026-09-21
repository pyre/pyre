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
            # record its family, for whoever lists it by specification
            self.families[item.pyre_name] = item.pyre_family()
            # and the component itself, for whoever wants to ask it more
            self.components[item.pyre_name] = item
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

    def record(self, document):
        """
        Store my sections in {document}, an editor of configuration files, leaving everything
        else in it as it is
        """
        # go through the sections
        for name, section in self.sections.items():
            # find where the document configures this component, however it spells the name
            path = document.find(name, section=True)
            # a component that is new to the document
            if path is None:
                # gets a top level section
                path = (name,)
            # go through the configured traits
            for trait, value in section.items():
                # and store each one in place
                document.set(*path, trait, value=value)
        # all done
        return document

    def save(self, uri):
        """
        Record my sections in the configuration file at {uri}, which need not exist yet
        """
        # get the editor factory
        from .yaml.Editor import Editor

        # open the document; one that does not exist yet starts out empty
        document = Editor(uri=uri)
        # record my sections
        self.record(document=document)
        # and write the document back, all at once
        return document.save()

    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # the sections, keyed by component name, in the order the components were met
        self.sections = {}
        # the families of the described components, keyed by name
        self.families = {}
        # and the components themselves
        self.components = {}
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
                        # a part the component owns is named after the trait that holds it,
                        # so its name leads the loader back to the very slot being bound
                        owned = value.pyre_name == f"{component.pyre_name}.{trait.name}"
                        # its family says all there is to say; anything else is specified
                        # in full, so the loader binds the same component
                        spec = value.pyre_family() if owned else value.pyre_spec
                        # a part without a family has nothing to record
                        if spec:
                            # the rest appear by specification
                            section[trait.name] = spec
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
        # a table travels as a table, entry by entry; the trait would render it whole as one
        # string, which a configuration file cannot tell from text
        if self._tabular(value=value):
            # so flatten it directly
            return self._flatten(value=value)
        # let the trait render everything else the way it knows how, e.g. paths and uris as
        # strings and tuples in the form the loader reads back
        rendered = trait.json(value)
        # and flatten whatever structure is left
        return self._flatten(value=rendered)

    def _tabular(self, value):
        """
        Check whether {value} is a table: a dictionary, or one of the framework's key maps
        """
        # anything with items to go through
        return isinstance(value, dict) or callable(getattr(value, "items", None))

    def _flatten(self, value):
        """
        Reduce {value} to scalars, lists, and tables of them
        """
        # scalars travel as they are
        if value is None or isinstance(value, (bool, int, float, str)):
            # untouched
            return value
        # tables, entry by entry
        if self._tabular(value=value):
            # with string keys
            return {str(key): self._flatten(value=item) for key, item in value.items()}
        # sequences of every kind become lists
        if isinstance(value, (list, tuple, set, frozenset)):
            # item by item
            return [self._flatten(value=item) for item in value]
        # anything else travels as its string form
        return str(value)


# end of file
