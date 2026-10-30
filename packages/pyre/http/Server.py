# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import functools
import json
import os
import resource
import time
import uuid
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
    from .Deferred import Deferred as deferred
    from .EventStream import EventStream as eventStream
    from .Hub import Hub
    from .Journal import Journal

    # exceptions
    from . import exceptions, responses, documents

    # user configurable state
    # the language of my responses
    renderer = pyre.weaver.language()
    renderer.default = "http"
    renderer.doc = "the renderer of the server responses to client requests"

    # keep idle streams from being reaped by intermediaries
    heartbeat = pyre.properties.dimensional()
    heartbeat.default = 15 * second
    heartbeat.doc = "how often to send a keep-alive on held-open streaming connections"

    # bound how far behind a slow subscriber may fall
    streamCapacity = pyre.properties.int()
    streamCapacity.default = 1024
    streamCapacity.doc = "the most frames a streaming subscriber may queue before it is dropped"

    # the journal a late client gets to catch up on
    history = pyre.properties.int()
    history.default = 2048
    history.doc = "how many journal records to keep for clients that open their event stream late"

    # the pace of the journal batches
    latency = pyre.properties.dimensional()
    latency.default = 0.1 * second
    latency.doc = "how long journal records accumulate before going out to clients as a batch"

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
        Register with the nexus, build the event hub, and start publishing the journal
        """
        # chain up to grab a port and register for connection requests
        super().activate(app=app, dispatcher=dispatcher)
        # mint the token that tells this run of the server apart from every other, including
        # the next one on the same host and port; a client that finds a different token on
        # the other end of a connection it thought it knew is talking to somebody else
        self.instance = str(uuid.uuid4())
        # the greeting carries the token, so one built for an earlier run is stale
        self._helloFrame = None
        # note when this run of the server came up
        self.started = time.time()
        # now that the dispatcher is available, build my event hub, wiring in the keep-alive
        # broadcast and the per-subscriber buffer bound
        self.hub = self.Hub(
            dispatcher=self.dispatcher,
            capacity=self.streamCapacity,
            interval=self.heartbeat,
            keepalive=self.eventStream.keepalive(),
        )
        # from here on, everything said to the journal also reaches the live clients
        self._listen()
        # all done
        return

    @pyre.export(tip="shutdown")
    def shutdown(self):
        """
        Give the journal back to the device it had before me, and clean up
        """
        # if my journal device was installed
        if self.journal is not None:
            # give the journal back to the device it replaced
            journal.chronicler.device = self.journal.mirror
            # and forget mine
            self.journal = None
        # chain up
        return super().shutdown()

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
            # if a deferred response was parked on this connection
            parked = self.parked.pop(channel, None)
            # let it know
            if parked is not None:
                # that nobody is waiting for its document any more
                parked.cancel()
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
        # channel, unparking it as we take it, so that a completed request is never left behind
        # for the next request on a kept-alive connection to inherit; it is parked again below,
        # in the {if not complete} branch, only while it is still partial
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
            # show me the request
            headerReport.line(f"got a {request.command} request")
            # its target
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

        # if the user wants to see the headers; a deferred response has none to show yet
        if headerReport.active and not isinstance(response, self.deferred):
            # sign on
            headerReport.line(f"sending a {response.code} response with headers")
            # go through the headers
            for key, value in response.headers.items():
                # and show me each one
                headerReport.line(f"  {key}: {value}")
            # and report
            headerReport.log()

        # if all goes well, respond
        return self.respond(channel=channel, request=request, response=response)

    # interface
    def hello(self):
        """
        Frame the greeting that opens every event stream, which says which run of the server
        is on the other end
        """
        # the greeting never changes, so build it once
        if self._helloFrame is None:
            # use the {EventStream} framing so the wire format lives in one place
            stream = self.eventStream(server=self)
            # the payload is my token
            payload = json.dumps({"instance": self.instance})
            # under a name of its own, so that clients that treat every unnamed message as a
            # change notification do not mistake the greeting for one
            self._helloFrame = stream.event(payload, name="hello")
        # hand it off
        return self._helloFrame

    def notifyChange(self):
        """
        Tell every live client subscribed to the global topic that its state has changed
        """
        # the notification never changes, so build it once
        if self._changeFrame is None:
            # use the {EventStream} framing so the wire format lives in one place
            stream = self.eventStream(server=self)
            # a minimal payload; any message on the global topic means "refetch your state"
            self._changeFrame = stream.event(json.dumps({"type": "change"}))
        # broadcast it on the global topic; coalesce, so a burst collapses into a single
        # pending refetch per client rather than a storm
        self.hub.publish(self._changeFrame, coalesce=True)
        # all done
        return

    def describe(self) -> dict:
        """
        Describe the process: what it is, where it runs, how long it has been up, and the
        descriptors it holds against its ceiling
        """
        # the system
        system = os.uname()
        # the descriptors
        held, ceiling = self._held()
        # assemble the description; a server that has not come up yet has no uptime
        return {
            "pid": os.getpid(),
            "host": system.nodename,
            "platform": f"{system.sysname.lower()}-{system.machine}",
            "cores": os.cpu_count(),
            "memory": os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES"),
            "started": self.started,
            "uptime": time.time() - self.started if self.started is not None else None,
            "descriptors": held,
            "ceiling": ceiling,
        }

    def events(self):
        """
        Open an event stream on the global topic, where change notifications are published
        """
        # the stream opens with the greeting, so the client learns which run it is talking to
        return self.eventStream(server=self, opening=self.hello())

    def chronicle(self):
        """
        Open an event stream on the journal topic, which carries the records of the journal
        """
        # the greeting comes first
        opening = self.hello()
        # followed by the history, if there is any
        history = self.journal.opening()
        # so a newcomer sees what was said before it connected
        if history is not None:
            # append it
            opening += history
        # build the stream
        return self.eventStream(server=self, topic=self.Journal.topic, opening=opening)

    def fulfill(self, request):
        """
        Fulfill the given fully formed client {request}
        """
        # delegate to the app to build a response and return it
        return self.application.pyre_respond(server=self, request=request)

    def respond(self, channel, request, response):
        # a deferred response parks the connection until its document shows up
        if isinstance(response, self.deferred):
            # install the delivery hook
            response.deliver = functools.partial(self.complete, channel=channel, request=request)
            # remember it, so a peer hangup can cancel it
            self.parked[channel] = response
            # and keep watching the channel so we can tell when the peer hangs up
            return True

        # if this is a streaming response
        if response.streaming:
            # hand the channel to the hub instead of rendering and writing it once
            return self.stream(channel=channel, request=request, response=response)

        # if the body of the response is in a file
        if response.payload is not None:
            # it goes from the file to the peer without passing through this process
            return self.transmit(channel=channel, request=request, response=response)

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
                # say what went wrong
                channel.line(f"encountered {error}")
                # while doing what
                channel.line(f"while responding to a {request.command} request")
                # for which target
                channel.line(f"for '{request.url}'")
                # and with which headers
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

    def transmit(self, channel, request, response):
        """
        Send the status line and the headers of {response}, and then its body straight from
        the file that holds it, which the kernel copies to the peer without it ever passing
        through this process
        """
        # the file that holds the body
        payload = response.payload
        # the file must be closed, whatever happens
        try:
            # the size of the body is the size of the file
            size = os.fstat(payload.fileno()).st_size
            # which the client learns before the headers go out
            response.headers["Content-Length"] = size
            # render the status line and the headers, and mark their end
            preamble = b"\r\n".join(self.renderer.preamble(document=response)) + b"\r\n\r\n"
            # send them
            channel.write(preamble)
            # a socket can have the kernel send the body
            send = getattr(channel, "sendfile", None)
            # if mine can
            if send is not None:
                # let it
                send(payload, 0, size)
            # otherwise
            else:
                # read the body and write it
                channel.write(os.pread(payload.fileno(), size, 0))
        # if anything goes wrong on the wire
        except OSError as error:
            # make a channel
            channel = journal.debug("pyre.http.server")
            # if it is active
            if channel.active:
                # say what went wrong
                channel.line(f"encountered {error}")
                # while doing what
                channel.line(f"while transmitting the body of a {request.command} response")
                # and for which target
                channel.line(f"for '{request.url}'")
                # and complain
                channel.log()
        # no matter what
        finally:
            # let go of the file
            payload.close()
        # if the application wants to terminate
        if response.abort:
            # do it
            raise SystemExit(response.exitCode)
        # otherwise, let the response document decide whether we should keep the channel alive
        return response.alive

    def complete(self, channel, request, response):
        """
        The document of a parked connection is ready; send it to the peer
        """
        # the connection is no longer parked
        self.parked.pop(channel, None)
        # and the document is no longer deferred, so it follows the standard path
        return self.respond(channel=channel, request=request, response=response)

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
        # subscribe this channel to the response's topic; the headers promise a body in the
        # chunked coding, so ask the hub to wrap everything it delivers to this channel
        hub.subscribe(channel=channel, topic=response.topic, framing=response.chunk)
        # queue the preamble; the hub arms the channel and delivers it on the same path as
        # every later event, so a streaming channel is never touched by the blocking writer.
        # the preamble is not part of the body, so it goes out as it is
        hub.send(channel=channel, data=preamble, raw=True)
        # if the response opens with frames of its own, e.g. what a newcomer missed
        if response.opening:
            # they go out next, ahead of anything published from here on
            hub.send(channel=channel, data=response.opening)
        # let the response decide whether the connection stays open
        return response.alive

    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # initialize my connection index
        self.requests = {}
        # and the registry of responses parked on their connections
        self.parked = {}
        # all done
        return

    # implementation details
    def _listen(self):
        """
        Install the journal device that keeps a history and publishes entries to live clients
        """
        # the device the journal has been writing to, typically the terminal
        terminal = journal.chronicler.device
        # build mine, with the terminal as its mirror
        self.journal = self.Journal(
            server=self, mirror=terminal, capacity=self.history, latency=self.latency
        )
        # and make it the default device
        journal.chronicler.device = self.journal
        # all done
        return

    def _held(self) -> tuple:
        """
        Count the file descriptors this process holds, against how many it may, as a pair; the
        count is {None} on a platform that cannot tell

        Everything that serves a static asset needs a descriptor, so a count creeping up on the
        ceiling explains a server that has stopped answering, while a request that needs none
        keeps answering and makes the server look healthy
        """
        # the ceiling is inherited from whichever shell launched the server, so ask rather
        # than assume the system default
        ceiling, _ = resource.getrlimit(resource.RLIMIT_NOFILE)
        # carefully, since the count is a convenience
        try:
            # every open descriptor appears here, on the platforms that have it; the listing
            # itself holds one while it runs, so this reads one high
            held = len(os.listdir("/dev/fd"))
        # a platform without it
        except OSError:
            # says nothing rather than guessing
            return None, ceiling
        # otherwise, the count against the ceiling
        return held, ceiling

    # private data
    requests = None  # the requests still being assembled, by connection
    parked = None  # the deferred responses waiting for their documents, by connection
    hub = None  # the registry of streaming subscribers, built at activation
    journal = None  # the device that records and publishes journal entries
    instance = None  # the token that identifies this run of the server, minted at activation
    started = None  # when this run of the server came up, set at activation
    _helloFrame = None  # the greeting frame, built on first use
    _changeFrame = None  # the change notification frame, built on first use
    # constants
    MAX_BYTES = 1024 * 1024


# end of file
