# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


class Device:
    """
    The property sheet of a CUDA capable device
    """


    # attributes
    id = None
    name = ""
    capability = ()
    driverVersion = ()
    runtimeVersion = ()

    globalMemory = 0


    # debugging
    def dump(self, indent=''):
        """
        Print information about this device
        """
        print("{}device {.id}:".format(indent, self))
        print("{}  name: {.name}".format(indent, self))
        print("{}  driver version: {.driverVersion}".format(indent, self))
        print("{}  runtime version: {.runtimeVersion}".format(indent, self))
        print("{}  compute capability: {.capability}".format(indent, self))
        print("{}  global memory: {.globalMemory} bytes".format(indent, self))

        # all done
        return


# end of file
