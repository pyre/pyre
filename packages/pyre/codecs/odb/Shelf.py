# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import re


class Shelf(dict):
    """
    Shelves are symbol tables that map component record factories to their names.

    Consider a configuration event, such as the command line instruction

        --integrator=odb://quadrature/integrators#monte_carlo

    This causes the manager of the persistent store to attempt to locate a file with the
    logical address "quadrature/integrators.odb". If the file exists, it is parsed and all the
    symbols it defines are loaded into a Shelf, with the names of the symbols as keys and the
    corersponding python objects as the values. Note that in our example, "monte_carlo" is
    expected to be one of these symbols, and it is further expected that it is a callable that
    returns the class record of a component that is assignment compatible with the facility
    "integrators", but that is handled by the configuration manager and does not concern the
    shelf, which has been loaded successfully.

    The framework guarantees that each configuration file is loaded into one and only one
    shelf, and that this happens no more than once. This ensures that each component class
    record gets a unique id in the application process space, or that processing instructions
    in configuration files are executed only the first time the configuration file is loaded.
    """


    # public data
    defaultEncoding = "utf-8"


    # interface
    def retrieveContents(self, vnode):
        """
        Read the contents of the filesystem {vnode} and return them as a string
        """
        # open the vnode with the default encoding
        contents = vnode.open(encoding=self.defaultEncoding).read()
        # print("       opened as a {0!r} file".format(self.defaultEncoding))

        # check whether the file contains an encoding declaration
        hasEncoding = self._encodingDetector.search(contents, endpos=200)
        if hasEncoding:
            encoding = hasEncoding.group(1).lower()
            if encoding != self.defaultEncoding:
                # print("       re-opened as a {0!r} file".format(self.encoding))
                return vnode.open(encoding=encoding).read()
        
        return contents


    # implementation details
    # the encoding detector
    _encodingDetector = re.compile("coding[:=]\s*([-\w.]+)")


# end of file 
