// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// forward declarations
#include "forward.h"
// the support shared by the library bindings
#include "support.h"


// the vocabulary of the bindings
namespace {
    // the type-erased grid
    using AnyGrid = pyre::py::grid::AnyGrid;
    // the argument literals
    using namespace pybind11::literals;

    // raise the failure the curand {status} of {routine} reports
    auto check(curandStatus_t status, const char * routine) -> void
    {
        // if there is one
        if (status != CURAND_STATUS_SUCCESS) {
            // say so
            throw std::runtime_error(
                std::string(routine) + ": curand error "
                + std::to_string(static_cast<int>(status)));
        }
        // all done
        return;
    }
} // namespace


// the curand bindings
auto
pyre::cuda::py::curand(py::module & m) -> void
{
    // the submodule
    auto curand = m.def_submodule(
        // the name
        "curand",
        // the docstring
        "thin bindings for the curand host api, over grids on managed memory");

    // the pseudo-random generators
    py::enum_<curandRngType_t>(curand, "RngType", "which pseudo-random generator to allocate")
        // the default
        .value("DEFAULT", CURAND_RNG_PSEUDO_DEFAULT, "the default xorwow generator")
        // xorwow
        .value("XORWOW", CURAND_RNG_PSEUDO_XORWOW, "xorwow")
        // mrg32k3a
        .value("MRG32K3A", CURAND_RNG_PSEUDO_MRG32K3A, "mrg32k3a")
        // philox
        .value("PHILOX4_32_10", CURAND_RNG_PSEUDO_PHILOX4_32_10, "philox4x32-10");

    // a generator
    curand.def(
        // the name
        "create_generator",
        // the implementation
        [](curandRngType_t rngType) -> std::uintptr_t {
            // make room for the generator
            curandGenerator_t generator = nullptr;
            // make one
            check(curandCreateGenerator(&generator, rngType), "create_generator");
            // and hand it off, as the integer python carries
            return fromHandle(generator);
        },
        // the signature
        "rngType"_a,
        // the docstring
        "allocate a curand generator of type {rngType}");

    // the release of a generator
    curand.def(
        // the name
        "destroy_generator",
        // the implementation
        [](std::uintptr_t handle) -> void {
            // release it
            check(curandDestroyGenerator(toHandle<curandGenerator_t>(handle)), "destroy_generator");
            // all done
            return;
        },
        // the signature
        "handle"_a,
        // the docstring
        "release the curand generator {handle}");

    // the seed of a generator
    curand.def(
        // the name
        "set_seed",
        // the implementation
        [](std::uintptr_t handle, unsigned long long seed) -> void {
            // seed it
            check(
                curandSetPseudoRandomGeneratorSeed(toHandle<curandGenerator_t>(handle), seed),
                "set_seed");
            // all done
            return;
        },
        // the signature
        "handle"_a, "seed"_a,
        // the docstring
        "seed the pseudo-random generator {handle} with {seed}");

    // draws from the uniform distribution, into float64 cells
    curand.def(
        // the name
        "generate_uniform_double",
        // the implementation
        [](std::uintptr_t handle, AnyGrid & out, std::size_t n) -> void {
            // draw
            check(
                curandGenerateUniformDouble(
                    toHandle<curandGenerator_t>(handle),
                    static_cast<double *>(data(out, 'd', "generate_uniform_double")), n),
                "generate_uniform_double");
            // all done
            return;
        },
        // the signature
        "handle"_a, "out"_a, "n"_a,
        // the docstring
        "fill the first {n} cells of {out} with draws from U(0, 1], over {float64} cells");

    // draws from the normal distribution, into float64 cells
    curand.def(
        // the name
        "generate_normal_double",
        // the implementation
        [](std::uintptr_t handle, AnyGrid & out, std::size_t n, double mean,
           double stddev) -> void {
            // draw
            check(
                curandGenerateNormalDouble(
                    toHandle<curandGenerator_t>(handle),
                    static_cast<double *>(data(out, 'd', "generate_normal_double")), n, mean,
                    stddev),
                "generate_normal_double");
            // all done
            return;
        },
        // the signature
        "handle"_a, "out"_a, "n"_a, "mean"_a, "stddev"_a,
        // the docstring
        "fill the first {n} cells of {out} with draws from N(mean, stddev^2), over {float64} "
        "cells; {n} must be even");

    // draws from the uniform distribution, into float32 cells
    curand.def(
        // the name
        "generate_uniform",
        // the implementation
        [](std::uintptr_t handle, AnyGrid & out, std::size_t n) -> void {
            // draw
            check(
                curandGenerateUniform(
                    toHandle<curandGenerator_t>(handle),
                    static_cast<float *>(data(out, 'f', "generate_uniform")), n),
                "generate_uniform");
            // all done
            return;
        },
        // the signature
        "handle"_a, "out"_a, "n"_a,
        // the docstring
        "fill the first {n} cells of {out} with draws from U(0, 1], over {float32} cells");

    // draws from the normal distribution, into float32 cells
    curand.def(
        // the name
        "generate_normal",
        // the implementation
        [](std::uintptr_t handle, AnyGrid & out, std::size_t n, float mean, float stddev) -> void {
            // draw
            check(
                curandGenerateNormal(
                    toHandle<curandGenerator_t>(handle),
                    static_cast<float *>(data(out, 'f', "generate_normal")), n, mean, stddev),
                "generate_normal");
            // all done
            return;
        },
        // the signature
        "handle"_a, "out"_a, "n"_a, "mean"_a, "stddev"_a,
        // the docstring
        "fill the first {n} cells of {out} with draws from N(mean, stddev^2), over {float32} "
        "cells; {n} must be even");

    // all done
    return;
}


// end of file
