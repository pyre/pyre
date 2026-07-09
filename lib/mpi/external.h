// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// externals
#include <complex>
#include <cstddef>
#include <cstdint>
#include <exception>
#include <memory>
#include <optional>
#include <string>
#include <utility>
#include <vector>
// support
#include <pyre/journal.h>
// the mpi c api; {pyre::mpi} is a wrapper over it, and depends on nothing else
#include <mpi.h>


// the type aliases that shape this namespace
namespace pyre::mpi {
    // names and other text
    using string_t = std::string;
    // the identity of a process within a communicator or a group
    using rank_t = int;
    // a collection of ranks, e.g. the membership of a group
    using ranks_t = std::vector<rank_t>;
    // the number of processes in a communicator or a group; deliberately not {size_t}, which
    // would shadow the global for every unqualified use inside this namespace
    using size_type = int;
    // the label that distinguishes one message from another
    using tag_t = int;
    // the shape of a cartesian process grid, and the periodicity of each of its axes
    using shape_t = std::vector<int>;
    // an uninterpreted payload; {std::byte} is not a spelling of {char}, and the difference
    // matters: it deduces to {MPI_BYTE}, which mpi moves octet for octet, where {MPI_CHAR} is
    // text that mpi may translate between ranks of unlike architecture
    using bytes_t = std::vector<std::byte>;
    // the mpi description of the layout of a message element
    using datatype_t = MPI_Datatype;
    // the mpi handle of a reduction operator
    using opcode_t = MPI_Op;
} // namespace pyre::mpi


// the mpi constants, hoisted out of the macros the c api hands us
namespace pyre::mpi {
    // the answer when mpi cannot place a process in a group
    inline constexpr rank_t undefined = MPI_UNDEFINED;
    // the wildcard that lets a receive match a message from any sender
    inline constexpr rank_t anySource = MPI_ANY_SOURCE;
    // the rank that names a peer with which communication is a no-op
    inline constexpr rank_t procNull = MPI_PROC_NULL;
    // the wildcard that lets a receive match a message carrying any label
    inline constexpr tag_t anyTag = MPI_ANY_TAG;
} // namespace pyre::mpi


// end of file
