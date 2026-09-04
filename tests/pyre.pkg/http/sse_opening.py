#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a streaming response with an opening payload has it delivered right after the
preamble, ahead of anything published later
"""

# the server whose streaming path is under test
from pyre.http.Server import Server

# the renderer it uses
from pyre.weaver.HTTP import HTTP

# the streaming response
from pyre.http.EventStream import EventStream


# a stand-in for the hub that records what it is asked to deliver
class Hub:
    """
    The minimal hub surface the streaming path needs
    """

    # metamethods
    def __init__(self):
        # the subscriptions
        self.subscriptions = []
        # and the outbound queue
        self.sent = []
        # all done
        return

    # interface
    def subscribe(self, channel, topic):
        # record
        self.subscriptions.append((channel, topic))
        # all done
        return

    def send(self, channel, data, coalesce=False):
        # record
        self.sent.append((channel, data))
        # all done
        return


# a stand-in for a client connection
class Channel:
    """
    The minimal channel surface the streaming path needs
    """

    # metamethods
    def __init__(self):
        # whether i was switched to non-blocking
        self.blocking = True
        # all done
        return

    # interface
    def setblocking(self, flag):
        # record
        self.blocking = flag
        # all done
        return


# a stand-in for the server itself
class Stub:
    """
    The pieces of a server that {stream} consults
    """

    # the identification string responses stamp into their headers
    name = "pyre/test"

    # metamethods
    def __init__(self):
        # the renderer
        self.renderer = HTTP(name="renderer")
        # and the hub
        self.hub = Hub()
        # all done
        return


def test():
    # the server pieces
    server = Stub()
    # a connection
    channel = Channel()
    # a response with an opening payload: two frames a newcomer must see first
    opening = b"event: journal\ndata: [1]\n\nevent: journal\ndata: [2]\n\n"
    response = EventStream(server=server, topic="journal", opening=opening)
    # it remembers the payload
    assert response.opening == opening

    # run the streaming path
    alive = Server.stream(server, channel=channel, request=None, response=response)
    # the connection stays open
    assert alive is True
    # and was switched to non-blocking
    assert channel.blocking is False
    # the channel was subscribed to the response's topic
    assert server.hub.subscriptions == [(channel, "journal")]
    # two deliveries were queued, both for this channel
    assert [entry[0] for entry in server.hub.sent] == [channel, channel]
    # the first is the preamble
    preamble = server.hub.sent[0][1]
    assert preamble.startswith(b"HTTP/1.1 200 OK\r\n")
    assert preamble.endswith(b"\r\n\r\n")
    # the second is the opening payload, verbatim
    assert server.hub.sent[1][1] == opening

    # a response without an opening payload queues only the preamble
    server = Stub()
    channel = Channel()
    Server.stream(server, channel=channel, request=None, response=EventStream(server=server))
    assert len(server.hub.sent) == 1

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
