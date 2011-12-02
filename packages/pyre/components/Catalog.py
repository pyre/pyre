# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Facility import Facility


class Catalog(Facility):
    """
    A component container
    """


    def pyre_instantiate(self, node, value):
        """
        Attach a component catalog to my trait slot in the client component
        """
        # initialize the index we will leave behind; a {dict} for now
        index = {}
        # get the client
        client = node.componentInstance
        # and its name
        name = client.pyre_name
        # if it is nameless
        if not name:
            # nothing to configure...
            return index
        # otherwise, build the my configuration access key
        basekey = client.pyre_split(name) + [self.name]
        # access the configurator
        configurator = client.pyre_executive.configurator
        # get my configuration information
        for _, slot in configurator.children(basekey):
            # get my interface to retrieve the component descriptor
            factory = self.type.pyre_cast(slot.getValue())
            # build the instance name
            cname = client.pyre_split(slot.name)[-1]
            # instantiate
            instance = factory(name=cname)
            # store in the index
            index[cname] = instance
        # return the index so that it can be attached as the trait value for this instance    
        return index


# end of file 
