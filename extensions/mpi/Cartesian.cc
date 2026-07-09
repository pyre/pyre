// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// add the bindings for the cartesian communicator
void
pyre::mpi::py::cartesian(py::module & m)
{
    // the class, which derives from the plain communicator so that everything the base binds
    // is available here too
    auto cls = py::class_<Cartesian, Communicator>(
        // in scope
        m,
        // the name
        "Cartesian",
        // the docstring
        "a communicator whose processes are arranged on a grid");

    // the shape of the grid
    cls.def_property_readonly(
        // the name
        "dimensions",
        // the implementation
        &Cartesian::dimensions,
        // the docstring
        "the number of axes my grid has");

    cls.def_property_readonly(
        // the name
        "axes",
        // the implementation
        &Cartesian::shape,
        // the docstring
        "the extent of my grid along each axis");

    cls.def_property_readonly(
        // the name
        "periods",
        // the implementation
        &Cartesian::periods,
        // the docstring
        "which of my axes wrap around");

    // walking the grid
    cls.def(
        // the name
        "coordinates",
        // the implementation
        [](const Cartesian & self, std::optional<rank_t> rank) -> shape_t {
            // when nobody is named, the caller is asking about itself
            return self.coordinates(rank ? *rank : self.rank());
        },
        // the signature
        "rank"_a = py::none(),
        // the docstring
        "where the process of the given {rank} sits on my grid; with no {rank}, where this "
        "process sits");

    cls.def(
        // the name
        "rankAt",
        // the implementation; the cast is required because the class also carries the
        // inherited {rank()}, brought in by a using declaration, so the name alone is ambiguous
        py::overload_cast<const Cartesian::shape_type &>(&Cartesian::rank, py::const_),
        // the signature
        "coordinates"_a,
        // the docstring
        "the rank of the process that sits at {coordinates}; this cannot be spelled {rank}, "
        "which python has already given to the inherited property that names this process");

    cls.def(
        // the name
        "shift",
        // the implementation
        &Cartesian::shift,
        // the signature
        "direction"_a, "displacement"_a = 1,
        // the docstring
        "the ranks of the two processes {displacement} steps away along {direction}: the one "
        "that would send to me, and the one i would send to. either comes back as {procNull} "
        "when the axis does not wrap and the walk falls off its end");

    cls.def(
        // the name
        "sub",
        // the implementation
        &Cartesian::sub,
        // the signature
        "keep"_a,
        // the docstring
        "the sub-grid spanned by the axes flagged in {keep}; collective over me");

    // for the benefit of anybody staring at a prompt
    cls.def(
        // the name
        "__repr__",
        // the implementation
        [](const Cartesian & self) -> string_t {
            // start the summary
            string_t summary = "<mpi.Cartesian: rank " + std::to_string(self.rank()) + " at (";
            // walk my coordinates
            auto here = self.coordinates(self.rank());
            // rendering each
            for (decltype(here.size()) axis = 0; axis < here.size(); ++axis) {
                // separated by commas
                if (axis > 0) {
                    summary += ",";
                }
                // and spelled out
                summary += std::to_string(here[axis]);
            }
            // close it out
            return summary + ")>";
        },
        // the docstring
        "a human readable summary of this communicator");

    // all done
    return;
}


// end of file
