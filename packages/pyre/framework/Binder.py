# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class Binder:
    """
    The manager of the component interdependencies.

    Binder is responsible for instantiating and validating the values of the traits of
    components and interfaces.
    """


    # interface
    def bindComponentClass(self, component):
        """
        Initialize the {component} class record

        After a component class is bound, its traits are known to be in good state
        """
        # iterate over all the locally declared traits
        for trait in component.pyre_inventory.keys():
            # delegate binding activities
            trait.pyre_bindClass(configurable=component)
        # all done
        return component


    def bindComponentInstance(self, component):
        """
        Initialize the {component} instance

        After a component instance is bound, its traits are known to be in good state
        """
        # print("Binder.bindComponentInstance: component {.pyre_name!r}".format(component))
        # iterate over all traits, both local and inherited
        for trait in component.pyre_getTraitDescriptors():
            # print("  trait {.name!r}".format(trait))
            # delegate binding activities
            trait.pyre_bindInstance(configurable=component)
        # all done
        return component


# end of file 
