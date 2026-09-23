// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// forward declarations
#include "forward.h"
// my declarations
#include "__init__.h"
// shared handle/pointer support
#include "support.h"


// local support, not part of the public interface
namespace {
    // translate a curand status into a python exception; like cusolver, curand has no string
    // translator of its own
    inline auto
    checkStatus(curandStatus_t status, const char * routine) -> void
    {
        if (status == CURAND_STATUS_SUCCESS) {
            return;
        }
        throw std::runtime_error(
            std::string(routine) + ": curand error " + std::to_string(static_cast<int>(status)));
    }
} // namespace


// build the {curand} submodule
auto
pyre::py::cuda::curand::__init__(py::module & m) -> void
{
    // make the submodule
    auto curand = m.def_submodule("curand", "thin bindings for curand");

    // the generator families; only the pseudo-random ones are exposed, since those are what a
    // sampler wants
    py::enum_<curandRngType_t>(curand, "RngType", "which pseudo-random generator to allocate")
        .value("DEFAULT", CURAND_RNG_PSEUDO_DEFAULT, "the default xorwow generator")
        .value("XORWOW", CURAND_RNG_PSEUDO_XORWOW, "xorwow")
        .value("MRG32K3A", CURAND_RNG_PSEUDO_MRG32K3A, "mrg32k3a")
        .value("PHILOX4_32_10", CURAND_RNG_PSEUDO_PHILOX4_32_10, "philox4x32-10");

    // generator lifetime, same convention as {cublas}/{cusolver}: an explicit handle on every
    // call, nothing hidden behind these functions
    curand.def(
        "create_generator",
        [](curandRngType_t rngType) -> std::uintptr_t {
            curandGenerator_t generator = nullptr;
            checkStatus(curandCreateGenerator(&generator, rngType), "create_generator");
            return fromHandle(generator);
        },
        "rngType"_a,
        "allocate a curand generator of the requested type");

    curand.def(
        "destroy_generator",
        [](std::uintptr_t handle) -> void {
            checkStatus(
                curandDestroyGenerator(toHandle<curandGenerator_t>(handle)), "destroy_generator");
        },
        "handle"_a,
        "release a curand generator");

    curand.def(
        "set_seed",
        [](std::uintptr_t handle, unsigned long long seed) -> void {
            checkStatus(
                curandSetPseudoRandomGeneratorSeed(toHandle<curandGenerator_t>(handle), seed),
                "set_seed");
        },
        "handle"_a, "seed"_a,
        "seed a pseudo-random generator");

    // fill {n} cells of {out}, starting at its first cell, with draws from a distribution;
    // {n} need not be the grid's full cell count, so a caller may fill a sub-grid's leading
    // run without allocating a separate buffer for it
    curand.def(
        "generate_uniform_double",
        [](std::uintptr_t handle, grid::AnyGrid & out, std::size_t n) -> void {
            checkStatus(
                curandGenerateUniformDouble(
                    toHandle<curandGenerator_t>(handle),
                    static_cast<double *>(data(out, 'd', "generate_uniform_double")), n),
                "generate_uniform_double");
            synchronize("generate_uniform_double");
        },
        "handle"_a, "out"_a, "n"_a,
        "fill the first {n} cells of {out} with draws from U(0, 1], {float64} cells");

    curand.def(
        "generate_normal_double",
        [](std::uintptr_t handle, grid::AnyGrid & out, std::size_t n, double mean,
           double stddev) -> void {
            checkStatus(
                curandGenerateNormalDouble(
                    toHandle<curandGenerator_t>(handle),
                    static_cast<double *>(data(out, 'd', "generate_normal_double")), n, mean,
                    stddev),
                "generate_normal_double");
            synchronize("generate_normal_double");
        },
        "handle"_a, "out"_a, "n"_a, "mean"_a, "stddev"_a,
        "fill the first {n} cells of {out} with draws from N(mean, stddev^2), {float64} "
        "cells; curand requires {n} to be even");
}


// end of file
