# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import itertools


# superclass
from .Executive import Executive


# class declaration
class Configurable(Executive):
    """
    The base class for components and interfaces

    This class provides storage for class attributes and a place to park utilities that are
    common to both components and interfaces
    """

    # types
    from .exceptions import FrameworkError, CategoryMismatchError, TraitNotFoundError


    # framework data; every class record gets a fresh set of these values
    pyre_key = None # the hash key issued by the nameserver
    pyre_pedigree = None # my ancestors that are configurables, in mro
    pyre_localTraits = None # the traits explicitly specified in my declaration
    pyre_inheritedTraits = None # the traits inherited from my superclasses
    pyre_namemap = None # the map of trait aliases to their canonical names
    pyre_traitmap = None # the map of trait names to trait descriptors
    pyre_locator = None # the location of the configurable declaration
    pyre_internal = True # mark this configurable as not visible to end users


    # introspection
    @property
    def pyre_name(self):
        """
        Look up my name
        """
        # if i don't have a registration key
        if self.pyre_key is None:
            # then, i don't have a name
            return None
        # otherwise, ask the nameserver
        _, name = self.pyre_executive.nameserver.lookup(self.pyre_key)
        # and return the registration name
        return name


    @property
    def pyre_familyKey(self):
        """
        Get my class registration key
        """
        return self.__class__.pyre_key


    @classmethod
    def pyre_family(cls):
        """
        Look up my family name
        """
        # if i don't have a key, i don't have a family
        if cls.pyre_key is None: return None
        # otherwise, ask the nameserver
        _, family = cls.pyre_executive.nameserver.lookup(cls.pyre_key)
        # and return the family name
        return family


    @classmethod
    def pyre_package(cls):
        """
        Deduce my package name
        """
        # get the name server
        ns = cls.pyre_executive.nameserver
        # if i don't have a key, i don't have a package
        if cls.pyre_key is None: return None
        # otherwise, ask the nameserver
        _, family = ns.lookup(cls.pyre_key)
        # split the family name apart; the package name is the zeroth entry
        pkgName = family.split(ns.separator)[0]
        # use it to look up the package
        return ns[pkgName]


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
    def pyre_configurables(cls):
        """
        Generate a sequence of all my trait descriptors that are marked as configurable.
        """
        return filter(lambda trait: trait.isConfigurable, cls.pyre_traits())


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
        incompatibility issue, without performing an exhaustive check of all traits. This is
        the default behavior. If {fast} is False, a thorough check of all traits will be
        performed resulting in a detailed compatibility report.
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
