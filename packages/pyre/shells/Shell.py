# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class Shell:

    """
    Mix-in class responsible for defining the mechanisms by which an application is launched.

    Launching involves interacting with the runtime environment in which the application is
    running to ensure that it starts running. For example, concurrent applications may schedule
    themselves for later execution, daemons may fork a couple of times to break their
    association with their controlling terminal, etc.

    The default behavior is to invoke an my {main} method, which is expected to be provided by
    some descendant.
    """


    def execute(self, *args, **kwds):
        """
        Invoke the application behavior
        """
        # must be implemented by a subclass
        return self.main(*args, **kwds)


# end of file 
