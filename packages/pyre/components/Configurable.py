# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import itertools
from .Requirement import Requirement


class Configurable(object): #, metaclass=Requirement):
    """
    The base class for framework configurable classes

    This class provides storage for class attributes and a place to park utilities that are
    common to both components and interfaces
    """


    # framework data
    _pyre_name = None # the instance name
    _pyre_state = None # track progress through the bootsrapping process
    _pyre_configurables = None # a tuple of all my ancestors that derive from Configurable
    _pyre_traits = None # a list of all the traits in my declaration


    # constants
    # update these when new categories are added
    _pyre_NONCONFIGURABLE_TRAITS = {"behaviors"}
    _pyre_CONFIGURABLE_TRAITS = {"properties", "faiclities"}


    # trait access
    @classmethod
    def pyre_traits(cls, mine=True, inherited=True, categories=None):
        """
        Iterate over all my traits that meet the given criteria and return a typle containing
        the trait and the configurable that declares it
        """
        # initialize the trait name cache
        # we cache the trait names that have been encountered already so we can shadow properly
        # the traits declared by ancestors that are redefined by this class
        known = set()
        # start with the traits defined by this class
        for trait in cls._pyre_traits:
            # add the name to the cache
            known.add(trait.name)
            # see whether we should yield this one
            # move on if we are skipping my local traits
            if not mine: continue
            # move on if we are checking categories and this trait is not in the right one
            if categories and trait._pyre_category not in categories: continue
            # otherwise yield it
            yield trait, cls

        # process the ancestors?
        if not inherited: return

        # iterate over all ancestors that have traits
        for ancestor in cls._pyre_configurables[1:]:
            # iterate over all the registered traits
            for trait in ancestor._pyre_traits:
                # if this name is known skip it
                if trait.name in known: continue
                # otherwise add it to the pile
                known.add(trait.name)
                # move on if we are checking categories and this one is not in the right group
                if categories and trait._pyre_category not in categories: continue
                # otherwise yield it
                yield trait, ancestor

        # all done
        return


    @classmethod
    def pyre_getTraitDescriptor(cls, name):
        """
        Attempt to retrieve the trait descriptor associated with {name}
        """
        # walk through the traits
        for trait,source in cls.pyre_traits():
            # if the name matches
            if trait.name == name:
                # success
                return trait
        # otherwise return failure
        return


    # compatibility checks
    @classmethod
    def pyre_isCompatible(this, other, createReport=False):
        """
        Check whether {this} is assignment compatible with {other}, i.e. it provides the same
        properties and behaviors as specified by {other}

        If {createReport} is False, this method will return failure when the first
        compatibility issue is detected, without performing an exhaustive check of all
        traits. If {createReport} is True, it will perform a thorough check of all traits and
        build a compatibility report
        """
        # checking for an inheritance relationship between this and other is not sufficient:
        # assignment compatible configurables do not have to derive from one another
        # also, the existence of a trait with the correct name is not sufficient either; we
        # must verify that it is of the correct category as well

        # get access to the compatibility report object
        from .CompatibilityReport import CompatibilityReport
        # and build an instance
        report = CompatibilityReport(this, other)
        # collect my traits
        myTraits = { trait.name: trait for trait,source in this.pyre_traits() }
        # iterate over hers
        for trait,origin in other.pyre_traits():
            # check existence
            try:
                mine = myTraits[trait.name]
            except KeyError:
                # build an error description
                error = this.TraitNotFoundError(configurable=this, name=trait.name)
                # add it to the report
                report.incompatibilities[trait].append(error)
                # bail out if we are not performing a thorough check
                if not createReport:
                    return report
                # otherwise, move on
                continue
            # check categories for a match
            if mine._pyre_category != trait._pyre_category:
                # build an error description
                error = this.CategoryMismatchError(configurable=this, target=other, name=trait.name)
                # add it to the report
                report.incompatibilities[trait].append(error)
                report.incompatibilities[trait].append(error)
                # bail out if we are not performing a thorough check
                if not createReport:
                    return report
                # otherwise, move on
                continue
            # skip the rest of the checks if the trait is a behavior
            if trait._pyre_category == "behavior":
                continue
            # check trait type
            print("NYI: Configurable.pyre_isCompatible: check trait type")

        # all done
        return report
    

    # other utilities
    @classmethod
    def pyre_normalizeName(cls, name):
        """
        Convert the given trait name or alias to the canonical one
        """
        # iterate over my ancestors
        for ancestor in cls._pyre_configurables:
            # look up the name in the namemap
            try:
                return ancestor._pyre_Inventory._pyre_namemap[name]
            except KeyError:
                continue

        raise cls.TraitNotFoundError(configurable=cls, name=name)


    # exceptions
    from . import CategoryMismatchError, TraitNotFoundError


# end of file 
