// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// {project.authors}
// (c) {project.span} all rights reserved

// my declarations
#include "version.h"

// build and return the version tuple
auto
{project.name}::version::version() -> version_t
{{
    // easy enough
    return version_t {{ major, minor, micro, revision }};
}}

// end of file
