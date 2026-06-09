#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify the {HTTP} renderer's {render} emits a complete response: a status line, a
{Content-Length}, a blank line, and the body
"""

# the renderer under test
from pyre.weaver.HTTP import HTTP
# the document it renders
from pyre.http.documents import OK


# a stand-in for the server; the {Response} base only consults it for its {name}
class Server:
    """
    The minimal server surface a response needs
    """

    # the identification string the response stamps into its headers
    name = "pyre/test"


# a document that carries a body, so {render} has something to size and ship
class Page(OK):
    """
    An {OK} response with a fixed payload
    """

    # hand back a known body
    def render(self, **kwds):
        """
        Generate the payload
        """
        # a fixed page
        return b"<html>hi</html>"


def test():
    # build the renderer and a document with a body
    renderer = HTTP(name="renderer")
    page = Page(server=Server())

    # join the rendered fragments the way the server does
    wire = b"\r\n".join(renderer.render(document=page))

    # the status line opens the response
    assert wire.startswith(b"HTTP/1.0 200 OK\r\n")
    # the renderer sizes the body and advertises it
    assert b"Content-Length: 15\r\n" in wire
    # a blank line separates the headers from the body, which arrives last
    assert wire.endswith(b"\r\n\r\n<html>hi</html>")

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
