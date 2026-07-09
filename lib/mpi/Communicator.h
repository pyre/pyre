// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"

// the owner of my handle, and the recipe it uses to release it
#include "traits.h"
#include "Handle.h"
// the entities i hand back by value; {Cartesian} is not among them, since it derives from me
// and so cannot be complete before i am, and a declaration is all my factory needs
#include "Group.h"
#include "Status.h"
#include "Request.h"


// a group of processes, together with the context that keeps their messages from colliding
// with anybody else's
class pyre::mpi::Communicator {
    // types
public:
    // the opaque token mpi uses to name a communicator
    using handle_type = MPI_Comm;
    // the shared owner of that token
    using storage_type = Handle<CommunicatorHandle>;
    // the set of processes i hold
    using group_type = Group;
    // a collection of ranks
    using ranks_type = ranks_t;
    // the name the original interface gave the same thing; kept so old clients still compile
    using ranklist_t = ranks_t;

    // metamethods
public:
    // adopt an existing {handle}; {immortal} marks the communicators mpi predefines
    explicit inline Communicator(handle_type handle, bool immortal = false);
    // the full set; copies share the handle, moves steal it
    inline Communicator(const Communicator &) = default;
    inline Communicator(Communicator &&) noexcept = default;
    inline Communicator & operator=(const Communicator &) = default;
    inline Communicator & operator=(Communicator &&) noexcept = default;
    inline ~Communicator() = default;

    // structure
public:
    // the raw token, for handing to the mpi c api
    inline auto handle() const -> handle_type;
    // whether i name no communicator at all
    inline auto isNull() const -> bool;
    // contextual conversion to {bool}, true when i name a communicator
    explicit inline operator bool() const;

    // the rank of the calling process within me
    inline auto rank() const -> rank_t;
    // how many processes i hold
    inline auto size() const -> size_type;
    // the set of processes i hold
    inline auto group() const -> group_type;

    // how my membership and context relate to {other}'s
    inline auto compare(const Communicator & other) const -> Comparison;

    // communicator factories
public:
    // build the communicator that holds exactly the processes of {group}; this is collective
    // over me, and the ranks left out of {group} get the null communicator back
    inline auto communicator(const group_type & group) const -> Communicator;
    // split me into one communicator per distinct {color}, ranking each by {key}; this is
    // collective over me
    inline auto split(int color, int key) const -> Communicator;
    // build a communicator with my membership but a fresh context
    inline auto duplicate() const -> Communicator;
    // arrange my processes on a grid of the given {shape}, wrapping the axes flagged in
    // {periods}, and letting mpi renumber them when {reorder} is set
    inline auto cartesian(const shape_t & shape, const shape_t & periods, int reorder) const
        -> Cartesian;

    // collective operations
public:
    // block until every one of my processes arrives here
    inline auto barrier() const -> void;

    // send {value} from {root} to every one of my processes
    template <typename cellT>
    inline auto bcast(cellT & value, rank_t root) const -> void;
    // the same, for a block of cells whose extent every process already agrees on
    template <typename cellT>
    inline auto bcast(std::vector<cellT> & values, rank_t root) const -> void;
    // the same, for a payload whose extent only {root} knows; the others are resized to match
    inline auto bcast(bytes_t & payload, rank_t root) const -> void;

    // combine the {value} of every process with {op}, delivering the answer to {root} alone;
    // the answer is meaningful only at {root}
    template <typename cellT>
    inline auto reduce(const cellT & value, Op op, rank_t root) const -> cellT;
    // the same, delivering the answer to every process
    template <typename cellT>
    inline auto allreduce(const cellT & value, Op op) const -> cellT;
    // the same, combining the cells of {values} elementwise
    template <typename cellT>
    inline auto allreduce(const std::vector<cellT> & values, Op op) const -> std::vector<cellT>;

    // combine the {value} of every process with {op}, delivering to each the answer over all
    // the processes that precede it, itself included
    template <typename cellT>
    inline auto scan(const cellT & value, Op op) const -> cellT;
    // the same, itself excluded; the answer is meaningless at rank zero
    template <typename cellT>
    inline auto exscan(const cellT & value, Op op) const -> cellT;

    // collect the {value} of every process at {root}, in rank order; the answer is empty
    // everywhere but {root}
    template <typename cellT>
    inline auto gather(const cellT & value, rank_t root) const -> std::vector<cellT>;
    // the same, delivering the answer to every process
    template <typename cellT>
    inline auto allgather(const cellT & value) const -> std::vector<cellT>;
    // hand the nth cell of {values} to the nth process; {values} matters only at {root}
    template <typename cellT>
    inline auto scatter(const std::vector<cellT> & values, rank_t root) const -> cellT;
    // hand the nth cell of every process's {values} to the nth process
    template <typename cellT>
    inline auto alltoall(const std::vector<cellT> & values) const -> std::vector<cellT>;

    // point to point operations
public:
    // send {value} to {peer}, labelled with {tag}
    template <typename cellT>
    inline auto send(const cellT & value, rank_t peer, tag_t tag = 0) const -> void;
    // block until a matching message arrives from {peer}, and fill {value} with it
    template <typename cellT>
    inline auto recv(cellT & value, rank_t peer, tag_t tag = anyTag) const -> Status;

    // send a block of cells to {peer}
    template <typename cellT>
    inline auto send(const std::vector<cellT> & values, rank_t peer, tag_t tag = 0) const -> void;
    // block until a matching message arrives, sizing {values} to hold exactly what came
    template <typename cellT>
    inline auto recv(std::vector<cellT> & values, rank_t peer, tag_t tag = anyTag) const -> Status;

    // send a raw payload to {peer}; this is the path the pickling layer takes
    inline auto sendBytes(const bytes_t & payload, rank_t peer, tag_t tag = 0) const -> void;
    // block until a raw payload arrives, sizing the answer to hold exactly what came
    inline auto recvBytes(rank_t peer, tag_t tag = anyTag) const -> bytes_t;

    // wait for a matching message to arrive, without receiving it, and report on it
    inline auto probe(rank_t peer, tag_t tag = anyTag) const -> Status;
    // send to one peer and receive from another in a single call, which mpi is free to
    // schedule without deadlocking
    template <typename cellT>
    inline auto sendrecv(
        const cellT & outgoing, rank_t destination, cellT & incoming, rank_t source,
        tag_t tag = 0) const -> Status;

    // start sending {value} to {peer}, and hand back the receipt
    template <typename cellT>
    inline auto isend(const cellT & value, rank_t peer, tag_t tag = 0) const -> Request;
    // start receiving into {value}, which must outlive the transfer, and hand back the receipt
    template <typename cellT>
    inline auto irecv(cellT & value, rank_t peer, tag_t tag = anyTag) const -> Request;

    // process control
public:
    // bring down every process i hold, handing {code} to the environment
    inline auto abort(int code) const -> void;

    // data
private:
    // the token i own
    storage_type _handle;
};


// get the inline definitions
#include "Communicator.icc"


// end of file
