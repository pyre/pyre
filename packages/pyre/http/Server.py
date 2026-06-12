# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import journal
import pyre

# the unit of time for the keep-alive interval
from pyre.units.SI import second


# my declaration
class Server(pyre.nexus.server, family="pyre.nexus.servers.http"):
    """
    A server that understands HTTP
    """

    # types
    from .Request import Request as request
    from .Response import Response as response
    from .EventStream import EventStream as eventStream
    from .Hub import Hub

    # exceptions
    from . import exceptions, responses, documents

    # user configurable state
    renderer = pyre.weaver.language(default="http")
    renderer.doc = "the renderer of the server responses to client requests"

    heartbeat = pyre.properties.dimensional(default=15 * second)
    heartbeat.doc = "how often to send a keep-alive on held-open streaming connections"

    streamCapacity = pyre.properties.int(default=1024)
    streamCapacity.doc = (
        "the most frames a streaming subscriber may queue before it is dropped"
    )

    # public state
    @property
    def name(self):
        """
        Server identification
        """
        # build an identification string
        return "pyre/{}.{}.{}".format(*self.version)

    @property
    def version(self):
        """
        Server version
        """
        # inherit the version of the framework
        return pyre.version()

    # protocol obligations
    @pyre.export(tip="register this service with the nexus")
    def activate(self, app, dispatcher):
        """
        Register with the nexus and build the event hub
        """
        # chain up to grab a port and register for connection requests
        super().activate(app=app, dispatcher=dispatcher)
        # now that the dispatcher is available, build my event hub, wiring in the keep-alive
        # broadcast and the per-subscriber buffer bound
        self.hub = self.Hub(
            dispatcher=self.dispatcher,
            capacity=self.streamCapacity,
            interval=self.heartbeat,
            keepalive=self.eventStream.keepalive(),
        )
        # all done
        return

    @pyre.export(tip="respond to the peer request")
    def process(self, channel):
        """
        Initiate or continue a conversation with a peer over {channel}
        """
        # we are here because {channel} has data for me; one of the following is true
        #
        # - this is the notification that the connection has been closed by the peer; in this
        #   case the channel contains exactly zero bytes for us; we check for this one early
        #
        # - this is the first time this peer connects
        #
        # - more data for an existing request have arrived
        #
        # - this is a known peer whose previous request was handled but has kept the connection
        #   alive; this case may not survive as it can be handled by starting a new request
        #   every time without closing the connection
        #
        # - the client has pipelined its requests; currently, this case is not handled
        #   correctly because it involves saving the local buffers

        # make a channel for reporting request and response information
        headerReport = journal.debug("pyre.http.headers")
        # get the application context
        application = self.application
        # show me
        application.debug.log(f"reading data from {channel.peer}")
        # get whatever data is available at this point
        chunk = channel.read(maxlen=self.MAX_BYTES)

        # if there was nothing to read
        if len(chunk) == 0:
            # show me
            application.debug.log(f"connection from {channel.peer} was closed")
            # close the connection
            channel.close()
            # if this channel was a streaming subscriber, drop it from the hub
            if self.hub is not None:
                # so we stop buffering events for a connection that is gone
                self.hub.unsubscribe(channel)
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

        # well, there is data to process; pick up any request parked from an earlier read on this
        # channel, unparking it as we take it. this {pop} is also the fix for response-crossing on a
        # kept-alive connection: a completed request is never left behind for the NEXT request to
        # inherit -- it is re-parked below, in the {if not complete} branch, only while still partial
        request = self.requests.pop(channel, None)
        # if nothing was parked for this channel
        if request is None:
            # this is a brand new request, so make one
            request = self.request()

        # attempt to
        try:
            # hand the chunk to the request
            complete = request.extract(server=self, chunk=chunk)
        # if something wrong happened
        except self.exceptions.ProtocolError as error:
            # send an error report to the client
            return self.respond(channel=channel, request=request, response=error)

        # if request assembly is not finished yet
        if not complete:
            # we expect more data to arrive later; register this request so we can continue the
            # processing next time there are data for it
            self.requests[channel] = request
            # and reschedule this channel
            return True

        # figuring out what the client is asking for is now complete; if the user wants
        # to see the headers
        if headerReport.active:
            # show me the request info
            headerReport.line(f"got a {request.command} request")
            headerReport.line(f"for '{request.url}'")
            # and the headers
            headerReport.line(f"with headers")
            # go through the headers
            for key, value in request.headers.items():
                # and show me each one
                headerReport.line(f"  {key}: {value}")
            # and report
            headerReport.log()

        # try to
        try:
            # fulfill the request
            response = self.fulfill(request)
        # if something bad happened
        except self.exceptions.ProtocolError as error:
            # send an error report to the client
            return self.respond(channel=channel, request=request, response=error)

        # if the user wants to see the headers
        if headerReport.active:
            # sign on
            headerReport.line(f"sending a {response.code} response with headers")
            # go through the headers
            for key, value in response.headers.items():
                # and show me eac hone
                headerReport.line(f"  {key}: {value}")
            # and report
            headerReport.log()

        # if all goes well, respond
        return self.respond(channel=channel, request=request, response=response)

    # interface
    def fulfill(self, request):
        """
        Fulfill the given fully formed client {request}
        """
        # delegate to the app to build a response and return it
        return self.application.pyre_respond(server=self, request=request)

    def respond(self, channel, request, response):
        # if this is a streaming response
        if response.streaming:
            # hand the channel to the hub instead of rendering and writing it once
            return self.stream(channel=channel, request=request, response=response)

        # attempt to
        try:
            # ask the renderer to put together the byte stream
            stream = b"\r\n".join(self.renderer.render(server=self, document=response))
        # if something goes wrong
        except self.exceptions.ProtocolError as error:
            # render the error
            stream = b"\r\n".join(self.renderer.render(server=self, document=error))

        # either way, attempt to
        try:
            # send the bytes to the client
            channel.write(stream)
        # if anything goes wrong
        except OSError as error:
            # make a channel
            channel = journal.debug("pyre.http.server")
            # if it is active
            if channel.active:
                # build a message
                channel.line(f"encountered {error}")
                channel.line(f"while responding to a {request.command} request")
                channel.line(f"for '{request.url}'")
                channel.line(f"with headers")
                # go through the headers
                for key, value in request.headers.items():
                    # and show me each one
                    channel.line(f"  {key}: {value}")
                # and complain
                channel.log()

        # if the application wants to terminate
        if response.abort:
            # do it
            raise SystemExit(response.exitCode)

        # otherwise, let the response document decide whether we should keep the channel alive
        return response.alive

    def stream(self, channel, request, response):
        """
        Begin a server-sent event stream on {channel} by handing it to the hub
        """
        # render the preamble: the status line and headers, with no body and no Content-Length,
        # terminated by the blank line that separates the headers from the event stream
        preamble = b"\r\n".join(self.renderer.preamble(document=response)) + b"\r\n\r\n"
        # switch the channel to non-blocking so the hub can perform partial sends
        channel.setblocking(False)
        # get my hub
        hub = self.hub
        # subscribe this channel to the response's topic
        hub.subscribe(channel=channel, topic=response.topic)
        # queue the preamble; the hub arms the channel and delivers it on the same path as
        # every later event, so a streaming channel is never touched by the blocking writer
        hub.send(channel=channel, data=preamble)
        # let the response decide whether the connection stays open
        return response.alive

    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # initialize my connection index
        self.requests = {}
        # all done
        return

    # implementation details
    # private data
    requests = None
    hub = None
    # constants
    MAX_BYTES = 1024 * 1024


# end of file
