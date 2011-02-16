# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
"""


def main():
    """
    This is the main entry point in the package. It is invoked by the {merlin} script.  It's
    job is to boot pyre, examine the command line to deduce which actor the user would like to
    invoke, instantiate it, and call its main entry point with the supplied command line
    arguments.

    There are other possible ways to invoke merlin. See the package documentation.
    """
    import pyre
    # extract the non-configurational parts of the command line
    request = tuple(c for p,c,l in pyre.executive.configurator.commands)



    # interpret the request as the name of a merlin component, followed by an argument tuple to
    # its main entry point
    componentName = request[0]
    args = request[1:]
    print("component name: {!r}".format(componentName))
    print("arguments: {!r}".format(args))
    # convert the component name into a uri
    # attempt to instantiate the component
    c = pyre.executive.retrieveComponentDescriptor(
        uri="import://gauss.functors#{}".format(componentName))
    print(c)

    return


# end of file 
