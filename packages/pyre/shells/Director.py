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
    def __init__(self, name, bases, attributes, **kwds):
        """
        Initialize a new application class record
        """
        # initialize the record
        super().__init__(name, bases, attributes, **kwds)
        # if I am a hidden application subclass, we are all done
        if self.pyre_hidden: return

        # all done
        return


    def __call__(self, name=None, **kwds):
        """
        Instantiate one of my classes
        """
        # build the application name
        name = name if name is not None else self.applicationName
        # ask the executive to hunt down the application INSTANCE configuration file
        self.pyre_executive.configurePackage(package=name)
        # delegate the creation of the instance and return it
        return super().__call__(name=name, **kwds)


# end of file 
