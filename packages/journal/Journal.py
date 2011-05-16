# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# access to the framework
import pyre

# access the requirements
from .Device import Device
# and their defaults
from .Console import Console


# declaration
class Journal(pyre.component, family="journal"):
    """
    Place holder for the configurable bits of the journal package
    """


    # class public data
    device = pyre.properties.facility(interface=Device, default=Console)
    device.doc = "the component responsible for handling journal entries"


    # interface
    def configureCategories(self, categories):
        """
        Extract channel information from the configuration store for each of the given
        {categories}
        """
        # access the configuration store
        config = self.pyre_executive.configurator
        # access the type converters
        import pyre.schema
        # and iterate over {categories}, updating their indices with the contents of the pyre
        # configuration store in {config}
        for category in categories:
            # build the key prefix
            prefix = "journal\." + category.severity
            # identify the relevant keys
            for name, node in config.select(pattern=prefix):
                # get the value
                value = node.value
                # if it's {None}, it probably came from the command line without an assignment
                if value is None: value = True
                # attempt to cast to a bool
                try:
                    value = pyre.schema.bool.pyre_cast(value)
                # if this fails
                except pyre.schema.bool.CastingError:
                    # ignore it and move on
                    continue
                # extract the category name
                categoryName = '.'.join(name.split('.')[2:])
                # update the index
                category(categoryName).active = value
        # all done
        return


    # meta methods
    def __init__(self, categories, **kwds):
        # chain to my ancestors
        super().__init__(**kwds)
        # configure the default channels
        self.configureCategories(categories)
        # all done
        return



# end of file 
