// -*- C -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

#if !defined(mm_portinfo_h)
#define mm_portinfo_h

// platform redirects
#if defined(MM_PLATFORM_darwin_x86_64)
#include "platforms/darwin/x86_64.h"

#elif defined(MM_PLATFORM_darwin_arm64)
#include "platforms/darwin/arm64.h"

#elif defined(MM_PLATFORM_linux_x86_64)
#include "platforms/linux/x86_64.h"

#elif defined(MM_PLATFORM_linux_ppc64le)
#include "platforms/linux/ppc64le.h"

#endif

// compiler redirects
#if defined(MM_COMPILER_gcc)
#include "compilers/gcc/gcc.h"

#elif defined(MM_COMPILER_clang)
#include "compilers/clang/clang.h"

#elif defined(MM_COMPILER_nvcc)
#include "compilers/nvcc/nvcc.h"

#endif

// all done
#endif

// end of file
