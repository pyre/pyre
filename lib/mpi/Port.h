// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"

// the communicator i carry, and the entities i hand back by value
#include "Communicator.h"
#include "Request.h"
#include "Status.h"


// a conduit between this process and one fixed peer
//
// a port is a communicator, a peer, and a message label, remembered together. that is all it
// is, and it is what turns a stencil sweep from a litany of repeated {peer} and {tag} arguments
// into a conversation with a named neighbor
class pyre::mpi::Port {
    // types
public:
    // me
    using self_type = Port;
    // the context my peer and i share
    using communicator_type = Communicator;

    // metamethods
public:
    // build a conduit to {peer} over {communicator}, whose messages carry {tag}
    inline Port(communicator_type communicator, rank_t peer, tag_t tag = 0);
    // the full set; a port is a communicator and two numbers
    inline Port(const Port &) = default;
    inline Port(Port &&) noexcept = default;
    inline Port & operator=(const Port &) = default;
    inline Port & operator=(Port &&) noexcept = default;
    inline ~Port() = default;

    // structure
public:
    // the communicator my peer and i belong to
    inline auto communicator() const -> const communicator_type &;
    // the process at the other end
    inline auto peer() const -> rank_t;
    // the label my messages carry
    inline auto tag() const -> tag_t;

    // blocking transfers
public:
    // ship one cell to my peer
    template <typename cellT>
    inline auto send(const cellT & value) const -> void;
    // block until my peer sends me one, and fill {value} with it
    template <typename cellT>
    inline auto recv(cellT & value) const -> Status;

    // ship a block of cells to my peer
    template <typename cellT>
    inline auto send(const std::vector<cellT> & values) const -> void;
    // block until a block arrives, sizing {values} to hold exactly what came
    template <typename cellT>
    inline auto recv(std::vector<cellT> & values) const -> Status;

    // ship a raw payload to my peer; this is the path a serializer rides on
    inline auto sendBytes(const bytes_t & payload) const -> void;
    // block until a raw payload arrives, sizing the answer to hold exactly what came
    inline auto recvBytes() const -> bytes_t;

    // ship text to my peer
    inline auto sendString(const string_t & message) const -> void;
    // block until text arrives, sizing the answer to hold exactly what came
    inline auto recvString() const -> string_t;

    // wait for a message from my peer to arrive, without receiving it
    inline auto probe() const -> Status;
    // ask whether a message from my peer has already arrived, without waiting for one to
    inline auto iprobe() const -> std::optional<Status>;

    // nonblocking transfers
public:
    // start shipping {value} to my peer, and hand back the receipt
    template <typename cellT>
    inline auto isend(const cellT & value) const -> Request;
    // start receiving into {value}, which must outlive the transfer, and hand back the receipt
    template <typename cellT>
    inline auto irecv(cellT & value) const -> Request;

    // start shipping the {extent} octets at {data}; the buffer belongs to the caller, and must
    // outlive the transfer
    inline auto isendBytes(const void * data, size_type extent) const -> Request;
    // start receiving {extent} octets into {data}; as above, the buffer belongs to the caller
    inline auto irecvBytes(void * data, size_type extent) const -> Request;

    // data
private:
    // the communicator my peer and i belong to
    communicator_type _communicator;
    // the process at the other end
    rank_t _peer;
    // the label my messages carry
    tag_t _tag;
};


// get the inline definitions
#include "Port.icc"


// end of file
