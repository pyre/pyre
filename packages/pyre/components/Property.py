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


    def pyre_validate(self, value):
        """
        Run the value through my validators
        """
        print("NYI: trait validation")
        return value


    def pyre_assign(self, node, value=None):
        """
        Assign {value} to {node} after making sure that it can be cast to the right type and
        passes the validation suite
        """
        # if the value is None, use the current value cache from {node}
        value = node._value if value is None else value
        # cast it
        value = self.pyre_cast(value)
        # validate it
        value = self.pyre_validate(value)
        # store it back with the variable
        node._value = value
        # and return the node
        return value


    # the descriptor interface
    # NYI: 
    #    these appear too raw to me
    #    where do casting and validation occur???
    def __set__(self, instance, value):
        """
        Set the trait of {instance} to {value}
        """
        node = getattr(instance._pyre_inventory, self.name)
        # update the value of the node in the instance inventory
        node.value = value
        # values could be literals, expressions, references, etc.
        # if this resulted in a literal value being deposited
        if node._value:
            # walk it through conversion and validation
            self.pyre_assign(node)
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
        # at this point, we have inventory, so look up the node using my name
        node = getattr(inventory, self.name)
        # check whether the node thinks it has a valid value
        ok = True if node._value else False
        # force an evaluation to take place
        value = node.value
        # if the value was previously cached
        if ok:
            # just return it
            return value
        # otherwise, walk it through conversion and validation
        return self.pyre_assign(node, value)


    # framework data
    _pyre_category = "properties"


# end of file 
