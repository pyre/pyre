// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// externals
#include "external.h"

// the static map from generator name to gsl_rng_type pointer
static std::map<std::string, const gsl_rng_type *> _rng_types;

namespace pyre::gsl::py {

// populate the map once at module load
void
rng_initialize()
{
    // ask GSL for the null-terminated array of all known generator types
    const gsl_rng_type ** types = gsl_rng_types_setup();
    // iterate until we hit the null sentinel
    for (const gsl_rng_type ** t = types; *t != nullptr; ++t) {
        _rng_types[(*t)->name] = *t;
    }
    // all done
    return;
}

void
rng(::py::module & m)
{
    // register the RNG type
    ::py::class_<pyre::gsl::RNG>(m, "RNG");

    // return all known generator names as a frozenset
    m.def(
        "rng_avail",
        []() {
            ::py::set names;
            for (auto & [name, _] : _rng_types) {
                names.add(name);
            }
            return ::py::frozenset(names);
        },
        "return all known generator names");

    // allocate a new rng of the named type
    m.def(
        "rng_alloc",
        [](const std::string & name) {
            // look up the type
            auto it = _rng_types.find(name);
            if (it == _rng_types.end()) {
                throw std::invalid_argument("unknown rng type: " + name);
            }
            return std::make_unique<pyre::gsl::RNG>(it->second);
        },
        "name"_a,
        "allocate a new random number generator of the named type");

    // seed the generator
    m.def(
        "rng_set",
        [](pyre::gsl::RNG & r, unsigned long seed) {
            gsl_rng_set(r.ptr, seed);
        },
        "r"_a, "seed"_a,
        "seed the random number generator");

    // return the generator name
    m.def(
        "rng_name",
        [](pyre::gsl::RNG & r) {
            return std::string(gsl_rng_name(r.ptr));
        },
        "r"_a,
        "return the name of the random number generator");

    // return the (min, max) range of the generator
    m.def(
        "rng_range",
        [](pyre::gsl::RNG & r) {
            return ::py::make_tuple(gsl_rng_min(r.ptr), gsl_rng_max(r.ptr));
        },
        "r"_a,
        "return the (min, max) range of the random number generator");

    // get the next random integer
    m.def(
        "rng_get",
        [](pyre::gsl::RNG & r) -> unsigned long {
            return gsl_rng_get(r.ptr);
        },
        "r"_a,
        "return the next random integer from the generator");

    // get the next uniform random double in [0, 1)
    m.def(
        "rng_uniform",
        [](pyre::gsl::RNG & r) -> double {
            return gsl_rng_uniform(r.ptr);
        },
        "r"_a,
        "return the next uniform random double in [0, 1)");
}

} // namespace pyre::gsl::py

// end of file
