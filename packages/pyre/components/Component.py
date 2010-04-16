# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Actor import Actor
from .Configurable import Configurable


class Component(Configurable, metaclass=Actor):
    """
    The base class for all components

    parameters:
      metaclass: the component class builder; override very carefully
      family: the component family name; used to specify settings shared by all instances
      core: a python object tha provides the actual implementation for my interface
      implements: the tuple of Interfaces i am assignment-compatible with

    Here is the sequence of events that occur when a component is declared:
      - Actor.__prepare__ (currently doesn't exist, so it is delegated to the ancestor)
        - Requirement.__prepare__
          - pyre.patterns.AttributeClassifier.__prepare__
            - instanstiates a cls._pyre_AttributeFilter, which is provided by the Requirement
              version
      - Actor.__new__
        - Requirement.__new__
          - pyre.patterns.AttributeClassifier.__new__
            - type.__new__
            - cls._pyre_buildCategoryIndex; provided by Requirement
              - create the embedded Inventory class
              - initialize its trait categorization
            - the category index is attached to the component class record
        - cls._pyre_buildImplementationSpecification; provided by Actor
        - _pyre_impelements is set
      - Actor.__init__
        - Requirement.__init__
          - pyre.patterns.AttributeClassifier.__init__ doesn't exist
            - pyre.patterns.AbstractMetaclass.__init__ swallows the kwds so type is happy
          - _pyre_family is set
          - _pyre_ancestors is set
        - _pyre_executive.registerComponentClass gets called

    Here is the sequence of events that occur when a component is instantiated:
      - Component.__init__
        - set the _pyre_name of the instance
        - builds _pyre_inventory as an instance of self._pyre_Inventory 
        - _pyre_executive.registerComponentInstance gets called
    """


# end of file 
