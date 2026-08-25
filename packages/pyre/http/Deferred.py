# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the placeholder for responses that are produced asynchronously
class Deferred:
    """
    A response placeholder that parks the client connection until the actual document is ready

    Request handlers hand an instance to the server in place of a document when the response
    is produced away from the request handling stack, e.g. by a team of worker processes. The
    server installs its delivery hook and keeps the connection open; when the document shows
    up, {resolve} pushes it through the hook and onto the wire
    """

    # interface
    def resolve(self, response):
        """
        The actual {response} document is ready; hand it to the transport
        """
        # push the document through the hook the server installed when it parked the connection
        return self.deliver(response=response)

    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # the delivery hook; the server installs it when it parks the connection
        self.deliver = None
        # all done
        return


# end of file
