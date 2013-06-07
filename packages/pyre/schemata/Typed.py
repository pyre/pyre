# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# declaration
class Typed:
    """
    A class decorator that embeds type decorated subclasses whose names match their {typename}
    """


    # the list of types that i will use to decorate my client
    from . import schemata


    # meta-methods
    def __new__(cls, record=None, schemata=schemata, **kwds):
        """
        Trap use without an argument list and do the right thing
        """
        # if used without an argument, i get {record} at construction time
        if record is not None:
            # decorate it and return it; because the type returned doesn't match my type, the
            # constructor does not get invoked
            return cls.build(client=record)
        # otherwise, do the normal thing
        return super().__new__(cls, **kwds)

        
    def __init__(self, record=None, schemata=schemata, **kwds):
        """
        Build an instance of this decorator.
        """
        # the parameter {record} is not used; it is present only because it must be removed
        # from {kwds} before chaining up
        super().__init__(**kwds)
        # save my schemata
        self.schemata = schemata
        # all done
        return


    def __call__(self, client):
        """
        Build a class record
        """
        # delegate to my implementation
        return self.build(client=client, schemata=self.schemata)


    # implementation details
    @classmethod
    def build(cls, client, schemata=schemata):
        """
        Embed within {client} subclasses of its direct ancestor that also derive from the types in
        my {schemata}
        """
        # go through all the schemata
        for schema in schemata:
            # first, let's build the tuple of base classes; if the client provides a mixin
            # class to be included in the hierarchy
            try:
                # get it
                mixin = getattr(client, schema.typename)
            # if not
            except AttributeError:
                # inherit from the client and the schema
                ancestors = (client, schema)
            # if it's there
            else:
                # inherit from all three
                ancestors = (client, mixin, schema)
           
            # document it
            doc = "a subclass of {!r} of type {!r}".format(client.__name__, schema.typename)
            # build the class: name it after the schema, add the docstring
            typedClient = type(schema.typename, ancestors, {"__doc__": doc})
            # and attach it to the client
            setattr(client, schema.typename, typedClient)
            
        # return the new class record
        return client


# end of file
