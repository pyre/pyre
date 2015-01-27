# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import pyre


# my declaration
class Server(pyre.nexus.server, family='pyre.nexus.servers.http'):
    """
    A server that understands HTTP
    """


    # types
    from .Request import Request as request
    from .Response import Response as response
    # exceptions
    from .exceptions import ProtocolError


    # protocol obligations
    @pyre.export(tip='respond to the peer request')
    def process(self, dispatcher, channel):
        """
        Initiate or continue a conversation with a peer over {channel}
        """
        # we are here because the {dispatcher} has data in {channel}; one of the following is true
        #
        # - this is the notification that the connection has been closed by the peer; in this
        #   case the channel contains exactly zero bytes for us; we check for this one early
        # - this the first time this peer connects
        # - more data that for an existing request have arrived
        # - this is a known peer whose previous request was handled but has kept the connection
        #   alive; this case may not survive as it can be handled by starting a new request
        #   every time without closing the connection

        # show me
        self.info.log('pulling data from {}'.format(channel.peer))
        # get whatever data is available at this point
        chunk = channel.read(maxlen=self.MAX_BYTES)

        # if there was nothing to read
        if len(chunk) == 0:
            # show me
            self.info.log('connection from {} was closed'.format(channel.peer))
            # close the connection
            channel.close()
            # check whether we know this peer
            try:
                # in which case, forget him
                del self.requests[channel]
            # if not
            except KeyError:
                # no problem
                pass
            # stop listening
            return False

        # well, there is data to process; if we have a pending request
        try:
            # get it
            request = self.requests[channel]
        # otherwise
        except KeyError:
            # make a new one
            request = self.request()

        # attempt to
        try:
            # hand the chunk to the request
            complete = request.process(chunk)
        # if something wrong happened
        except self.ProtocolError as error:
            # send an error report to the client
            self.complain(error)
            # and reschedule the channel for more data
            return True

        # if collecting the request is not finished
        if not complete:
            # we expect more data to arrive later, so register this request so we can continue
            # the processing next time there are data for it
            self.requests[channel] = request
            # and reschedule this channel
            return True

        # figuring out what the client is asking for is now complete; try to
        try:
            # fulfill the request
            response = self.fulfill(request)
        # if something bad happened
        except self.ProtocolError as error:
            # send an error report to the client
            self.complain(error)
            # and reschedule the channel for more data
            return True

        # if all goes well, respond
        # return self.respond(response)
        # get the peer address
        peer = channel.peer

        # show me
        self.info.line()
        self.info.line("method: {.command}".format(request))
        self.info.line("url: {.url}".format(request))
        self.info.line("version: {.version}".format(request))
        # print the headers
        self.info.line('headers from {}'.format(peer))
        for key, value in request.headers.items():
            self.info.line("{}: {}".format(key, value))
        self.info.log()

        # make a response
        self.info.log('preparing response for {}'.format(peer))
        response = self.response()
        self.info.log('sending response to {}'.format(peer))
        channel.write(response.error(404))
        self.info.log('done sending response to {}'.format(peer))

        return True


    # interface
    def  fulfill(self, request):
        """
        Fulfill the given fully formed client {request}
        """
        # build a response
        response = self.response()
        # and return it
        return response


    def respond(self, response):
        # all done
        return True


    def complain(self, error):
        """
        Send an error message to the client
        """

    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # initialize my connectionn index
        self.requests = {}
        # all done
        return


    # implementation details
    # private data
    requests = None
    # constants
    MAX_BYTES = 1024 * 1024


# end of file
