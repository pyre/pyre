// -*- C++ -*-
//
// bianca giovanardi
// (c) 2021 all rights reserved
//

#if !defined(pyre_algebra_Tensor_h)
#define pyre_algebra_Tensor_h

#define DEVELOP_MODE

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
    inline Tensor(const data_t &);

    // constructor with underlying data type (need this for return value optimization)
    inline Tensor(const data_t &&);

    // constructor from brace-enclosed initializer list
    template <class... T2>
    Tensor(T2...) requires(sizeof...(T2) == S);

    // copy constructor
    Tensor(const Tensor &) = default;

    // move constructor
    Tensor(Tensor &&) = default;

    // copy assignment operator
    Tensor & operator=(const Tensor &) = default;

    // move assignment operator
    Tensor & operator=(Tensor &&) = default;

    // destructor
    inline ~Tensor();

public:
    // components accessors with index
    inline const T & operator[](index_t) const;
    inline T & operator[](index_t);

    // components accessors with integers
    inline const T & operator[](int) const;
    inline T & operator[](int);

    // operator plus equal
    inline void operator+=(const Tensor<T, I...> &);

    // cast to underlying type T (enable if S = 1, i.e. scalar)
    operator T() const requires(S == 1);

    // cast to underlying data structure
    operator data_t() const;

    // reset all entries to zero
    inline void reset();

private:
    // helper function for index sequence
    template <size_t... J, class... T2>
    void _initialize(std::index_sequence<J...>, T2...);

    // helper function for index sequence
    template <size_t... J>
    void _reset(std::index_sequence<J...>);

    // helper function for index sequence
    template <size_t... J>
    void _operatorPlusEqual(std::index_sequence<J...>, const Tensor<T, I...> &);

private:
    // data
    data_t _data;

#ifdef DEVELOP_MODE
public:
    static int _constructor_calls;
    static int _destructor_calls;
#endif    // DEVELOP_MODE
};

#ifdef DEVELOP_MODE
template <typename T, int... I> 
int pyre::algebra::Tensor<T, I...>::_constructor_calls = 0;
template <typename T, int... I>
int pyre::algebra::Tensor<T, I...>::_destructor_calls = 0;
#endif    // DEVELOP_MODE

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

// helper functions for print
template <typename Arg, typename... Args>
inline std::ostream & _print(std::ostream & os, Arg && arg, Args &&... args)
{
    os << std::forward<Arg>(arg);
    ((os << ", " << std::forward<Args>(args)), ...);
    return os;
}

template <int D, typename T, std::size_t... J>
inline std::ostream & _print_vector(
    std::ostream & os, const pyre::algebra::vector_t<D, T> & vector, std::index_sequence<J...>)
{
    os << "[ ";
    if (sizeof...(J) > 0)
        _print(os, vector[J]...);
    os << " ]";
    return os;
}

template <int D1, int D2, typename T, size_t... J>
std::ostream & _print_row(
    std::ostream & os, const tensor_t<D1, D2, T> & tensor, size_t row, std::index_sequence<J...>)
{
    os << "[ ";
    if (sizeof...(J) > 0)
        _print(os, tensor[row * D2 + J]...);
    os << " ]";
    return os;
}

template <int D1, int D2, typename T, size_t... J>
std::ostream & _print_comma_row(
    std::ostream & os, const tensor_t<D1, D2, T> & tensor, size_t row, std::index_sequence<J...>)
{
    os << ",";
    return _print_row(os, tensor, row, std::make_index_sequence<D2> {});
}

template <int D1, int D2, typename T, size_t... J>
std::ostream & _print_matrix(
    std::ostream & os, const tensor_t<D1, D2, T> & tensor, std::index_sequence<J...>)
{
    os << "[ ";
    _print_row(os, tensor, 0, std::make_index_sequence<D2> {});
    ((_print_comma_row(os, tensor, J + 1, std::make_index_sequence<D2> {})), ...);
    os << " ]";
    return os;
}

// overload operator<< for vectors
template <int D, typename T>
std::ostream & operator<<(std::ostream & os, const pyre::algebra::vector_t<D, T> & vector)
{
    return _print_vector(os, vector, std::make_index_sequence<D> {});
}

// overload operator<< for second order tensors
template <int D1, int D2, typename T>
std::ostream & operator<<(std::ostream & os, const pyre::algebra::tensor_t<D1, D2, T> & tensor)
{
    return _print_matrix(os, tensor, std::make_index_sequence<D1-1> {});
}

}
}

// include the inlines
#include "Tensor.icc"
#endif

// end of file
