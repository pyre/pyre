# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from ..patterns.AttributeClassifier import AttributeClassifier


class DTD(AttributeClassifier):
    """
    Metaclass that scans the class record of a Document descendant for element descriptors and
    builds the necessary machinery for parsing the XML document
    """


    # contants
    _pyre_DTD = "dtd" # the name of the attribute that holds the attribute index
    _pyre_CLASSIFIER_NAME = "_pyre_category" # the location of index key


    # meta methods
    @classmethod
    def __prepare__(cls, name, bases, **kwds):
        """
        Create and return a container for the attributes in the class record
        """
        return super().__prepare__(name, bases, classifier=cls._pyre_CLASSIFIER_NAME, **kwds)


    def __new__(cls, name, bases, attributes, **kwds):
        """
        Build the document class record
        """
        return super().__new__(cls, name, bases, attributes, index=cls._pyre_DTD, **kwds)


    @classmethod
    def _pyre_buildCategoryIndex(cls, record, index, attributes):
        """
        Attach the category index to the class record as the attribute index

        parameters:
            {record}: the class record being decorated
            {index}: the name of the attribute that will hold the category index
            {attributes}: storage for the category index
        """
        # extract the element descriptors from the attribute categories
        descriptors = tuple(attributes.categories["elements"])

        # namespaces introduce a bit of complexity. unless it turns out to be inconsistent with
        # the rules, here is the strategy: if a nested element is in the same namespace as its
        # direct parent, it goes into the _pyre_nodeIndex. otherwise it goes into the
        # _pyre_nodeQIndex of namespace qualified tags
        
        # in the Reader, {start|end}Element look up tags directly in the _pyre_nodeIndex, which
        # is the only possible implementation since there is no additional information
        # available beyond the tag name. this is equivalent to assuming that the nested tag
        # belongs to the same namespace. the namespace qualified hooks {start|end}ElementNS
        # need a slightly modified approach: if the namespace given matches the namespace of
        # the parent tag, look in _pyre_nodeIndex; if not look it up in _pyre_nodeQIndex

        # build a (descriptor name -> handler) map
        index = { descriptor.name: descriptor for descriptor in descriptors }

        # now, build the dtd for each handler 
        for element in descriptors:
            # get the class that handles this element
            handler = element.handler
            # initialize the class attributes
            handler.tag = element.name
            handler._pyre_nodeIndex = {}
            handler._pyre_nodeQIndex = {}
            # build the nested element indices
            for tag in handler.elements:
                # get the nestling handler
                nestling = index[tag].handler
                # figure out which into which index this nestling should be placed
                if handler.namespace == nestling.namespace:
                    handler._pyre_nodeIndex[tag] = nestling
                else:
                    handler._pyre_nodeQIndex[(nestling.namespace, tag)] = nestling

        # and now adjust the actual document class
        if record.root is not None:
            root = index[record.root].handler
            record.namespace = root.namespace
            record._pyre_nodeIndex = { record.root: root }

        # return the list of descriptors so it can be attached to whatever name _pyre_DTD specifies
        return descriptors


# end of file 
