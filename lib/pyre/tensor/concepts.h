// -*- c++ -*-
//
// bianca giovanardi
// (c) 1998-2024 all rights reserved


// code guard
#if !defined(pyre_tensor_concepts_h)
#define pyre_tensor_concepts_h


// set up the namespace
namespace pyre::tensor {

    // concept of a tensor
    template <class F>
    concept tensor_c = requires(F c) {
        // require that F only binds to {Tensor} specializations
        []<typename T, class packingT, int... I>(const Tensor<T, packingT, I...> &) {
        }(c);
    };

    // concept of a matrix
    template <class F>
    concept matrix_c = requires(F c) {
        // require that F only binds to {matrix_t} specializations
        []<int D1, int D2, typename T, class packingT>(const matrix_t<D1, D2, T, packingT> &)
            // with D1 and D2 different than 1 (otherwise it is a vector)
            requires(D1 != 1 && D2 != 1)
        {}
        (c);
    };

    // concept of a square matrix
    template <class F>
    concept square_matrix_c = requires(F c) {
        // require that F only binds to square {matrix_t} specializations
        []<int D, typename T, class packingT>(const matrix_t<D, D, T, packingT> &)
            // with D different than 1 (otherwise it is a scalar)
            requires(D != 1)
        {}
        (c);
    };

    // concept of a diagonal matrix
    template <class F>
    concept diagonal_matrix_c = requires(F c) {
        // require that F only binds to square {matrix_t} specializations
        []<int D, typename T>(const matrix_t<D, D, T, pyre::grid::diagonal_t<D>> &)
            // with D different than 1 (otherwise it is a scalar)
            requires(D != 1)
        {}
        (c);
    };

    // concept of a vector
    template <class F>
    concept vector_c = requires(F c) {
        // require that F only binds to {matrix_t} specializations
        []<int D1, int D2, typename T, class packingT>(const matrix_t<D1, D2, T, packingT> &)
            // with either D1 or D2 equal to 1 (but not both)
            requires(!(D1 == 1) != !(D2 == 1))
        {}
        (c);
    } or requires(F c) {
        // require that F only binds to {vector_t} specializations
        []<int D, typename T, class packingT>(const vector_t<D, T, packingT> &)
            requires(D != 1)
        {}
        (c);
    };

} // namespace pyre::tensor


#endif

// end of file
