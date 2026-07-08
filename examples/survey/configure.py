#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the framework and the toolkit under demonstration
import pyre
import survey


# a make-believe web server whose traits we configure interactively
class Server(pyre.component, family="survey.demo.server"):
    """
    A small stand-in component with just enough traits to show every prompt {survey.configure}
    knows how to pick
    """

    # a plain string -> a free-text prompt
    host = pyre.properties.str()
    host.default = "localhost"
    host.doc = "the interface to bind"

    # an integer that must be positive -> free text, rejected until it coerces and validates
    port = pyre.properties.int()
    port.default = 8080
    port.doc = "the port to listen on"
    port.validators = pyre.constraints.isPositive()

    # an integer confined to a range -> free text, validated against the bounds
    workers = pyre.properties.int()
    workers.default = 4
    workers.doc = "how many worker processes"
    workers.validators = pyre.constraints.isBetween(low=1, high=64)

    # a string limited to a fixed set of choices -> a menu
    loglevel = pyre.properties.str()
    loglevel.default = "info"
    loglevel.doc = "logging verbosity"
    loglevel.validators = pyre.constraints.isMember("debug", "info", "warning", "error")

    # a boolean -> a yes/no confirmation
    tls = pyre.properties.bool()
    tls.default = False
    tls.doc = "serve over TLS"

    # a filesystem path -> free text, coerced into a {pyre} path
    root = pyre.properties.path()
    root.default = "/var/www"
    root.doc = "the document root"


def main():
    """
    Configure a {Server} by walking its traits with {survey.configure}
    """
    # style the prompts: a cool blue for the questions, a warm orange for the current choice
    survey.set_theme(
        survey.Theme(
            message=survey.hsl(210, 0.85, 0.62),
            selected=survey.hsl(28, 0.90, 0.55),
        )
    )

    # open with a banner
    print("── configure a server ──────────────────────────────")
    # spell out what is about to happen
    print("survey walks the component's traits; each prompt is chosen from the trait's type,")
    print("seeded with its default, and every answer is coerced and validated by pyre\n")

    # build a server carrying its declared defaults
    server = Server(name="server")

    # let survey walk its properties, prompt for each, and apply the answers
    survey.configure(server)

    # head the summary
    print("\n── configured ──────────────────────────────────────")
    # walk the properties and show what each one ended up as
    for trait in server.pyre_properties():
        # read the now-validated value and print it on an aligned row
        print(f"  {trait.name:10} {getattr(server, trait.name)}")

    # report success
    return 0


# driver
if __name__ == "__main__":
    # run the example, treating ctrl-c as a clean, quiet exit
    try:
        # share the exit code with the shell
        raise SystemExit(main())
    except KeyboardInterrupt:
        # the user bailed; leave the terminal on a fresh line
        print("\ncancelled")
        # and report the cancellation
        raise SystemExit(1)


# end of file
