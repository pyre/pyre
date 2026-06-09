# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2026 all rights reserved
#


# externals
import time # to generate timestamps
# framework
import pyre
# my protocol
from .Language import Language
# and its default implementation
from .HTML import HTML


# declaration
class HTTP(pyre.component, implements=Language):
    """
    An HTTP compliant document renderer
    """


    # user configurable state
    encoding = pyre.properties.str(default='iso-8859-1')
    encoding.doc = 'the encoding for HTTP headers'


    # public data
    version = 1, 1  # my preferred protocol version


    # mill obligations
    @pyre.export
    def render(self, document, **kwds):
        """
        Render the document
        """
        # assemble the payload
        page = self.body(document=document, **kwds)
        # inform the client about the size of the payload, before the headers go out
        document.headers['Content-Length'] = len(page)

        # emit the status line and headers
        yield from self.preamble(document=document)
        # mark the end of the headers
        yield b''
        # send the page
        yield page
        # all done
        return


    @pyre.export
    def header(self, document):
        """
        Render the header of the document
        """
        # get my encoding
        encoding = self.encoding
        # go through the headers
        for key, value in document.headers.items():
            # encode and ship
            yield f"{key}: {value}".encode(encoding, 'strict')

        # all done
        return


    @pyre.export
    def body(self, document, **kwds):
        """
        Render the body of the document
        """
        # ask the document to present itself
        return document.render(**kwds)


    @pyre.export
    def footer(self):
        """
        Render the footer of the document
        """
        yield ''


    # implementation details
    def preamble(self, document):
        """
        Render the status line and headers of a streaming {document}, with no body and no
        {Content-Length}
        """
        # unpack
        code = document.code
        status = document.status
        version = document.version

        # decide which protocol to use
        protocol = self.version if self.version < version else version
        # turn it into a string
        protocol = "{}.{}".format(*protocol)
        # start the response
        yield f"HTTP/{protocol} {code} {status}".encode(self.encoding, 'strict')

        # assemble the headers and send them off
        yield from self.header(document=document)
        # all done
        return


# end of file
