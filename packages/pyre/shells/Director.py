# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
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
            family = self.pyre_family()
            # if i have one, use it; otherwise, use the class name
            self.pyre_prefix = self.pyre_executive.nameserver.split(family)[0] if family else name

        # all done
        return


    def __call__(self, name=None, **kwds):
        """
        Instantiate one of my classes
        """
        # if I have a name for the application instance, use it hunt down configuration files
        # for this particular instance
        if name:
            # get the executive
            executive = self.pyre_executive
            # set up the priority
            priority = executive.priority.package
            # build a locator
            locator = pyre.tracking.simple('while initializing application {!r}'.format(name))
            # ask the executive to hunt down the application INSTANCE configuration file
            executive.configure(stem=name, priority=priority, locator=locator)

        # delegate the creation of the instance and return it
        return super().__call__(name=name, **kwds)


# end of file 
