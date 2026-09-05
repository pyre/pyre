#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Every severity reaches the courier through the right sink, in order, with its page intact
    """
    # externals
    import os

    # access
    import journal

    # make a pipe
    reader, writer = os.pipe()
    # make a courier on its write end and install it
    courier = journal.courier(descriptor=writer)
    journal.chronicler.device = courier

    # the channel name
    name = "test.courier.ship"
    # the severities that do not raise, and the sink each one reaches
    quiet = [
        (journal.info, "alert"),
        (journal.warning, "alert"),
        (journal.help, "help"),
        (journal.debug, "memo"),
    ]
    # log through each one
    for factory, _ in quiet:
        # make the channel
        channel = factory(name)
        # debug channels are off by default
        channel.active = True
        # log a two line entry with some indentation
        channel.line("first")
        channel.indent()
        channel.line("second")
        channel.outdent()
        channel.log("third", extra="note")
    # the fatal severities raise after delivering
    fatal = [
        (journal.error, "alert", journal.ApplicationError),
        (journal.firewall, "memo", journal.FirewallError),
    ]
    # log through each one
    for factory, _, complaint in fatal:
        # attempt to
        try:
            # log
            factory(name).log("boom")
        # the complaint is expected
        except complaint:
            # carry on
            pass
        # anything else is a failure
        else:
            # complain
            assert False, f"{factory.__name__} did not raise"

    # every entry made it out
    expected = len(quiet) + len(fatal)
    assert courier.seq == expected
    assert courier.shipped == expected
    assert courier.dropped == 0

    # read the records back
    lines = os.read(reader, 64 * 1024).splitlines(keepends=True)
    # one per entry
    assert len(lines) == expected
    # decode them
    records = [journal.record.decode(line) for line in lines]
    # the sequence numbers are consecutive
    assert [int(record.notes["seq"]) for record in records] == list(range(1, expected + 1))

    # the quiet ones
    for (factory, sink), record in zip(quiet, records):
        # reached the right sink
        assert record.sink == sink
        # from the right channel
        assert record.channel == name
        assert record.severity == factory.severity
        # with the page as logged, indentation included
        assert record.page == ["first", "  second", "third"]
        # and the extra note stringified
        assert record.notes["extra"] == "note"
    # the fatal ones
    for (factory, sink, _), record in zip(fatal, records[len(quiet) :]):
        # reached the right sink
        assert record.sink == sink
        # from the right channel
        assert record.severity == factory.severity
        # with their page
        assert record.page == ["boom"]

    # clean up
    courier.close()
    os.close(reader)

    # all done
    return


# main
if __name__ == "__main__":
    # tell journal to stay away from the bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
