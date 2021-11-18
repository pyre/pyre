// -*- C++ -*-
//
// bianca giovanardi
// (c) 2021 all rights reserved
//


#if !defined(pyre_algebra_MatrixBasis_h)
#define pyre_algebra_MatrixBasis_h


namespace pyre::algebra {
    template <int D, typename T = real>
    class MatrixBasis {
      private:
        // if the index is on the diagonal, get unit matrix as diagonal matrix
        template<int index_0, int index_1>
        static constexpr diagonal_matrix_t<D, T> _getUnit() requires (index_0 == index_1);

        // if the index is not on the diagonal, get unit matrix as canonical matrix
        template<int index_0, int index_1>
        static constexpr matrix_t<D, D, T> _getUnit() requires (index_0 != index_1);

      public:
        // a unit matrix with all zeros but a one at {index_0, index_1}  
        template<int index_0, int index_1>
        static constexpr auto unit = _getUnit<index_0, index_1>();
};

}


// get the inline definitions
#define pyre_algebra_MatrixBasis_h
#include "MatrixBasis.icc"
#undef pyre_algebra_MatrixBasis_h


#endif

// end of file
