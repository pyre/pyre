// -*- C++ -*-
//
// bianca giovanardi
// (c) 2021 all rights reserved
//


#if !defined(pyre_algebra_VectorBasis_h)
#define pyre_algebra_VectorBasis_h


namespace pyre::algebra {
    template <int D, typename T = real>
    class VectorBasis {

    public:
        template<int index>
        static constexpr auto unit = vector_t<D, T>::unit(index);

    };
}


#endif

// end of file
