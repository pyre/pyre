# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from ..components.Actor import Actor


class Director(Actor):
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


    def __call__(self, *args, **kwds):
        """
        Instantiate one of my classes
        """
        # delegate
        shell = super().__call__(**kwds)
        # invoke the application behavior
        status = shell.run(*args, **kwds)
        # and return the status
        return status


# end of file 
