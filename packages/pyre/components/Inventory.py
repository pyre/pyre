# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class Inventory(object):
    """
    Storage and access to a component's traits

    This class is a seed: each class record built by Requirement has an attribute
    _pyre_Inventory that refers to an embedded class derived on the fly from all of its
    immediate ancestors' _pyre_Inventory classes. Configurable, the base class for components
    and interfaces, import this class as its _pyre_Inventory and establishes the embryonic
    case.

    Requirement further decorates these class records with attributes named after the canonical
    trait names of a component/interface whose values are the defaults as specified in the
    trait declaration. 

    At run time, component instances get a _pyre_inventory (note the capitalization) attribute
    that is an instance of the Inventory-derived class, where the per-instance values of the
    traits get stored.
    """

    # public data
    _pyre_namemap = None # map of my trait aliases to their canonical names built by Requirement 
    _pyre_categories = None # Requirement will attach my trait categories here 


# end of file 
