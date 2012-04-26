# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
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
        # print(" ** Catalog.pyre_instantiate: node={}, value={!r}".format(node, value))
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
        # otherwise, build my configuration access key
        basekey = client.pyre_split(name) + [self.name]
        # access the configurator
        configurator = client.pyre_executive.configurator
        # and the component registrar
        registrar = client.pyre_executive.registrar

        # get the explicit configuration information
        for _, slot in configurator.children(basekey):
            # instantiate the value
            instance = super().pyre_instantiate(node=slot, value=slot.getValue())
            # build the instance name
            cname = client.pyre_split(slot.name)[-1]
            # store it in the index
            index[cname] = instance

        # now the deferred configuration
        for trait, assignment, priority in configurator._retrieveDeferredAssignments(
            registrar=registrar, ns=basekey):
            # cast the assignment rhs
            value = self.type.pyre_cast(assignment.value)
            # if i got a component class record
            if not isinstance(value, self.Component) and issubclass(value, self.Component):
                # construct its name
                traitName = client.pyre_SEPARATOR.join([name, self.name, trait])
                # instantiate it
                value = value(name=traitName)
            # in any case, store the instance in the index
            index[trait] = value

        # return the index so that it can be attached as the trait value for this instance    
        return index


# end of file 
