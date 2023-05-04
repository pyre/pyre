# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2021 all rights reserved
#


# externals
import weakref
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
        Instantiate one of my classes
        """
        # record the caller's location
        locator = pyre.tracking.here(1) if locator is None else locator
        # chain up to create the instance
        app = super().__call__(name=name, globalAliases=globalAliases, locator=locator, **kwds)

        # get the dashboard
        from ..framework.Dashboard import Dashboard as dashboard
        # check whether there is already an app registered with the dashboard
        if dashboard.pyre_application is not None:
            # generate a warning
            app.warning.log('the app {.pyre_application} is already registered'.format(self))
        # in any case, attach this instance to the dashboard
        dashboard.pyre_application = app

        # and return it
        return app


# end of file
