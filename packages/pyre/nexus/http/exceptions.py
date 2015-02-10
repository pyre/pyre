# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# exceptions
from ..exceptions import NexusError


# local anchor for all package exceptions
class ProtocolError(NexusError):
    """
    Base exceptions for all error conditions detected by http components
    """

    # meta-methods
    def __init__(self, server, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the server reference
        self.server = server
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
