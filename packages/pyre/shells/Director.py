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

        # otherwise
        # build the private file space
        self.pyre_filesystem = self.pyre_mountVirtualFilesystem()
        # and mount any additional application-specific directories
        self.pyre_mountApplicationFolders()

        # register the application class as the resolver of its namespace
        self.pyre_executive.registerNamespaceResolver(
            resolver=self, namespace=self.pyre_getPackageName())

        # all done
        return


# end of file 
