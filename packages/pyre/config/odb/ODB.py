# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# access to the locator factories
import pyre.tracking

# and my ancestors
from ..Codec import Codec


class ODB(Codec):
    """
    This package contains the implementation of the native importer
    """

    
    # type
    from .Shelf import Shelf


    # constants
    encoding = "odb"
    separator = '/'


    # interface
    def decode(self, client, scheme, source, locator):
        """
        Interpret {source} as a filename that the client's fileserver can convert into a file
        object; open it, execute it, and place its contents into a shelf
        """
        # print(" ** ODB.decode: {!r}".format(self))
        # build a locator for this request
        shelfLocator = pyre.tracking.simple(source=source)
        # adjust the locator
        locator = pyre.tracking.chain(this=shelfLocator, next=locator) if locator else shelfLocator
        # get the fileserver from the executive
        fileserver = client.fileserver
        # ask it to open the file
        try:
            # print("      opening {}:{}".format(scheme, source))
            _, stream = fileserver.open(scheme=scheme, address=source)
            # print("        ok!")
        # if this fails
        except fileserver.GenericError as error:
            # print("        NOT ok!")
            # report it as a decoding error
            raise self.DecodingError(
                codec=self, uri=locator.source, description=str(error),
                locator=locator) from error
        # read the contents
        # print("      reading")
        contents = stream.read()
        # build a new shelf
        shelf = self.Shelf(locator=locator)
        # invoke the interpreter to parse its contents and place them in the {shelf}
        # print("      parsing")
        exec(contents, shelf)
        # return the {shelf}
        # print("      shelving")
        return shelf


    def shelfSearchPath(self, client, context):
        """
        Build a sequence of locations to look for {context} appropriate shelves
        """
        # my client knows...
        return client.componentSearchPath(context=context)
                    

# end of file
