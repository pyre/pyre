# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


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
    {pyre.patterns.AttributeClassifier}. The descriptors themselves are typically typed,
    because they play some kind of rôle during conversions between internal and external
    representations of data.
    """


    # types
    from ..schema import identity


    # public data
    name = None # my name
    aliases = None # alternate names by which I am known to my client
    default = None # my default value
    schema = identity # my type; most likely one of the {pyre.schema} type declarators
    tip = None # a short description of my purpose

    # wire doc to __doc__ so the bultin help can decorate the attributes properly
    @property
    def doc(self):
        """
        Return my documentation string
        """
        return self.__doc__

    @doc.setter
    def doc(self, text):
        """
        Store text as my documentation string
        """
        self.__doc__ = text
        return


    # interface
    def coerce(self, **kwds):
        # not much to do; just pass it on to my schema
        return self.schema.coerce(**kwds)


    # meta methods
    def __init__(self, name=None, default=None, schema=identity, doc=None, **kwds):
        # chain up
        super().__init__(**kwds)

        # the attributes that are likely to be known at construction time
        self.name = name
        self.default = default
        self.schema = schema
        self.__doc__ = doc

        # and the rest
        self.aliases = set() if name is None else { name }

        # and return
        return


    def __get__(self, instance, cls):
        """
        Retrieve the value of this descriptor from the client
        """
        # don't know what to do
        raise NotImplementedError(
            "descriptor {.__name__!r} does not support '__get__'".format(type(self)))


    def __set__(self, client, value):
        """
        Set the value of this descriptor for a configurable instance 
        """
        # don't know what to do
        raise NotImplementedError(
            "descriptor {.__name__!r} does not support '__set__'".format(type(self)))


# end of file 
