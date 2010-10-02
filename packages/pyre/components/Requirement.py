# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Configurable import Configurable
from ..patterns.AttributeClassifier import AttributeClassifier


class Requirement(AttributeClassifier):
    """
    Metaclass that enables the harvesting of trait declarations

    This class captures the class record processing that is common to both interfaces and
    components. Given a declaration record, {Requirement}

    * discovers the bases classes that are configurables
    * identifies the specially marked attributes
    * creates the namemap that handles trait name aliasing
    """


    # constants
    pyre_SEPARATOR = Configurable.pyre_SEPARATOR

    # framework data
    # access to the framework executive; patched by the bootstrapping code in pyre/__init__.py
    pyre_executive = None


    # meta methods
    def __new__(cls, name, bases, attributes, **kwds):
        """
        Build a new configurable class record

        This class handles the steps common to all classes that derived from {Configurable}
        """
        # set the name so it is always available
        attributes["pyre_name"] = name
        # add the state attribute to the pile
        # this must be done very early so that __setattr__ below doesn't trigger as the class
        # record is being decorated; and it must be done for every new class, since the
        # ancestor's pyre_state is immediately available to subclasses
        attributes["pyre_state"] = None
        # create storage for the configurable state
        attributes["pyre_inventory"] = {}
        # initialize the namemap
        attributes["pyre_namemap"] = {}
        # build the record
        # also, build a tuple of the locally declared traits in {pyre_localTraits}
        configurable = super().__new__(
            cls, name, bases, attributes, descriptors="pyre_localTraits", **kwds)

        # initialize the locally declared descriptors
        for descriptor in configurable.pyre_localTraits:
            descriptor.pyre_initialize()

        # harvest the inherited traits: this must be done from scratch for every new
        # configurable class, since multiple inheritance messes with the __mro__ in
        # unpredictable ways
        # initialize the set of known names so we shadow them properly
        known = set(attributes)
        # initialize the trait accumulator
        inheritedTraits = []
        # iterate over the configurable's ancestors
        for base in configurable.__mro__[1:]:
            # only other configurables have traits
            if isinstance(base, cls):
                # loop over the traits in base
                for trait in base.pyre_localTraits:
                    # skip it if its something else by this name has been seen before
                    if trait.name in known: continue
                    # otherwise save it
                    inheritedTraits.append(trait)
            # in any case, add all the local attribute names onto the known pile
            known.update(base.__dict__)
        # attach the harvested traits to the class record
        configurable.pyre_inheritedTraits = tuple(inheritedTraits)
            
        # extract the ancestors in the configurable's mro that are themeselves configurable
        # n.b.: since {Requirement} is not the direct metaclass of any class, the chain here
        # stops at either Component or Interface, depending on whether {Actor} or {Role} is the
        # actual metaclass
        configurable.pyre_pedigree = tuple(
            base for base in configurable.__mro__ if isinstance(base, cls))

        # fix the namemap
        for trait in configurable.pyre_getTraitDescriptors():
            # update the name map with all the aliases of each trait
            configurable.pyre_namemap.update({alias: trait.name for alias in trait.aliases})

        # return the record to the caller
        return configurable
        

# end of file 
