# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


# framework access
import pyre


# declaration
class Director(pyre.actor):
    """
    The metaclass of applications

    {Director} takes care of all the tasks necessary to register an application family with the
    framework
    """

    # meta methods
    def __init__(self, name, bases, attributes, namespace=None, **kwds):
        """
        Initialization of application class records
        """
        # chain up
        super().__init__(name, bases, attributes, **kwds)

        # if i don't have a namespace
        if not namespace:
            # get my package
            package = self.pyre_package()
            # and if it exists
            if package:
                # use its name as my namespace
                namespace = package.name
        # attach it
        self.pyre_namespace = namespace

        # all done
        return

    def __call__(self, name=None, globalAliases=True, locator=None, **kwds):
        """
        Build an application instance
        """
        # record the caller's location
        # if i have a name
        if name is not None:
            # build a locator
            loc = pyre.tracking.simple(f"while initializing application '{name}'")
            # connect it to the locator of the caller
            locator = loc if locator is None else pyre.tracking.chain(loc, locator)
            # load the application configuration
            self.pyre_executive.configure(namespace=name, locator=loc)
        # otherwise
        else:
            # just adjust the locator
            locator = pyre.tracking.here(1) if locator is None else locator

        # and chain up
        return super().__call__(
            name=name, globalAliases=globalAliases, locator=locator, **kwds
        )


# end of file
