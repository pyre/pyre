# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the base class
from .Response import Response


# the server-sent event stream response
class EventStream(Response):
    """
    An HTTP response that holds the connection open and pushes server-sent events (SSE)

    {EventStream} is pure transport: it carries the SSE headers and frames the wire format,
    knowing nothing about any application. The server routes it down its streaming path, where
    a {Hub} delivers events to the held-open connection.
    """

    # public data
    code = 200  # a successful response
    status = "OK"  # its description
    streaming = True  # route me down the server's streaming path
    alive = True  # hold the connection open
    topic = ""  # the hub topic that scopes delivery; empty is the global topic

    # interface
    def event(self, data, *, name=None, id=None, retry=None):
        """
        Format {data} as a single SSE frame and return the encoded bytes
        """
        # collect the frame lines
        lines = []
        # an optional event id lets a reconnecting client report where it left off
        if id is not None:
            lines.append(f"id: {id}")
        # an optional event name lets listeners be type specific
        if name is not None:
            lines.append(f"event: {name}")
        # an optional reconnection delay hint, in milliseconds
        if retry is not None:
            lines.append(f"retry: {retry}")
        # the payload, split so that any embedded newline stays within this one frame
        for line in data.splitlines() or [""]:
            lines.append(f"data: {line}")
        # join the lines and terminate the frame with a blank line
        frame = "\n".join(lines) + "\n\n"
        # encode and hand off
        return frame.encode(self.encoding)

    def render(self, **kwds):
        """
        A streaming response carries no rendered body; its payload arrives out of band
        """
        # nothing to render
        return b""

    # the keep-alive frame the server's hub broadcasts on a timer to hold idle connections open
    @classmethod
    def keepalive(cls):
        """
        Frame an SSE comment that keeps the connection warm without dispatching a client event
        """
        # a colon-led line is a comment the client ignores; the blank line ends the frame
        return b": keepalive\n\n"

    # meta-methods
    def __init__(self, topic="", **kwds):
        # chain up
        super().__init__(**kwds)
        # remember the topic that scopes my delivery
        self.topic = topic
        # decorate the headers for SSE
        headers = self.headers
        # mark the content type
        headers["Content-Type"] = "text/event-stream"
        # forbid caching of the stream
        headers["Cache-Control"] = "no-cache"
        # hold the connection open
        headers["Connection"] = "keep-alive"
        # tell reverse proxies (nginx and friends) not to buffer the stream, so events reach the
        # client promptly instead of being held back until the connection closes
        headers["X-Accel-Buffering"] = "no"
        # all done
        return


# end of file
