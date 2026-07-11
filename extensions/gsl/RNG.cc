// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"
// the generators
#include <gsl/gsl_rng.h>
// the catalogue of generator names crosses as a set
#include <set>


// the local helpers
namespace gsl::py {
    // gsl allocates every generator through {gsl_rng_alloc} and releases it through
    // {gsl_rng_free}, so the handle python holds owns exactly one of them
    struct rngDeleter {
        void operator()(gsl_rng * r) const
        {
            // release the generator, if there is one
            if (r) {
                gsl_rng_free(r);
            }
        }
    };
    using rng_ptr = std::unique_ptr<gsl_rng, rngDeleter>;

    // find the generator type that answers to {name}
    //
    // gsl keeps no lookup of its own; it hands out a null terminated array of the types it knows,
    // and leaves the matching to us
    inline auto generator(const std::string & name) -> const gsl_rng_type *
    {
        // walk the types gsl knows
        for (const gsl_rng_type ** t = gsl_rng_types_setup(); *t != nullptr; ++t) {
            // until one answers to the name we were given
            if (name == (*t)->name) {
                // and hand it back
                return *t;
            }
        }
        // otherwise, there is no such generator
        return nullptr;
    }
} // namespace gsl::py


// add the bindings for the gsl random number generator
void
gsl::py::rng(py::module & m)
{
    // the class
    auto cls = py::class_<gsl_rng, rng_ptr>(
        // in scope
        m,
        // the name
        "RNG",
        // the docstring
        "a pseudo-random number generator from gsl");

    // build a generator that runs the named {algorithm}
    cls.def(
        // the implementation
        py::init([](const std::string & algorithm) -> rng_ptr {
            // look the algorithm up
            const gsl_rng_type * type = generator(algorithm);
            // and if there is no such thing
            if (!type) {
                // say so
                throw py::value_error("unknown random number generator '" + algorithm + "'");
            }
            // otherwise, allocate one, remembering how it is released
            return rng_ptr(gsl_rng_alloc(type));
        }),
        // the signature
        "algorithm"_a,
        // the docstring
        "build a generator that runs the named {algorithm}");

    // the name of the algorithm i run
    cls.def_property_readonly(
        // the name
        "algorithm",
        // the implementation
        [](const gsl_rng & self) -> std::string { return gsl_rng_name(&self); },
        // the docstring
        "the name of the algorithm i run");

    // the range of integers i draw from
    cls.def_property_readonly(
        // the name
        "range",
        // the implementation
        [](const gsl_rng & self) -> std::pair<unsigned long, unsigned long> {
            // the smallest and largest value i return
            return { gsl_rng_min(&self), gsl_rng_max(&self) };
        },
        // the docstring
        "the smallest and largest integer i draw, as a pair");

    // seed me
    //
    // the lambda takes and returns the python object rather than the {gsl_rng}, so that the call
    // hands back the very generator it was called on, letting callers chain off it; returning the
    // {gsl_rng} would instead wrap it in a second owning handle
    cls.def(
        // the name
        "seed",
        // the implementation
        [](py::object self, unsigned long seed) -> py::object {
            // seed the generator behind {self}
            gsl_rng_set(&self.cast<gsl_rng &>(), seed);
            // and hand it back
            return self;
        },
        // the signature
        "seed"_a = 0,
        // the docstring
        "seed me with the given value, and return me");

    // draw a real from the unit interval
    cls.def(
        // the name
        "float",
        // the implementation
        [](gsl_rng & self) -> double { return gsl_rng_uniform(&self); },
        // the docstring
        "draw a real uniformly from the interval [0, 1)");

    // draw an integer from my range
    cls.def(
        // the name
        "int",
        // the implementation
        [](gsl_rng & self) -> unsigned long { return gsl_rng_get(&self); },
        // the docstring
        "draw an integer uniformly from my range");

    // the catalogue of the generators gsl was built with
    m.def(
        // the name
        "rng_avail",
        // the implementation
        []() -> std::set<std::string> {
            // room for the names
            std::set<std::string> names;
            // walk the types gsl knows
            for (const gsl_rng_type ** t = gsl_rng_types_setup(); *t != nullptr; ++t) {
                // and record each name
                names.insert((*t)->name);
            }
            // hand the set back
            return names;
        },
        // the docstring
        "the names of the random number generators gsl was built with");

    // all done
    return;
}


// end of file
