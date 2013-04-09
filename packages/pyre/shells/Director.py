# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
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
    def __init__(self, name, bases, attributes, prefix=None, **kwds):
        """
        Initialization of application class records
        """
        # chain up
        super().__init__(name, bases, attributes, **kwds)

        # compute the application prefix
        # if one were given explicitly
        if prefix:
            # use it
            self.pyre_prefix = prefix
        # otherwise
        else:
            # get my family name
            package = self.pyre_package()
            # if i have one, use it; otherwise, use the class name
            self.pyre_prefix = package.name if package else name

        # all done
        return


    def __call__(self, name=None, globalAliases=True, locator=None, **kwds):
        """
        Instantiate one of my classes
        """
        # get the executive
        executive = self.pyre_executive
        # if I have a name for the application instance, use it to hunt down configuration
        # files for this particular instance
        if name:
            # set up the priority
            priority = executive.priority.package
            # build a locator
            initloc = pyre.tracking.simple('while initializing application {!r}'.format(name))
            # ask the executive to hunt down the application INSTANCE configuration file
            executive.configure(stem=name, priority=priority, locator=initloc)

        # record the caller's location
        locator = pyre.tracking.here(1) if locator is None else locator
        # chain up to create the instance
        app = super().__call__(name=name, globalAliases=globalAliases, locator=locator, **kwds)
        # attach it to the executive
        executive.application = weakref.proxy(app)
        # and return it
        return app


# end of file 
