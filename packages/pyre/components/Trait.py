# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from ..patterns.Named import Named


class Trait(Named):
    """
    """


    # public data
    name = None # my canonical name; set at construction time or binding name
    aliases = None # the set of alternative names by which I am accessible
    default = None # my default value
    optional = False # am i allowed to be uninitialized?
    converters = () # the chain of functions that are required to produce my native type
    constraints = () # the chain of functions that validate my values
    tip = None # a short description of my purpose and constraints; see doc below

    # wire doc to __doc__ so help can decorate properly without disturbing the trait declaration
    @property
    def doc(self):
        """
        Return my  documentation string
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
    def pyre_attach(self, configurable):
        """
        Attach me to the given {configurable} class record.

        This is invoked by pyre.components.Requirement while processing the trait declarations
        in {configurable} after the pyre_Inventory class has been inserted in the class
        dictionary. No instances of {configurable} can possibly exist at this point, so careful
        when looking through the {configurable} attributes.
        """
        # record the configurable that owns me
        self.pyre_configurable = configurable
        # access the namemap
        namemap = configurable._pyre_Inventory._pyre_namemap
        # map my name to my name
        namemap[self.name] = self.name
        # map my aliases
        for alias in self.aliases:
            namemap[alias] = self.name
        # and return
        return


    # meta methods
    def __init__(self, name=None, **kwds):
        super().__init__(name=name, **kwds)
        # initialize my aliases
        self.aliases = set()
        # and return
        return


    # the descriptor interface
    # NYI: 
    #    these appear too raw to me
    #    where do casting and validation occur???
    def __set__(self, instance, value):
        """
        Set the trait of {instance} to {value}
        """
        # update the value of the node in the instance inventory
        getattr(instance._pyre_inventory, self.name).value = value
        # all done
        return


    def __get__(self, instance, cls=None):
        """
        Get the value of this trait
        """
        try:
            # attempt to access the instance inventory
            inventory = instance._pyre_inventory
        except AttributeError:
            # access through a class variable; interpret as a request for the descriptor itself
            if cls and not instance:
                return self
            # otherwise, re-raise the error
            raise
        # at this point, we have inventory, so look up the attribute using my name an return it
        return getattr(inventory, self.name).value


    # private data
    pyre_configurable = None
    _pyre_category = "traits"


# end of file 
