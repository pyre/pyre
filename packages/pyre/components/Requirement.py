# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
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


    # types
    from .Trait import Trait

    # framework data
    # access to the framework executive; patched by the bootstrapping code in pyre/__init__.py
    pyre_executive = None


    # meta methods
    def __new__(cls, name, bases, attributes, *, family=None, **kwds):
        """
        Build a new configurable class record

        This class handles the steps common to all classes that derived from {Configurable}
        """
        # set the name so it is always available
        attributes["pyre_name"] = name
        # record the public name
        attributes["pyre_family"] = family.split(cls.pyre_SEPARATOR) if family else []
        # initialize the namemap
        attributes["pyre_namemap"] = {}
        # the locally declared traits
        attributes["pyre_localTraits"] = localTraits = []
        # the inherited traits
        attributes["pyre_inheritedTraits"] = inheritedTraits = []
        # and the list of ancestors that are themselves configurables
        attributes["pyre_pedigree"] = pedigree = []

        # extract the descriptors
        for traitname, trait in cls.pyre_harvest(attributes, cls.Trait):
            # set the name of the trait as seen in the declaration
            trait.name = traitname
            # and add it to the pile of local traits
            localTraits.append(trait)

        # build the record
        configurable = super().__new__(cls, name, bases, dict(attributes), **kwds)

        # harvest the inherited traits: this must be done from scratch for every new
        # configurable class, since multiple inheritance messes with the __mro__ in
        # unpredictable ways
        # the code fragment appends directly to the local variable that points to the same list
        # as the configurable attribute
        # initialize the set of known names so we shadow them properly
        known = set(attributes)
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
            
        # extract the ancestors in the configurable's mro that are themeselves configurable
        # n.b.: since {Requirement} is not the direct metaclass of any class, the chain here
        # stops at either Component or Interface, depending on whether {Actor} or {Role} is the
        # actual metaclass
        for base in configurable.__mro__:
            if isinstance(base, cls): pedigree.append(base)

        # initialize the locally declared descriptors
        for descriptor in localTraits:
            descriptor.pyre_initialize()
        # fix the namemap
        for trait in configurable.pyre_getTraitDescriptors():
            # update the name map with all the aliases of each trait
            configurable.pyre_namemap.update({alias: trait.name for alias in trait.aliases})

        # return the record to the caller
        return configurable
        

# end of file 
