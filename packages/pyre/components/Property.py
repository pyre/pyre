# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Trait import Trait


class Property(Trait):
    """
    Base class for propery descriptors

    Most properties take simple objects as their values, and therefore do not present any
    serious challenges from a configuration/initialization point of view. However, properties
    that represent acquired resources, such as file or network streams, may require complex
    initialization. The needs of the former are probably taken care of by this class in their
    entirety, whereas the latter may require more specialized descriptors.
    """

    # import the schema
    import pyre.schema as schema


    # public data
    name = None # my canonical name; set at construction time or binding name
    type = schema.object # my type; most likely one of the pyre.schema type declarators
    aliases = None # the set of alternative names by which I am accessible
    default = None # my default value
    optional = False # am i allowed to be uninitialized?
    converters = () # the chain of functions that are required to produce my native type
    constraints = () # the chain of functions that validate my values
    tip = None # a short description of my purpose and constraints; see doc below


    # interface 
    def pyre_attach(self, configurable):
        """
        Attach me to the given {configurable} class record.

        This is invoked by pyre.components.Requirement while processing the trait declarations
        in {configurable} after the pyre_Inventory class has been inserted in the class
        dictionary. No instances of {configurable} can possibly exist at this point, so careful
        when looking through the {configurable} attributes.
        """
        # access the namemap
        namemap = configurable._pyre_Inventory._pyre_namemap
        # map my aliases
        for alias in self.aliases:
            namemap[alias] = self.name
        # and return
        return


    def pyre_cast(self, value):
        """
        Convert {value} to the trait native type
        """
        return self.type.cast(value)


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
            # access through a class variable
            inventory = cls._pyre_Inventory
        # at this point, we have inventory, so look up the attribute using my name an return it
        return getattr(inventory, self.name).value


    # framework data
    _pyre_category = "properties"


# end of file 
