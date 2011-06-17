# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Object import Object


# declaration
class Descriptor:
    """
    The base class for typed descriptors

    Descriptors are class data members that enable special processing to occur whenever they
    are accessed as attributes of class instances. For example, descriptors that define the
    methods __get__ and __set__ are recognized by the python interpreter as data access
    interceptors. 

    In pyre, classes that use descriptors typically have a non-trivial metaclass that harvests
    them and catalogs them. The base class that implements most of the harvesting logic is
    {pyre.patterns.AttributeClassifier}. The descriptors themselves are typically typed, because
    they play some kind of rôle during conversions between internal and external
    representations of data.
    """


    # class public data
    name = None # my name
    default = None # my default value
    optional = False # am i allowed to be uninitialized?
    type = Object # my type; most likely one of the pyre.schema type declarators
    validators = () # the chain of functions that inspect and validate my value
    converters = () # the chain of transformations necessary to produce a value in my native type


# end of file 
