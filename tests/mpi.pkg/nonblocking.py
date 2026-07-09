#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the transfers that hand back a receipt instead of blocking
"""


def test():
    # access the package
    import mpi

    # initialize
    ext = mpi.init()
    # get the world communicator
    world = mpi.world
    # and its structure
    size = world.size
    rank = world.rank

    # place the processes on a ring: the one i send to
    following = (rank + 1) % size
    # and the one i hear from
    preceding = (rank - 1) % size

    # the payload i ship says who sent it
    payload = bytes([rank, 0xAB])

    # post the receive first, so that the message has somewhere to land
    inbox = bytearray(2)
    # then the send; neither call blocks, so the ring needs no parity split
    pending = [
        world.irecvBytes(inbox, preceding, 5),
        world.isendBytes(payload, following, 5),
    ]
    # the receipts name transfers that have not completed
    assert all(receipt.active for receipt in pending)

    # block until both are done
    reports = ext.waitAll(pending)
    # one report per transfer
    assert len(reports) == 2
    # and waiting has emptied every receipt
    assert not any(receipt.active for receipt in pending)

    # the payload came round the ring
    assert bytes(inbox) == bytes([preceding, 0xAB])
    # and the report of the receive says who sent it
    assert reports[0].source == preceding
    # carrying the label we agreed on
    assert reports[0].tag == 5
    # and exactly two octets
    assert reports[0].bytes == 2
    # none of which was cancelled
    assert not reports[0].cancelled

    # the same, but waiting for whichever transfer finishes first
    again = bytearray(2)
    # post the pair
    pending = [
        world.irecvBytes(again, preceding, 6),
        world.isendBytes(payload, following, 6),
    ]
    # wait for one of them
    index, report = ext.waitAny(pending)
    # it names one of the two
    assert index in (0, 1)
    # and mpi has emptied that receipt, while the other may well still be in flight
    assert not pending[index].active
    # finish whatever is left
    ext.waitAll(pending)
    # and the payload came round once more
    assert bytes(again) == bytes([preceding, 0xAB])

    # a message that has not arrived yet is reported as absent rather than waited for
    assert world.iprobe(preceding, 99) is None

    # ship a payload the blocking way, so that one is certainly on its way to me
    world.sendBytes(payload, following, 7)
    # and spin until the one addressed to me shows up
    waiting = None
    # asking as often as it takes
    while waiting is None:
        waiting = world.iprobe(preceding, 7)
    # what is waiting carries two octets
    assert waiting.bytes == 2
    # sent by the process before me
    assert waiting.source == preceding
    # now take it
    landed = world.recvBytes(preceding, 7)
    # and it says who sent it
    assert landed == bytes([preceding, 0xAB])

    # mpi writes into the buffer long after the call that started the transfer has returned, so
    # the receipt must hold on to it; without that, a buffer nobody else names would be
    # reclaimed while the transfer was still writing into it
    import sys

    # make one
    orphan = bytearray(2)
    # count who refers to it
    before = sys.getrefcount(orphan)
    # start a transfer into it
    receipt = world.irecvBytes(orphan, preceding, 13)
    # and somebody new does: the receipt
    assert sys.getrefcount(orphan) > before

    # so the transfer lands in it, no matter who else lets go
    ext.waitAll([receipt, world.isendBytes(payload, following, 13)])
    # carrying what the process before me sent
    assert bytes(orphan) == bytes([preceding, 0xAB])
    # and once the receipt is spent and gone, so is its claim on the buffer
    del receipt
    assert sys.getrefcount(orphan) == before

    # a conduit offers the same transfers, with the peer and the label already remembered
    upstream = world.port(peer=preceding, tag=11)
    downstream = world.port(peer=following, tag=11)

    # post the receive, then the send
    delivery = bytearray(2)
    # neither blocks
    conversation = [upstream.irecvBytes(delivery), downstream.isendBytes(payload)]
    # block until both are done
    ext.waitAll(conversation)
    # and the payload came round the ring
    assert bytes(delivery) == bytes([preceding, 0xAB])

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
