#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise the transfers that hand back a receipt instead of blocking, the receipt itself, the
    report it completes into, and the collective waits the module publishes
    """
    # access the package that hosts the bindings
    import mpi

    # for counting who holds on to a buffer
    import sys

    # bring mpi up, arranging for the shutdown
    mpi.init()
    # get the bindings
    libmpi = mpi.libmpi
    # and the world communicator straight from them
    world = libmpi.world()
    # and its structure: the number of processes
    size = world.size
    # and my place among them
    rank = world.rank

    # place the processes on a ring: the one i send to
    following = (rank + 1) % size
    # and the one i hear from
    preceding = (rank - 1) % size

    # the payload i ship says who sent it
    payload = bytes([rank, 0xAB])

    # somewhere for the message to land
    inbox = bytearray(2)
    # post the receive first, so the message has somewhere to land, then the send; neither call
    # blocks, so the ring needs no parity split
    pending = [
        world.irecvBytes(inbox, preceding, 5),
        world.isendBytes(payload, following, 5),
    ]
    # a fresh receipt names a transfer that has not completed
    assert all(receipt.active for receipt in pending)
    # and is true while it is in flight
    assert all(bool(receipt) for receipt in pending)

    # block until both are done, reaching the wait that lives on the module
    reports = libmpi.waitAll(pending)
    # one report per transfer
    assert len(reports) == 2
    # and waiting has emptied every receipt
    assert not any(receipt.active for receipt in pending)
    # so a spent receipt is false
    assert not any(bool(receipt) for receipt in pending)

    # the payload came round the ring
    assert bytes(inbox) == bytes([preceding, 0xAB])

    # the report of the receive tells the whole story of the transfer
    report = reports[0]
    # who sent it
    assert report.source == preceding
    # the label it carried
    assert report.tag == 5
    # how many octets arrived
    assert report.bytes == 2
    # that it was not cancelled
    assert report.cancelled is False
    # that its own status code is a whole number, zero when nothing went wrong
    assert isinstance(report.error, int)
    # and that it renders as a readable summary
    assert "mpi.Status" in repr(report)

    # the same, but waiting for whichever transfer finishes first
    again = bytearray(2)
    # post the pair
    pending = [
        world.irecvBytes(again, preceding, 6),
        world.isendBytes(payload, following, 6),
    ]
    # wait for one of them
    index, outcome = libmpi.waitAny(pending)
    # it names one of the two
    assert index in (0, 1)
    # and that receipt is now empty, while the other may still be in flight
    assert not pending[index].active
    # the report of a send says nothing about its peer, so if the send won
    if index == 1:
        # wait again; the spent receipt is passed over, and the receive is what completes
        index, outcome = libmpi.waitAny(pending)
        # so it is the one named
        assert index == 0
    # the report belongs to the receive: it names the process before me
    assert outcome.source == preceding
    # the label we agreed on
    assert outcome.tag == 6
    # and the two octets of the payload
    assert outcome.bytes == 2
    # finish whatever is left
    libmpi.waitAll(pending)
    # and the payload came round once more
    assert bytes(again) == bytes([preceding, 0xAB])

    # a receipt can also be polled without blocking: post a pair, then ask until the receive says
    # it is done, which hands back a report where an empty poll hands back {None}
    landing = bytearray(2)
    # post the receive
    receiving = world.irecvBytes(landing, preceding, 8)
    # and the send
    sending = world.isendBytes(payload, following, 8)
    # spin on the non-blocking poll
    polled = receiving.test()
    # until it reports
    while polled is None:
        # asking again
        polled = receiving.test()
    # once it completes, the poll reports on the very same transfer
    assert polled.source == preceding
    # and clears the receipt
    assert not receiving.active
    # let the matching send drain
    sending.wait()

    # mpi writes into the buffer long after the call that started the transfer returned, so the
    # receipt must hold on to it; without that, a buffer nobody else names would be reclaimed
    # while the transfer was still writing into it. make one
    orphan = bytearray(2)
    # and count who refers to it
    before = sys.getrefcount(orphan)
    # start a transfer into it
    receipt = world.irecvBytes(orphan, preceding, 13)
    # and somebody new refers to it now: the receipt
    assert sys.getrefcount(orphan) > before
    # so the transfer lands in it, no matter who else lets go
    libmpi.waitAll([receipt, world.isendBytes(payload, following, 13)])
    # carrying what the process before me sent
    assert bytes(orphan) == bytes([preceding, 0xAB])
    # once the receipt is spent and gone
    del receipt
    # so is its claim on the buffer
    assert sys.getrefcount(orphan) == before

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
