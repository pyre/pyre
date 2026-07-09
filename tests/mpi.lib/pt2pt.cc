// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// for the build system
#include <portinfo>
// other packages
#include <cassert>
// grab the mpi objects
#include <pyre/mpi.h>


// exercise point to point communication: the blocking pair, the combined {sendrecv}, the
// nonblocking pair and the receipts they hand back, and the raw byte payloads that the
// pickling layer above us rides on
int
main()
{
    // bring mpi up
    pyre::mpi::initialize();

    // push down a scope so our handles die before mpi does
    {
        // the communicator that holds the whole job
        auto world = pyre::mpi::world();
        // its size
        auto size = world.size();
        // and my rank in it
        auto rank = world.rank();
        // this test needs a ring, so it needs at least two processes
        assert(size > 1);

        // place the processes on a ring: the one i send to
        auto next = (rank + 1) % size;
        // and the one i hear from
        auto previous = (rank + size - 1) % size;

        // pass my rank around the ring in a single call, which mpi is free to schedule
        // without deadlocking, where a ring of matched {send}/{recv} pairs would
        int received = -1;
        // exchange
        auto report = world.sendrecv(rank, next, received, previous, 17);
        // what came round is the rank of the process before me
        assert(received == previous);
        // and it came from that process
        assert(report.source() == previous);
        // carrying the label we agreed on
        assert(report.tag() == 17);
        // and it was a single cell
        assert(report.count<int>() == 1);

        // now the blocking pair, which needs the ring broken to avoid deadlocking: the even
        // ranks speak first, the odd ranks listen first
        int heard = -1;
        // so split on parity
        if (rank % 2 == 0) {
            // say my rank
            world.send(rank, next, 5);
            // then listen
            world.recv(heard, previous, 5);
        } else {
            // listen
            world.recv(heard, previous, 5);
            // then say my rank
            world.send(rank, next, 5);
        }
        // either way, what i heard is the rank of the process before me
        assert(heard == previous);

        // the nonblocking pair does not need the ring broken at all: post the receive first,
        // so the message has somewhere to land, then post the send
        int landed = -1;
        // start listening
        auto listening = world.irecv(landed, previous, 9);
        // the receipt names a transfer that has not completed
        assert(static_cast<bool>(listening));
        // start speaking
        auto speaking = world.isend(rank, next, 9);

        // block until my message has gone out
        speaking.wait();
        // and until the one addressed to me has arrived
        auto arrival = listening.wait();
        // once a receipt has been waited on, it names nothing
        assert(!listening.active());
        // what landed is the rank of the process before me
        assert(landed == previous);
        // and it came from that process
        assert(arrival.source() == previous);

        // the same, but waiting on both receipts at once
        int again = -1;
        // build the two transfers
        std::vector<pyre::mpi::Request> pending;
        // the receive first, so the message has somewhere to land
        pending.push_back(world.irecv(again, previous, 11));
        // then the send
        pending.push_back(world.isend(rank, next, 11));
        // block until both are done
        auto reports = pyre::mpi::waitAll(pending);
        // one report per transfer
        assert(reports.size() == 2);
        // waiting has emptied every receipt, so none of them will try to free anything
        assert(!pending[0].active());
        assert(!pending[1].active());
        // and the value came round the ring
        assert(again == previous);

        // send a raw payload around the ring; this is the path the pickling layer takes
        pyre::mpi::bytes_t outgoing { std::byte(rank), std::byte(0xab), std::byte(0xcd) };
        // the even ranks speak first, as before
        pyre::mpi::bytes_t incoming;
        // so split on parity again
        if (rank % 2 == 0) {
            world.sendBytes(outgoing, next, 23);
            incoming = world.recvBytes(previous, 23);
        } else {
            incoming = world.recvBytes(previous, 23);
            world.sendBytes(outgoing, next, 23);
        }
        // the payload arrived whole, sized by the probe rather than by prior agreement
        assert(incoming.size() == 3);
        // carrying the rank of the process before me
        assert(incoming[0] == std::byte(previous));
        // and the two bytes we planted
        assert(incoming[1] == std::byte(0xab));
        assert(incoming[2] == std::byte(0xcd));

        // a port is the same ring, said once instead of at every call site: it remembers the
        // peer and the label, so the transfers below name neither
        auto upstream = world.port(previous, 31);
        // and one for the neighbor i speak to
        auto downstream = world.port(next, 31);
        // which remember what they were built with
        assert(upstream.peer() == previous);
        assert(downstream.tag() == 31);

        // pass a value around the ring through the ports; the even ranks speak first, as before
        int relayed = -1;
        // so split on parity
        if (rank % 2 == 0) {
            downstream.send(rank);
            upstream.recv(relayed);
        } else {
            upstream.recv(relayed);
            downstream.send(rank);
        }
        // and the value came round
        assert(relayed == previous);

        // the ports move text as readily as they move cells
        pyre::mpi::string_t greeting;
        // the even ranks speak first
        if (rank % 2 == 0) {
            downstream.sendString("hello " + std::to_string(next));
            greeting = upstream.recvString();
        } else {
            greeting = upstream.recvString();
            downstream.sendString("hello " + std::to_string(next));
        }
        // and the text arrived whole, sized by the message rather than by a terminating null
        assert(greeting == "hello " + std::to_string(rank));

        // the nonblocking transfers work through a port too, and need no parity split
        int posted = -1;
        // start listening upstream
        auto listener = upstream.irecv(posted);
        // and speaking downstream
        auto speaker = downstream.isend(rank);
        // block until both are done
        speaker.wait();
        listener.wait();
        // and the value came round once more
        assert(posted == previous);

        // broadcasting a payload works the same way: only the root knows how long it is, and
        // everybody else learns the extent from the call itself
        pyre::mpi::bytes_t payload;
        // the root brings the bytes
        if (rank == 0) {
            payload = pyre::mpi::bytes_t { std::byte(1), std::byte(2), std::byte(3),
                                           std::byte(4) };
        }
        // send them out
        world.bcast(payload, 0);
        // everybody now holds all four
        assert(payload.size() == 4);
        // and they are the ones the root brought
        assert(payload[3] == std::byte(4));
    }

    // take mpi down
    pyre::mpi::finalize();

    // all done
    return 0;
}


// end of file
