// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// a helper that asks the kernel for the cpu count published under a given {sysctl} name
namespace pyre::extensions::host {
    // return the count reported under {name}, or zero when {sysctl} is unavailable
    static auto cpucount(const char * name) -> int
    {
        // storage for the cpu count
        int cpus = 0;

#if defined(HAVE_SYSCTL_HW_DOT)
        // the mib vector and its size
        int mib[2];
        std::size_t mib_l = sizeof(mib) / sizeof(int);
        // resolve {name} into a mib vector
        sysctlnametomib(name, mib, &mib_l);

        // storage size for the cpu count
        std::size_t cpus_l = sizeof(cpus);
        // ask the kernel to fill it in
        sysctl(mib, mib_l, &cpus, &cpus_l, 0, 0);
#endif

        // hand back what we found
        return cpus;
    }
} // namespace pyre::extensions::host


// the cpu resource counts this host reports
void
pyre::extensions::host::cpu(py::module & m)
{
    // the number of logical processors
    m.def(
        // the name
        "logical",
        // the implementation
        []() { return cpucount("hw.logicalcpu"); },
        // the docstring
        "the number of logical processors");

    // the maximum number of logical processors
    m.def(
        // the name
        "logicalMax",
        // the implementation
        []() { return cpucount("hw.logicalcpu_max"); },
        // the docstring
        "the maximum number of logical processors");

    // the number of physical processors
    m.def(
        // the name
        "physical",
        // the implementation
        []() { return cpucount("hw.physicalcpu"); },
        // the docstring
        "the number of physical processors");

    // the maximum number of physical processors
    m.def(
        // the name
        "physicalMax",
        // the implementation
        []() { return cpucount("hw.physicalcpu_max"); },
        // the docstring
        "the maximum number of physical processors");

    // all done
    return;
}


// end of file
