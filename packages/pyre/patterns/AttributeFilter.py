# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .Type import Type


# declaration
class AttributeFilter(Type):
    """
    A base metaclass that enables attribute classification.

    A common pattern in pyre is to define classes that contain special attributes that collect
    declarative metadata. These attributes are processed by special purpose metaclasses and
    are converted into appropriate behavior. For example, components have properties, which are
    decorated descriptors that enable external configuration of component state. Similarly, XML
    parsing happens with the aid of classes that capture the syntax, semantics and processing
    behavior of tags by employing descriptors to capture the layout of an XML document.
    """


    # interface
    @classmethod
    def pyre_harvest(cls, attributes, descriptor):
        """
        Examine the class {attributes}, looking for instances of {descriptor}
        """
        # go through the attributes
        for name, attribute in attributes.items():
            # if this is a {descriptor} instance that;s not the in the reserved list
            if isinstance(attribute, descriptor) and not cls.pyre_isReserved(name):
                # pass it on
                yield name, attribute
        # all done
        return


    @classmethod
    def pyre_isReserved(cls, name):
        """
        Exclude reserved names from this process
        """
        # by default, look in a set of such names
        return name in cls.pyre_reservedNames


    # public data
    # names excluded from filtering
    pyre_reservedNames = set()


# end of file
