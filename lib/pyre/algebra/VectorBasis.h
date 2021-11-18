// -*- C++ -*-
//
// bianca giovanardi
// (c) 2021 all rights reserved
//

// TOFIX
#include "Tensor.h"

#if !defined(pyre_algebra_VectorBasis_h)
#define pyre_algebra_VectorBasis_h

namespace pyre { 
namespace algebra {

template <int D, typename T = real>
class VectorBasis {

public:
    template<int index>
    static constexpr auto unit = vector_t<D, T>::unit(index);

};

}
}

#endif //pyre_algebra_VectorBasis_h

// end of file
