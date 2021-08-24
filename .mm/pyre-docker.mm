# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# docker images
pyre.docker-images := \
    pyre.focal-gcc.dev pyre.focal-clang.dev \
    pyre.groovy-gcc.dev pyre.groovy-clang.dev pyre.groovy-cuda.dev \
    pyre.hirsute-gcc.dev pyre.hirsute-clang.dev pyre.hirsute-gcc-cmake.dev
    pyre.focal-gcc.test pyre.focal-clang.test \
    pyre.groovy-gcc.test pyre.groovy-clang.test pyre.groovy-cuda.test \
    pyre.hirsute-gcc.test pyre.hirsute-clang.test pyre.hirsute-gcc-cmake.test


# the docker dev images
# focal
pyre.focal-gcc.dev.name := focal-gcc
pyre.focal-gcc.dev.mounts := mm pyre
pyre.focal-clang.dev.name := focal-clang
pyre.focal-clang.dev.mounts := mm pyre
# groovy
pyre.groovy-gcc.dev.name := groovy-gcc
pyre.groovy-gcc.dev.mounts := mm pyre
pyre.groovy-clang.dev.name := groovy-clang
pyre.groovy-clang.dev.mounts := mm pyre
pyre.groovy-cuda.dev.name := groovy-cuda
pyre.groovy-cuda.dev.mounts := mm pyre
# hirsute
pyre.hirsute-gcc.dev.name := hirsute-gcc
pyre.hirsute-gcc.dev.mounts := mm pyre
pyre.hirsute-clang.dev.name := hirsute-clang
pyre.hirsute-clang.dev.mounts := mm pyre
pyre.hirsute-gcc-cmake.dev.name := hirsute-gcc-cmake
pyre.hirsute-gcc-cmake.dev.mounts := mm pyre

# the docker test images
# focal
pyre.focal-gcc.test.name := focal-gcc
pyre.focal-clang.test.name := focal-clang
# groovy
pyre.groovy-gcc.test.name := groovy-gcc
pyre.groovy-clang.test.name := groovy-clang
pyre.groovy-cuda.test.name := groovy-cuda
# hirsute
pyre.hirsute-gcc.test.name := hirsute-gcc
pyre.hirsute-clang.test.name := hirsute-clang
pyre.hirsute-gcc-cmake.test.name := hirsute-gcc-cmake


# end of file
