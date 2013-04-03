# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


class Device:
    """
    The property sheet of a CUDA capable device
    """


    # attributes
    id = None
    name = ""
    version = None
    capability = None

    globalMemory = 0
    

    # debugging
    def dump(self, indent=''):
        """
        Print information about this device
        """
        print("{}device {.id}:".format(indent, self))
        print("{}  name: {.name}".format(indent, self))
        print("{}  driver version: {.version}".format(indent, self))
        print("{}  compute capability: {.capability}".format(indent, self))
        print("{}  global memory: {.globalMemory} bytes".format(indent, self))
    
        # all done
        return


# end of file 
