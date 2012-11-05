# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
from .. import schema


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


    # public data
    name = None # my name
    aliases = None # alternate names by which I am known to my client
    default = None # my default value
    schema = schema.identity # my type; most likely one of the {pyre.schema} type declarators
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


    # framework requests
    def attach(self, client, name):
        """
        Called by {client}, the class during whose declaration i was constructed, to let me
        know it is aware of me as an attribute with a canonical {name}
        """
        # set my canonical name
        self.name = name
        # update my aliases
        self.aliases.add(name)
        # and return
        return self


    # meta methods
    def __init__(self, default=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # the attributes that are likely to be known at construction time
        self.default = default
        # and the rest
        self.__doc__ = None
        self.aliases = set()
        # and return
        return


# end of file 
