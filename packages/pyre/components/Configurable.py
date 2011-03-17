# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import itertools


class Configurable:
    """
    The base class for components and interfaces

    This class provides storage for class attributes and a place to park utilities that are
    common to both components and interfaces
    """


    # constant
    pyre_SEPARATOR = '.'


    # access to the framework executive; patched during framework boot
    pyre_executive = None

    # framework data; patched up by metaclasses and the framework bootstrapping
    pyre_name = None # my public id
    pyre_namemap = None # a map of descriptor aliases to their canonical names
    pyre_localTraits = None # a tuple of all the traits in my declaration
    pyre_inheritedTraits = None # a tuple of all the traits inherited from my superclasses
    pyre_pedigree = None # a tuple of ancestors that are themselves configurables
    pyre_hidden = True # true


    # framework notifications
    @classmethod
    def pyre_registerClass(cls, executive):
        """
        Hook that gets invoked by the framework after the class record has been registered but
        before any configuration events
        """
        return


    @classmethod
    def pyre_configureClass(cls, executive):
        """
        Hook that gets invoked by the framework after the class record has been configured,
        before any instances have been created
        """
        return


    @classmethod
    def pyre_initializeClass(cls, executive):
        """
        Hook that gets invoked by the framework after the class record has been initialized,
        before any instances have been created
        """
        return


    # introspection interface
    @classmethod
    def pyre_getTraitDescriptors(cls):
        """
        Generate a sequence of all my trait descriptors

        The only complexity here is proper shadowing in the presence of inheritance. If you are
        looking for the traits declared in a particular class, use the attribute
        {cls.pyre_traits} instead.
        """
        # the full set of my descriptors is prepared by {Requirement} and separated into two
        # piles: my local traits, i.e. traits that were first declared in my class record, and
        # traits that i inherited
        return itertools.chain(cls.pyre_localTraits, cls.pyre_inheritedTraits)


    @classmethod
    def pyre_getTraitDescriptor(cls, alias):
        """
        Given the name {alias}, locate and return the canonical name, descriptor and base class
        where the descriptor was declared
        """
        # attempt to normalize the given name
        try:
            canonical = cls.pyre_namemap[alias]
        # not one of my traits
        except KeyError:
            raise cls.TraitNotFoundError(configurable=cls, name=alias)
        # got it; look through my ancestors' dictionaries for the descriptor
        for base in cls.pyre_pedigree:
            # attempt to look it up in this base
            try:
                return base.__dict__[canonical]
            # not here; move on
            except KeyError:
                pass
        # impossible
        import journal
        firewall = journal.firewall("pyre.components")
        raise firewall.log("UNREACHABLE")


    def pyre_getTraitFullName(self, name):
        """
        Build the full name of the given trait
        """
        return self.pyre_SEPARATOR.join(filter(None, [self.pyre_name, name]))


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
        # collect my traits
        myTraits = { trait.name: trait for trait in this.pyre_getTraitDescriptors() }
        # iterate over the traits of {other}
        for hers in other.pyre_getTraitDescriptors():
            # check existence
            try:
                # here is mine
                mine = myTraits[hers.name]
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
            if not issubclass(mine.__class__, hers.__class__):
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


    # exceptions
    from .exceptions  import CategoryMismatchError, TraitNotFoundError
                

# end of file 
