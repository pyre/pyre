# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
from .. import tracking
# superclass
from ..patterns.AttributeClassifier import AttributeClassifier


# class declaration
class Requirement(AttributeClassifier):
    """
    Metaclass that enables the harvesting of trait declarations

    This class captures the class record processing that is common to both interfaces and
    components. Given a declaration record, {Requirement}

    * discovers the bases classes that are configurables
    * identifies the specially marked attributes
    * creates the namemap that handles trait name aliasing
    """

    # the presence of a family/component name determines the slot storage strategy: if a
    # configurable is to be registered with the nameserver, it delegates storage of its slot to
    # it, which allows me to maintain only one slot for each component trait. if a configurable
    # is not registered, its slots are kept in its pyre_inventory. slotted traits know how to
    # retrieve the slots for each kind

    # at one point, i tossed around the idea of introducing accessors to handle the different
    # strategies for storing slots. it turned out to be very tricky to do it that way: each
    # class in the inheritance graph had to get its own accessors for all its slots, both local
    # and inherited, which made support for shadowing very tricky.

    # types
    from ..traits.Trait import Trait


    # meta-methods
    def __new__(cls, name, bases, attributes, *, internal=False, **kwds):
        """
        Build the class record for a new configurable

        This metaclass handles the record building steps common to components and protocols,
        whose metaclasses are subclasses of {Requirement}. It initializes the class record so
        that it matches the layout of {Configurable}, the base class of {Component} and
        {Protocol}.
        """
        # my local traits
        # access to my name maps
        namemap = {}
        traitmap = {}

        # initialize the class attributes explicitly
        attributes['pyre_pedigree'] = ()
        attributes["pyre_localTraits"] = ()
        attributes['pyre_inheritedTraits'] = ()
        attributes['pyre_namemap'] = namemap
        attributes['pyre_traitmap'] = traitmap
        attributes['pyre_internal'] = internal

        # build the record
        configurable = super().__new__(cls, name, bases, attributes, **kwds)

        # harvest the local traits
        configurable.pyre_localTraits = tuple(
            configurable.pyre_getLocalTraits(attributes))

        # harvest the inherited traits: this must be done from scratch for every new
        # configurable class, since multiple inheritance messes with the __mro__; 
        configurable.pyre_inheritedTraits = tuple(
            configurable.pyre_getInheritedTraits(shadowed=set(attributes)))
            
        # extract the ancestors listed in the mro of the configurable that are themselves
        # configurable; N.B.: since {Requirement} is not the direct metaclass of any class, the
        # chain here stops at either {Component} or {Protocol}, depending on whether {Actor}
        # or {Role} is the actual metaclass
        pedigree = tuple(base for base in configurable.__mro__ if isinstance(base, cls))
        # attach it to the configurable
        configurable.pyre_pedigree = pedigree

        # adjust the name maps; the local variables are tied to the class attribute
        # N.B. this assumes that the traits have been initialized, which updates the {aliases}
        # to include the canonical name of the trait
        for trait in configurable.pyre_traits():
            # update the trait map
            traitmap[trait.name] = trait
            # update the namemap with all aliases of each trait
            namemap.update({alias: trait.name for alias in trait.aliases})

        # return the class record to the caller
        return configurable


    # support for decorating components and protocols
    def pyre_getLocalTraits(self, attributes):
        """
        Scan the dictionary {attributes} for trait descriptors
        """
        # examine the attributes and harvest the trait descriptors
        for name, trait in self.pyre_harvest(attributes=attributes, descriptor=self.Trait):
            # establish my association with my trait
            trait.attach(client=self, name=name)
            # add it to the pile
            yield trait
        # all done
        return


    def pyre_getInheritedTraits(self, shadowed):
        """
        Look through the ancestors of {configurable} for traits whose name are not members of
        {shadowed}, the set of names that are inaccessible.
        """
        # my metaclass
        metaclass = type(self)
        # for each superclass of configurable
        for base in self.__mro__[1:]:
            # only other configurables have traits
            if isinstance(base, metaclass):
                # go through the traits local in base
                for trait in base.pyre_localTraits:
                    # skip it if something else by the same name is already known
                    if trait.name in shadowed: continue
                    # otherwise, save it
                    yield trait
            # in any case, add all the local attribute names onto the known pile
            shadowed.update(base.__dict__)
        # all done
        return


# end of file 
