// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// translate one of my reduction operators into the handle mpi expects
auto
pyre::mpi::opcode(Op op) -> opcode_t
{
    // dispatch on the operator
    switch (op) {
        // arithmetic
        case Op::sum:
            return MPI_SUM;
        case Op::product:
            return MPI_PROD;
        case Op::maximum:
            return MPI_MAX;
        case Op::minimum:
            return MPI_MIN;
        // logical
        case Op::logicalAnd:
            return MPI_LAND;
        case Op::logicalOr:
            return MPI_LOR;
        case Op::logicalXor:
            return MPI_LXOR;
        // bitwise
        case Op::bitwiseAnd:
            return MPI_BAND;
        case Op::bitwiseOr:
            return MPI_BOR;
        case Op::bitwiseXor:
            return MPI_BXOR;
        // the extrema, paired with the rank that supplied them
        case Op::maxloc:
            return MPI_MAXLOC;
        case Op::minloc:
            return MPI_MINLOC;
        // the last value wins
        case Op::replace:
            return MPI_REPLACE;
    }

    // an operator outside the enumeration means somebody added a case and forgot this switch
    auto channel = pyre::journal::firewall_t("pyre.mpi.op");
    // complain
    channel
        // what
        << "unknown reduction operator"
        << pyre::journal::newline
        // details
        << "value: " << static_cast<int>(op)
        // where, and flush
        << pyre::journal::endl(__HERE__);

    // not reached, since the firewall is fatal; here so every path returns
    return MPI_OP_NULL;
}


// translate the answer of an mpi comparison into one of my labels
auto
pyre::mpi::comparison(int result) -> Comparison
{
    // the two handles name the very same object
    if (result == MPI_IDENT) {
        return Comparison::identical;
    }
    // the same members in the same order, but distinct communication contexts
    if (result == MPI_CONGRUENT) {
        return Comparison::congruent;
    }
    // the same members, ranked differently
    if (result == MPI_SIMILAR) {
        return Comparison::similar;
    }
    // nothing in common
    if (result == MPI_UNEQUAL) {
        return Comparison::unequal;
    }

    // anything else means mpi answered with a value its own standard does not define
    auto channel = pyre::journal::firewall_t("pyre.mpi.comparison");
    // complain
    channel
        // what
        << "unknown comparison result"
        << pyre::journal::newline
        // details
        << "value: " << result
        // where, and flush
        << pyre::journal::endl(__HERE__);

    // not reached, since the firewall is fatal; here so every path returns
    return Comparison::unequal;
}


// end of file
