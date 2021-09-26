// -*- C++ -*-
//
// bianca giovanardi
// (c) 2021 all rights reserved
//

#if !defined(pyre_algebra_Tensor_h)
#define pyre_algebra_Tensor_h

// TOFIX
#include "../grid.h"

namespace pyre { 
namespace algebra {

template <typename T, int... I>
class Tensor {
private:
    // number of indices of the tensor (N = 0 for empty parameter pack, i.e. scalar)
    static constexpr int N = sizeof...(I);
    // number of total entries of the tensor (S = 1 for empty parameter pack, i.e. scalar)
    static constexpr int S = (I * ...);

private:
    // QUESTION: should Tensor be templated wrt pack_t and storage_t?  
    // conventionally packed grid
    using pack_t = pyre::grid::canonical_t<N>;
    // of T on the heap
    using storage_t = pyre::memory::stack_t<S, T>;
    // putting it all together
    using grid_t = pyre::grid::grid_t<pack_t, storage_t>;
    // index
    using index_t = pack_t::index_type;
    // data_type
    using data_t = grid_t;

public:
    // export the underlying type
    using type = T;
    // export the number of indices
    static constexpr int dofs = N;
    // export the container size
    static constexpr int size = S;

public:
    // default constructor
    inline Tensor();

    // constructor with underlying data type
    inline Tensor(const data_t & data);

    // constructor with underlying data type (need this for return value optimization)
    inline Tensor(const data_t && data);

    // constructor from brace-enclosed initializer list
    template <class... T2>
    Tensor(T2... args) requires(sizeof...(T2) == S);

    // copy constructor
    Tensor(const Tensor &) = default;

    // move constructor
    Tensor(Tensor &&) = default;

    // copy assignment operator
    Tensor & operator=(const Tensor &) = default;

    // move assignment operator
    Tensor & operator=(Tensor && rhs) = default;

    // destructor
    inline ~Tensor();

public:
    // components accessors with index
    inline const T & operator[](index_t i) const;
    inline T & operator[](index_t i);

    // components accessors with integers
    inline const T & operator[](int i) const;
    inline T & operator[](int i);

    // operator plus equal
    inline void operator+=(const Tensor<T, I...> & rhs);

    // cast to underlying type T (enable if S = 1, i.e. scalar)
    operator T() const requires(S == 1);

    // cast to underlying data structure
    operator data_t() const;

    // reset all entries to zero
    inline void reset();

private:
    // helper function for index sequence
    template <size_t... J, class... T2>
    void _initialize(std::index_sequence<J...>, T2... args);

    // helper function for index sequence
    template <size_t... J>
    void _reset(std::index_sequence<J...>);

    // helper function for index sequence
    template <size_t... J>
    void _operatorPlusEqual(std::index_sequence<J...>, const Tensor<T, I...> & rhs);

private:
    // data
    data_t _data;
};

// typedef for real values
using real = double;

// typedef for scalars
using scalar_t = real;

// typedef for vectors
template <int D, typename T = real>
using vector_t = pyre::algebra::Tensor<T, D>;

// typedef for tensors
template <int D1, int D2 = D1, typename T = real>
using tensor_t = pyre::algebra::Tensor<T, D1, D2>;

}
}

// include the inlines
#include "Tensor.icc"
#endif

// end of file
