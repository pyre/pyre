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
        # build the record;  this also assigns to {pyre_traits}
        configurable = super().__new__(
            cls, name, bases, attributes, descriptors="pyre_traits", **kwds)
        # extract the ancestors in the configurable's mro that are themeselves configurable
        # n.b.: since {Requirement} is not the direct metaclass of any class, the chain here
        # stops at either Component or Interface, depending on whether {Actor} or {Role} is the
        # actual metaclass
        configurable.pyre_pedigree = tuple(
            base for base in configurable.__mro__ if isinstance(base, cls))
        # normalize the local descriptors
        for descriptor in configurable.pyre_traits:
            descriptor.pyre_normalize(configurable)
        # embed all descriptors, both own and inherited
        for descriptor in configurable.pyre_getTraitDescriptors():
            descriptor.pyre_embed(configurable)
        # return the record to the caller
        return configurable
        

# end of file 
