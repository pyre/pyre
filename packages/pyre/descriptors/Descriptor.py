# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# declaration
class Descriptor:
    """
    The base class for typed descriptors

    Descriptors are class data members that collect compile time meta-data about attributes.

    In pyre, classes that use descriptors typically have a non-trivial metaclass that harvests
    them and catalogs them. The base class that implements most of the harvesting logic is
    {pyre.patterns.AttributeClassifier}. The descriptors themselves are typically typed,
    because they play some kind of rôle during conversions between internal and external
    representations of data.
    """


# end of file 
