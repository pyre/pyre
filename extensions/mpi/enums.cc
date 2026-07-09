// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// add the enumerations to the module
void
pyre::mpi::py::enums(py::module & m)
{
    // the operators that the reductions know how to apply
    py::enum_<Op>(m, "Op", "the reduction operators")
        // arithmetic
        .value("sum", Op::sum, "add the contributions")
        .value("product", Op::product, "multiply the contributions")
        .value("maximum", Op::maximum, "the largest contribution")
        .value("minimum", Op::minimum, "the smallest contribution")
        // logical
        .value("logicalAnd", Op::logicalAnd, "the truth of every contribution")
        .value("logicalOr", Op::logicalOr, "the truth of any contribution")
        .value("logicalXor", Op::logicalXor, "the truth of exactly one contribution")
        // bitwise
        .value("bitwiseAnd", Op::bitwiseAnd, "the bits set in every contribution")
        .value("bitwiseOr", Op::bitwiseOr, "the bits set in any contribution")
        .value("bitwiseXor", Op::bitwiseXor, "the bits set in exactly one contribution")
        // the extrema, paired with the rank that supplied them
        .value("maxloc", Op::maxloc, "the largest contribution, and who made it")
        .value("minloc", Op::minloc, "the smallest contribution, and who made it")
        // the last value wins
        .value("replace", Op::replace, "the last contribution");

    // the outcome of comparing two communicators or two groups
    py::enum_<Comparison>(m, "Comparison", "the outcome of a comparison")
        .value("identical", Comparison::identical, "the two handles name the same object")
        .value("congruent", Comparison::congruent, "the same members, in the same order")
        .value("similar", Comparison::similar, "the same members, in a different order")
        .value("unequal", Comparison::unequal, "nothing in common");

    // how much of the mpi interface a threaded process may use
    py::enum_<Thread>(m, "Thread", "the levels of thread support")
        .value("single", Thread::single, "only one thread will execute")
        .value("funneled", Thread::funneled, "only the thread that brought mpi up will call it")
        .value("serialized", Thread::serialized, "any thread may call mpi, but never two at once")
        .value("multiple", Thread::multiple, "any thread may call mpi at any time");

    // all done
    return;
}


// end of file
