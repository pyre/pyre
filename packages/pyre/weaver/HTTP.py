# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
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
    headerEncoding = pyre.properties.str(default='iso-8859-1')
    headerEncoding.doc = 'the encoding for HTTP headers'

    bodyEncoding = pyre.properties.str(default='utf-8')
    bodyEncoding.doc = 'the encoding for the HTTP payload'

    html = Language(default=HTML)
    html.doc = 'the renderer of my payload'


    # mill obligations
    @pyre.export
    def render(self, document, server, **kwds):
        """
        Render the document
        """
        yield


    @pyre.export
    def header(self):
        """
        Render the header of the document
        """
        yield ''


    @pyre.export
    def body(self):
        """
        Render the body of the document
        """
        yield ''


    @pyre.export
    def footer(self):
        """
        Render the footer of the document
        """
        yield ''


    # interface
    def error(self, server, error):
        """
        Something bad has happened, so bypass the normal document rendering to display an error
        """
        # assemble the payload
        page = '\n'.join(self.html.render(document=str(error))).encode(self.bodyEncoding, 'strict')
        # build the headers
        yield '\r\n'.join([
            # the top line
            "HTTP/1.1 {0.code} {0.__doc__}".format(error),
            # the server identification string
            "Server: {}".format(server.name),
            # the date
            "Date: {}".format(self.timestamp()),
            # the error content type
            "Content-Type: text/html;charset=utf-8",
            # what to do with the connection
            "Connection: close",
            # how much stuff we are sending
            "Content-Length: {}".format(len(page)),
            ]).encode(self.headerEncoding, 'strict')
        # mark the end of headers
        yield b''
        # send the payload
        yield page
        # all done
        return



    # implementation details
    def timestamp(self, tick=None):
        """
        Generate a conforming timestamp
        """
        # use now if necessary
        if tick is None: tick = time.time()
        # unpack
        year, month, day, hh, mm, ss, wd, y, z = time.gmtime(tick)
        # render and return
        return "{}, {:02} {} {} {:02}:{:02}:{:02} GMT".format(
            self.weekdays[wd], day, self.months[month], year,
            hh, mm, ss
            )


    # private data
    months = (
        None,
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

    weekdays = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')


# end of file
