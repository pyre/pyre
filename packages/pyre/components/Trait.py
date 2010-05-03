# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from ..patterns.Named import Named


class Trait(Named):
    """
    This is the base class for component features that form their public interface

    Traits extend the notion of a class attribute to an object that is capabable of
    capturing information about the attribute that has no natural resting place as part of a
    normal class declaration.

    Traits enable end-user configurable state, for both simple attributes and references to
    more elaborate objects, such as other components. Individual inventory items need a name
    that enables access to the associated information, per-instance actual storage for the
    attribute value, and additional meta data, such as reasonable default values when the
    attribute is not explictly given a value during configuration, and the set of constraints
    it should satisfy before it is considered a legal value.
    """


    # public data
    name = None # my canonical name; set at construction time or binding name
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
        return


    # meta methods
    def __init__(self, name=None, **kwds):
        super().__init__(name=name, **kwds)
        return


    # framework data
    _pyre_category = "traits"


# end of file 
