# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import re


class Shelf(dict):
    """
    Shelves are symbol tables that map component record factories to their names.

    Consider a configuration event, such as the command line instruction

        --integrator=vfs:/quadrature/integrators.odb#monte_carlo

    This causes the manager of the persistent store to attempt to locate a file with the
    logical address "quadrature/integrators.odb". If the file exists, it is parsed and all the
    symbols it defines are loaded into a Shelf, with the names of the symbols as keys and the
    corresponding python objects as the values. Note that in our example, "monte_carlo" is
    expected to be one of these symbols, and it is further expected that it is a callable that
    returns the class record of a component that is assignment compatible with the facility
    "integrators", but that is handled by the configuration manager and does not concern the
    shelf, which has been loaded successfully.

    The framework guarantees that each configuration file is loaded into one and only one
    shelf, and that this happens no more than once. This ensures that each component class
    record gets a unique id in the application process space, or that processing instructions
    in configuration files are executed only the first time the configuration file is loaded.
    """


    # exceptions
    from ..exceptions import SymbolNotFoundError


    # public data
    defaultEncoding = "utf-8"


    # interface
    @classmethod
    def retrieveContents(cls, source):
        """
        Read the contents of the filesystem {vnode} and return them as a string

        MGA: this is currently unused; not sure how important this encoding sniffing is. the
        main logic moved to the {pyre.framework.Executive}, who is now responsible for opening
        a stream from the uri it receives
        """
        # unpack the source
        scheme, address = source
        # open with the default encoding
        encoding, stream = filesystem.open(
            scheme=scheme, address=address, encoding=cls.defaultEncoding)
        contents = stream.read()
        # print("       opened as a {0!r} file".format(cls.defaultEncoding))
        # check whether the file contains an encoding declaration
        hasEncoding = cls._encodingDetector.search(contents, endpos=200)
        if hasEncoding:
            encoding = hasEncoding.group(1).lower()
            if encoding != cls.defaultEncoding:
                # print("       re-opened as a {0!r} file".format(cls.encoding))
                encoding, stream = filesystem.open(
                    scheme=scheme, address=address, encoding=encoding)
                contents = stream.read()
        # contents now is an open stream
        # build a new shelf
        shelf = Shelf()
        # invoke the interpreter to parse its contents
        exec(contents, shelf)
        # and return the shelf
        return shelf


    def retrieveSymbol(self, symbol):
        """
        Retrieve {symbol} from this shelf
        """
        try:
            return self[symbol]
        except KeyError as error:
            raise self.SymbolNotFoundError(shelf=self, symbol=symbol) from error


    # implementation details
    # the encoding detector
    _encodingDetector = re.compile("coding[:=]\s*([-\w.]+)")


# end of file 
