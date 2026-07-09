// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// external packages and the type aliases that shape this namespace
#include "external.h"


// the pyre-owned wrappers over the mpi c api
namespace pyre::mpi {
    // the exception hierarchy
    // the base of everything this package throws
    class Error;
    // a failed mpi call, carrying the status code it returned
    class MPIError;
    // an argument whose shape does not match what the call requires
    class ShapeError;

    // the owner of an mpi object handle
    template <class traitsT>
    class Handle;
    // the recipes that teach {Handle} how to release each kind of mpi object
    struct CommunicatorHandle;
    struct GroupHandle;

    // the outcome of a completed message transfer
    class Status;
    // the receipt of a message transfer that is still in flight
    class Request;

    // a set of processes
    class Group;
    // a group, together with the context that isolates its messages
    class Communicator;
    // a communicator whose processes are arranged on a cartesian grid
    class Cartesian;
    // a conduit between this process and one fixed peer
    class Port;
} // namespace pyre::mpi


// error handling
namespace pyre::mpi {
    // turn a failed mpi status code into an exception
    inline auto check(int status) -> void;
} // namespace pyre::mpi


// datatype deduction: the mpi description of the layout of a {cellT}
namespace pyre::mpi {
    // the generic case; instantiating it is an error, since only the specializations below
    // name a type that mpi knows how to move
    template <typename cellT>
    inline auto datatype() -> datatype_t;

    // the fixed width integral types; note the deliberate absence of {long} and
    // {unsigned long}: they are the same type as {int64_t} and {uint64_t} on LP64, so
    // specializing both would be a redefinition
    template <>
    inline auto datatype<std::int8_t>() -> datatype_t;
    template <>
    inline auto datatype<std::int16_t>() -> datatype_t;
    template <>
    inline auto datatype<std::int32_t>() -> datatype_t;
    template <>
    inline auto datatype<std::int64_t>() -> datatype_t;
    template <>
    inline auto datatype<std::uint8_t>() -> datatype_t;
    template <>
    inline auto datatype<std::uint16_t>() -> datatype_t;
    template <>
    inline auto datatype<std::uint32_t>() -> datatype_t;
    template <>
    inline auto datatype<std::uint64_t>() -> datatype_t;
    // the floating point types
    template <>
    inline auto datatype<float>() -> datatype_t;
    template <>
    inline auto datatype<double>() -> datatype_t;
    template <>
    inline auto datatype<long double>() -> datatype_t;
    // the complex types
    template <>
    inline auto datatype<std::complex<float>>() -> datatype_t;
    template <>
    inline auto datatype<std::complex<double>>() -> datatype_t;
    // the character and truth types, each distinct from the fixed width integrals above
    template <>
    inline auto datatype<char>() -> datatype_t;
    template <>
    inline auto datatype<bool>() -> datatype_t;
    // raw memory, which mpi moves without interpreting
    template <>
    inline auto datatype<std::byte>() -> datatype_t;
} // namespace pyre::mpi


// the reduction operators
namespace pyre::mpi {
    // the operators that {reduce} and its relatives know how to apply
    enum class Op {
        // arithmetic
        sum,
        product,
        maximum,
        minimum,
        // logical
        logicalAnd,
        logicalOr,
        logicalXor,
        // bitwise
        bitwiseAnd,
        bitwiseOr,
        bitwiseXor,
        // the extrema, paired with the rank that supplied them
        maxloc,
        minloc,
        // the last value wins
        replace,
    };

    // translate one of my operators into the handle mpi expects
    inline auto opcode(Op op) -> opcode_t;
} // namespace pyre::mpi


// the outcome of comparing two communicators or two groups
namespace pyre::mpi {
    enum class Comparison {
        // the two handles name the same object
        identical,
        // the same members, in the same order, but distinct contexts
        congruent,
        // the same members, in a different order
        similar,
        // nothing in common
        unequal,
    };

    // translate the answer of an mpi comparison into one of my labels
    inline auto comparison(int result) -> Comparison;
} // namespace pyre::mpi


// how much of the mpi interface a threaded process may use
namespace pyre::mpi {
    // the four levels, in the order of increasing freedom that the standard guarantees, so that
    // comparing two of them answers the question a caller actually has: is this enough?
    enum class Thread {
        // only one thread will execute
        single,
        // only the thread that brought mpi up will call it
        funneled,
        // any thread may call mpi, but never two at once
        serialized,
        // any thread may call mpi at any time
        multiple,
    };

    // translate one of my levels into the constant mpi expects. mpi fixes the names of these
    // four and their order, but not the type: openmpi makes them an anonymous enum, while
    // mpich makes them an {int}. so neither spelling may escape this package
    inline auto threadLevel(Thread thread) -> int;
    // and translate mpi's answer back into one of my labels
    inline auto threadSupport(int level) -> Thread;
} // namespace pyre::mpi


// the group set operations, which are free functions because none of their arguments is
// privileged
namespace pyre::mpi {
    // the processes that belong to either group
    inline auto groupUnion(const Group &, const Group &) -> Group;
    // the processes that belong to both groups
    inline auto groupIntersection(const Group &, const Group &) -> Group;
    // the processes of the first group that do not belong to the second
    inline auto groupDifference(const Group &, const Group &) -> Group;
} // namespace pyre::mpi


// the runtime
namespace pyre::mpi {
    // bring mpi up, asking for the given level of thread support, and report the level granted
    inline auto initialize(Thread required = Thread::single) -> Thread;
    // take mpi down
    inline auto finalize() -> void;
    // whether {initialize} has been called
    inline auto initialized() -> bool;
    // whether {finalize} has been called
    inline auto finalized() -> bool;

    // the communicator that holds every process in the job
    inline auto world() -> Communicator;
    // the communicator that holds this process alone
    inline auto self() -> Communicator;
    // the communicator that holds no processes at all
    inline auto null() -> Communicator;

    // seconds elapsed on this process since some fixed point in its past
    inline auto wtime() -> double;
    // the resolution of {wtime}, in seconds
    inline auto wtick() -> double;
    // the name of the host this process is running on
    inline auto processorName() -> string_t;
} // namespace pyre::mpi


// end of file
