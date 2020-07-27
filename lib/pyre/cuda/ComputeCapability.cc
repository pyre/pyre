// -*- C++ -*-
// -*- coding: utf-8 -*-
//

// my parts
#include "ComputeCapability.h"

pyre::cuda::ComputeCapability::
operator std::string() const
{
    return std::to_string(major) + "." + std::to_string(minor);
}

std::ostream &
pyre::cuda::
operator<<(std::ostream & os, pyre::cuda::ComputeCapability compute)
{
    return os << std::string(compute);
}

// end of file
