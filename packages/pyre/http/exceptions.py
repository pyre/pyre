# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# exceptions
from .Response import Response


# local anchor for all package exceptions
class ProtocolError(Response):
    """
    Base exceptions for all error conditions detected by http components
    """


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # get my headers so i can add the standard headers for an error condition
        headers = self.headers
        # the error content type
        headers['Content-Type'] = 'text/html;charset={.encoding}'.format(self)
        # tell the client what to do with the connection
        headers['Connection'] = 'close'
        # all done
        return


    def __str__(self):
        """
        The default rendering of protocol errors
        """
        return """
        <head>
          <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
          <title>Unhappy web server - {0.server.name}</title>
        </head>
        <body>
          <h1>Something went very wrong</h1>
          <p>
            The server <em>{0.server.name}</em> is very unhappy and returned error code {0.code}.
          </p>
          <p>The standard description for this error is: {0.__doc__}</p>
          <p>{0.description}</p>
        </body>
        """.format(self)


# end of file
