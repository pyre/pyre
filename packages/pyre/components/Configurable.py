# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import itertools


# superclass
from ..framework.Dashboard import Dashboard


# class declaration
class Configurable(Dashboard):
    """
    The base class for components and interfaces

    This class provides storage for class attributes and a place to park utilities that are
    common to both components and interfaces
    """

    # types
    from .exceptions import FrameworkError, CategoryMismatchError, TraitNotFoundError


    # framework data; every class record gets a fresh set of these values
    pyre_pedigree = None # my ancestors that are configurables, in mro
    pyre_localTraits = () # the traits explicitly specified in my declaration
    pyre_inheritedTraits = () # the traits inherited from my superclasses
    pyre_namemap = None # the map of trait aliases to their canonical names
    pyre_traitmap = None # the map of trait names to trait descriptors
    pyre_locator = None # the location of the configurable declaration
    pyre_internal = True # mark this configurable as not visible to end users


    # basic support for the help system
    def pyre_help(self, indent=' '*4, **kwds):
        """
        Hook for the application help system
        """
        # my summary
        yield from self.pyre_showSummary(indent=indent, **kwds)
        # my public state
        yield from self.pyre_showConfigurables(indent=indent, **kwds)
        # all done
        return


    def pyre_showSummary(self, indent, **kwds):
        """
        Generate a short description of what I do
        """
        # look for my docstring
        if self.__doc__:
            # split my docstring into lines
            for line in self.__doc__.splitlines():
                # indent each one and return it
                yield '{}{}'.format(indent, line.strip())
        # all done
        return


    def pyre_showConfigurables(self, indent='', **kwds):
        """
        Generate a description of my configurable state
        """
        # my public state
        public = []
        # collect them
        for trait in self.pyre_configurables():
            # get the name
            name = trait.name
            # get the type
            schema = trait.typename
            # and the tip
            tip = trait.tip or trait.doc
            # skip nameless undocumented ones
            if not name or not tip: continue
            # pile the rest
            public.append((name, schema, tip))

        # if we were able to find any trait info
        if public:
            # the {options} section
            yield 'options:'
            # figure out how much space we need
            width = max(len(name) for name,_,_ in public) + 2 # for the dashes
            # for each behavior
            for name, schema, tip in public:
                # show the details
                yield "{}{:>{}}: {} [{}]".format(indent, '--'+name, width, tip, schema)
            # leave some space
            yield ''
        # all done
        return


    def pyre_showBehaviors(self, spec, indent, **kwds):
        """
        Generate a description of my interface
        """
        # the pile of my behaviors
        behaviors = []
        # collect them
        for behavior in self.pyre_behaviors():
            # get the name
            name = behavior.name
            # get the tip
            tip = behavior.tip
            # if there is no tip, assume it is internal and skip it
            if not tip: continue
            # everything else gets saved
            behaviors.append((name, tip))

        # if we were able to find any usage information
        if behaviors:
            # the {usage} section
            yield 'usage:'
            # a banner with all the commands
            yield '{}{} [{}]'.format(
                indent, spec, " | ".join(name for name,_ in behaviors))
            # leave some space
            yield ''
            # the beginning of the section with more details
            yield 'where'
            # figure out how much space we need
            width = max(len(name) for name,_ in behaviors)
            # for each behavior
            for behavior, tip in behaviors:
                # show the details
                yield '{}{:>{}}: {}'.format(indent, behavior, width, tip)
            # leave some space
            yield ''
            # all done
            return


    # introspection
    @classmethod
    def pyre_traits(cls):
        """
        Generate a sequence of all my trait descriptors, both locally declared and inherited.
        If you are looking for the traits declared in a particular class, use the attribute
        {cls.pyre_localTraits} instead.
        """
        # the full set of my descriptors is prepared by {Requirement} and separated into two
        # piles: my local traits, i.e. traits that were first declared in my class record, and
        # traits that i inherited
        return itertools.chain(cls.pyre_localTraits, cls.pyre_inheritedTraits)


    @classmethod
    def pyre_behaviors(cls):
        """
        Generate a sequence of all my trait descriptors that are marked as configurable.
        """
        return filter(lambda trait: trait.isBehavior, cls.pyre_traits())


    @classmethod
    def pyre_configurables(cls):
        """
        Generate a sequence of all my trait descriptors that are marked as configurable.
        """
        return filter(lambda trait: trait.isConfigurable, cls.pyre_traits())


    @classmethod
    def pyre_localConfigurables(cls):
        """
        Generate a sequence of all my trait descriptors that are marked as configurable.
        """
        return filter(lambda trait: trait.isConfigurable, cls.pyre_localTraits)


    @classmethod
    def pyre_trait(cls, alias):
        """
        Given the name {alias}, locate and return the associated descriptor
        """
        # attempt to normalize the given name
        try:
            canonical = cls.pyre_namemap[alias]
        # not one of my traits
        except KeyError:
            # complain
            raise cls.TraitNotFoundError(configurable=cls, name=alias)
        # got it; look through my trait map for the descriptor
        try:
            # if there, get the accessor
            trait = cls.pyre_traitmap[canonical]
        # if not there
        except KeyError:
            # we have a bug
            import journal
            firewall = journal.firewall("pyre.components")
            raise firewall.log("UNREACHABLE")

        # return the trait
        return trait


    # framework notifications
    @classmethod
    def pyre_classRegistered(cls):
        """
        Hook that gets invoked by the framework after the class record has been registered but
        before any configuration events
        """
        # do nothing
        return cls


    @classmethod
    def pyre_classConfigured(cls):
        """
        Hook that gets invoked by the framework after the class record has been configured,
        before any instances have been created
        """
        # do nothing
        return cls


    @classmethod
    def pyre_classInitialized(cls):
        """
        Hook that gets invoked by the framework after the class record has been initialized,
        before any instances have been created
        """
        # do nothing
        return cls


    # compatibility check
    @classmethod
    def pyre_isCompatible(this, other, fast=False):
        """
        Check whether {this} is assignment compatible with {other}, i.e. whether it provides at
        least the properties and behaviors specified by {other}

        If {fast} is True, this method will return as soon as it encounters the first
        incompatibility issue, without performing an exhaustive check of all traits. If {fast}
        is False, a thorough check of all traits will be performed resulting in a detailed
        compatibility report.
        """
        # gain access to the report factory
        from .CompatibilityReport import CompatibilityReport
        # build an empty one
        report = CompatibilityReport(this, other)
        # iterate over the traits of {other}
        for hers in other.pyre_traits():
            # check existence
            try:
                # here is mine
                mine = this.pyre_traitmap[hers.name]
            # oops
            except KeyError:
                # build an error description
                error = this.TraitNotFoundError(configurable=this, name=hers.name)
                # add it to the report
                report.incompatibilities[hers].append(error)
                # bail out if we are in fast mode
                if fast: return report
                # otherwise move on to the next trait
                continue
            # are the two traits instances of compatible classes?
            if not issubclass(type(mine), type(hers)):
                # build an error description
                error = this.CategoryMismatchError(configurable=this, target=other, name=hers.name)
                # add it to the report
                report.incompatibilities[hers].append(error)
                # bail out if we are in fast mode
                if fast: return report
                # otherwise move on to the next trait
                continue
        # all done
        return report


# end of file
