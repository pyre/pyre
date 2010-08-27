# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import collections
from .Named import Named
from .AbstractMetaclass import AbstractMetaclass


class AttributeClassifier(AbstractMetaclass):
    """
    A base metaclass that enables attribute categorization.

    A common pattern in pyre is to define classes that contain special attributes whose purpose
    is to collect declaration meta data and associate them with a class attribute. These
    attributes are processed by metaclasses and are converted into appropriate behavior. For
    example, components have properties, which are decorated descriptors that enable external
    configuration of component state. Similarly, XML parsing happens with the aid of classes
    that capture the syntax, semantics and processing behavior of tags by employing descriptors
    to capture the layout of an XML document.

    This class defines {pyre_Descriptor}, which is meant to be used as the base class for these
    special attributes. Instances of subclasses of {pyre_Descriptor} found in the class
    declaration record are collected in the ordered they were encountered and are made
    available to AttributeClassifier subclasses for proecessing. Subclasses can override
    {_pyre_decorateRecord} to provide specialized processing. They may also override
    {_pyre_identifyDescriptors} if their descriptor identification needs are more complex that
    what is implemented here.

    This metaclass overrides {__prepare__} to provide attribute storage that records the order in
    which attributes were encountered in the class record.
    """


    # meta methods
    @classmethod
    def __prepare__(cls, name, bases, **kwds):
        """
        Build an attribute table that maintains a category index for attribute descriptors
        """
        return collections.OrderedDict()


    def __new__(cls, name, bases, attributes, *, descriptors, **kwds):
        """
        Build the class record

        parameters:
          {cls}: the metaclass invoked; guaranteed to be an AttributeClassifier descendant
          {name}: the name of the class being built
          {bases}: the tuple of base class records
          {attributes}: a dictionry of attribute names and values
          {descriptors}: the name of the variable that will hold the list of trait descriptors
        """
        # initialize the list of descriptors
        harvest = []
        # loop over the attributes
        for attrname, attribute in attributes.items():
            # for attributes that are descriptors
            if isinstance(attribute, cls.pyre_Descriptor):
                # set their name
                attribute.name = attrname
                # add them to the pile
                harvest.append(attribute)
        # save the descriptor tuple as a class attribute
        attributes[descriptors] = tuple(harvest)
        # let type build the new record; build and hand it a new dictionary for the attributes
        record = super().__new__(cls, name, bases, dict(attributes))
        # return the class record
        return record


    # helper
    class pyre_Descriptor(Named):
        """
        The base class for classifiable attributes
        """


# end of file 
