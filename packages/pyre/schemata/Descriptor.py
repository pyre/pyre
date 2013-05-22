# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import collections
# superclass
from .Type import Type


# declaration
class Descriptor(Type):
    """
    The base class for typed descriptors

    Descriptors are class data members that enable special processing to occur whenever they
    are accessed as attributes of class instances. For example, descriptors that define the
    methods {__get__} and {__set__} are recognized by the python interpreter as data access
    interceptors.

    In pyre, classes that use descriptors typically have a non-trivial metaclass that harvests
    them and catalogs them. The base class that implements most of the harvesting logic is
    {pyre.patterns.AttributeClassifier}. The descriptors themselves are typically typed,
    because they play some kind of rôle during conversions between internal and external
    representations of data.
    """


    # types
    from .Object import Object as identity


    # public data
    name = None # my name
    default = None # my default value
    aliases = None # alternate names by which I am known to my client
    schema = identity # my type; most likely one of the type declarators in this package
    # documentation support
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
    def coerce(self, value, **kwds):
        """
        Walk {value} through value coercion
        """
        # {None} is special; leave it alone
        if value is None: return None
        # otherwise, convert
        for converter in self.converters: value = converter(value)
        # cast
        value = self.schema.coerce(value, **kwds)
        # normalize
        for normalizer in self.normalizers: value = normalizer(value)
        # validate
        for validator in self.validators: value = validator(value)
        # and return the new value
        return value


    # framework requests
    def attach(self, client, name):
        """
        Called by {client}, the class during whose declaration i was constructed, to let me
        know it is aware of me as an attribute with a canonical {name}
        """
        # set my canonical name
        self.name = name
        # update my aliases: easy access to all the names by which I am known
        self.aliases.add(name)

        # normalize my converters
        self.converters = self.listify(self.converters)
        # my normalizers
        self.normalizers = self.listify(self.normalizers)
        # and my validators
        self.validators = self.listify(self.validators)

        # and return
        return self


    # meta methods
    def __init__(self, default=default, **kwds):
        # chain up
        super().__init__(**kwds)

        # N.B.: in most cases, {schema} is a class variable, so don't set it here; facilities
        # are an exception to this: they use {schema} to record their protocols.

        # the attributes that are likely to be known at construction time
        self.default = default
        # initialize the rest
        self.__doc__ = None
        self.aliases = set()

        # initialize my value processors
        self.converters = []
        self.normalizers = []
        self.validators = []

        # and return
        return


    # implementation details
    def listify(self, processors):
        """
        Make sure {processors} is an iterable regardless of what the user left behind
        """
        # handle anything empty
        if not processors: return []
        # if i have an iterable
        if isinstance(processors, collections.Iterable):
            # turn it into a list
            return list(processors)
        # otherwise, place the lone processor in a list
        return [processors]


# end of file 
