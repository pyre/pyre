# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from ..patterns.AttributeClassifier import AttributeClassifier


class Trait(AttributeClassifier.pyre_Descriptor):
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
    aliases = None # the set of alternative names by which I am accessible
    tip = None # a short description of my purpose and constraints; see doc below

    # framework data
    # predicate that indicates whether this trait is subject to runtime configuration
    pyre_isConfigurable = True


    # wire doc to __doc__ so the bultin help can decorate the attributes properly
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
    def pyre_initialize(self):
        """
        Look through the metadata harvested from the class declaration and perform any
        necessary cleanup
        """
        # update my aliases to include my canonical name
        self.aliases.add(self.name)
        # all done
        return self


    def pyre_embedLocal(self, component):
        """
        Build an association between this {configurable} and this locally declared trait
        """
        return self


    def pyre_embedInherited(self, component):
        """
        Build an association between this {configurable} and this inherited trait
        """
        return self


    def pyre_bindClass(self, configurable):
        """
        Resolve and convert the current value of this trait of {configurable} into my native type
        """
        return configurable


    def pyre_bindInstance(self, configurable):
        """
        Resolve and convert the current value of this trait of {configurable} into my native type
        """
        return configurable


    # meta methods
    def __init__(self, name=None, **kwds):
        super().__init__(name=name, **kwds)
        self.aliases = set()
        return


# end of file 
