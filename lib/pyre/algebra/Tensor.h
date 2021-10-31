// -*- C++ -*-
//
// bianca giovanardi
// (c) 2021 all rights reserved
//

#if !defined(pyre_algebra_Tensor_h)
#define pyre_algebra_Tensor_h

// TOFIX
#include "../grid.h"
#include "machine_epsilon.h"

namespace pyre { 
namespace algebra {

template <typename T, int... I>
class Tensor {

private:
    // helper function to compute the product of an arguments list
    template <typename... Args>
    static constexpr auto multiply(Args &&... args)
    {
        if constexpr (sizeof...(args))
            return  (args * ...);
        return 1;
    }
private:
    // number of indices of the tensor, i.e. rank (N = 0 for empty parameter pack, i.e. scalar)
    static constexpr int N = sizeof...(I);
    // number of total entries of the tensor (S = 1 for empty parameter pack, i.e. scalar)
    static constexpr int S = multiply(I...);

private:
    // TODO: template Tensor wrt pack_t and storage_t, just like class Grid
    // conventionally packed grid
    using pack_t = pyre::grid::canonical_t<N>;
    // of T on the heap
    using storage_t = pyre::memory::stack_t<S, T>;
    // index
    using index_t = pack_t::index_type;
    // data type
    using data_t = storage_t;

public:
    // export the underlying type
    using type = T;
    // export the number of indices
    static constexpr int dofs = N;
    // export the container size
    static constexpr int size = S;

public:
    // default constructor
    constexpr inline Tensor();

    // constructor with underlying data type
    constexpr inline Tensor(const data_t &);

    // constructor with underlying data type (need this for return value optimization)
    constexpr inline Tensor(const data_t &&);

    // constructor from brace-enclosed initializer list
    template <class... T2>
    constexpr Tensor(T2...) requires(sizeof...(T2) == S);

    // copy constructor
    constexpr Tensor(const Tensor &) = default;

    // move constructor
    constexpr Tensor(Tensor &&) = default;

    // copy assignment operator
    constexpr Tensor & operator=(const Tensor &) = default;

    // move assignment operator
    constexpr Tensor & operator=(Tensor &&) = default;

    // destructor
    constexpr inline ~Tensor();

public:
    // components accessors with index
    constexpr inline const T & operator[](index_t) const;
    constexpr inline T & operator[](index_t);

    // components accessors with integers
    constexpr inline const T & operator[](int) const;
    constexpr inline T & operator[](int);

    // operator plus equal
    constexpr inline void operator+=(const Tensor<T, I...> &);

    // cast to underlying type T (enable if S = 1, i.e. scalar)
    constexpr operator T() const requires(S == 1);

    // cast to underlying data structure
    constexpr operator data_t() const;

    // reset all entries to zero
    constexpr inline void reset();

private:
    // helper function for index sequence
    template <size_t... J, class... T2>
    constexpr void _initialize(std::index_sequence<J...>, T2...);

    // helper function for index sequence
    template <size_t... J>
    constexpr void _reset(std::index_sequence<J...>);

    // helper function for index sequence
    template <size_t... J>
    constexpr void _operatorPlusEqual(std::index_sequence<J...>, const Tensor<T, I...> &);

    // helper function to build the zero tensor
    template <size_t... J>
    static constexpr pyre::algebra::Tensor<T, I...> _make_zeros(std::index_sequence<J...>);

    // helper function to build a tensor of ones
    template <size_t... J>
    static constexpr pyre::algebra::Tensor<T, I...> _make_ones(std::index_sequence<J...>);

    // helper function to build a tensor of zeros with a 1 at index K
    template <size_t... J>
    static constexpr pyre::algebra::Tensor<T, I...> _make_basis_element(index_t K, 
        std::index_sequence<J...>);

public:
    // the zero element
    static constexpr Tensor<T, I...> zero = pyre::algebra::Tensor<T, I...>::_make_zeros(
        std::make_index_sequence<pyre::algebra::Tensor<T, I...>::size> {});

    // a tensor of ones
    static constexpr Tensor<T, I...> one = pyre::algebra::Tensor<T, I...>::_make_ones(
        std::make_index_sequence<pyre::algebra::Tensor<T, I...>::size> {});

    // the K-th unit tensor
    template<typename... Args>
    static constexpr Tensor<T, I...> unit(Args...) requires (sizeof...(Args) == N);

private:
    // layout
    static constexpr pack_t _layout {{I ...}};

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

// typedef for matrices
template <int D1, int D2 = D1, typename T = real>
using matrix_t = pyre::algebra::Tensor<T, D1, D2>;

// (dummy) typedef for symmetric matrices
// TODO: this should be a specialization of matrix_t with a symmetric pack_t
template <int D, typename T = real>
using symmetric_matrix_t = matrix_t<D, D, T>;

// (dummy) typedef for symmetric matrices
// TODO: this should be a specialization of matrix_t with a diagonal pack_t
template <int D, typename T = real>
using diagonal_matrix_t = matrix_t<D, D, T>;

// factory for unit tensors
template <int D, typename T = real, typename... Args>
static constexpr auto unit(Args... args) {
    
    // number of indices of the tensor, i.e. rank
    constexpr int N = sizeof...(args);
    
    auto _pack = []<size_t... J>(Args... args, std::index_sequence<J...>) -> auto
    {
        auto wrap = []<size_t>()->int { return D; };
        // expands to Tensor<T, D, ..., D> where D appears N times
        return Tensor<T, wrap.template operator()<J>()...>::unit(args...);
    };

    return _pack(args..., std::make_index_sequence<N> {});
}

// factory for identity matrices
template <int D, typename T = real>
static constexpr auto _make_identity_matrix() {

    diagonal_matrix_t<D, T> identity;

    auto _loop = [&identity]<size_t... I>(std::index_sequence<I...>)
    {
        ((identity[{I, I}] = 1), ... );
        return;
    };

    _loop(std::make_index_sequence<D> {});

    return identity;
}

template <int D, typename T = real>
static constexpr diagonal_matrix_t<D, T> identity_matrix = _make_identity_matrix<D, T>();

template <int D, typename T = real>
static constexpr diagonal_matrix_t<D, T> zero_matrix = diagonal_matrix_t<D, T>::zero;

template <int D, typename T = real>
static constexpr matrix_t<D, D, T> one_matrix = matrix_t<D, D, T>::one;

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
    std::ostream & os, const matrix_t<D1, D2, T> & tensor, size_t row, std::index_sequence<J...>)
{
    os << "[ ";
    if (sizeof...(J) > 0)
        _print(os, tensor[{ row, J }]...);
    os << " ]";
    return os;
}

template <int D1, int D2, typename T, size_t... J>
std::ostream & _print_comma_row(
    std::ostream & os, const matrix_t<D1, D2, T> & tensor, size_t row, std::index_sequence<J...>)
{
    os << ",";
    return _print_row(os, tensor, row, std::make_index_sequence<D2> {});
}

template <int D1, int D2, typename T, size_t... J>
std::ostream & _print_matrix(
    std::ostream & os, const matrix_t<D1, D2, T> & tensor, std::index_sequence<J...>)
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
std::ostream & operator<<(std::ostream & os, const pyre::algebra::matrix_t<D1, D2, T> & tensor)
{
    return _print_matrix(os, tensor, std::make_index_sequence<D1-1> {});
}

template <typename T>
constexpr bool is_equal(T lhs, T rhs)
{
    // QUESTION: < (>) or <= (>=)?
    if ((lhs <= rhs + epsilon(rhs)) && (lhs >= rhs - epsilon(rhs)))
    {
        return true;
    }

    return false;
}

template <typename T, int... I>
constexpr bool is_equal(const Tensor<T, I...> & lhs, const Tensor<T, I...> & rhs)
{
    // helper function (component-wise)
    constexpr auto _is_equal = []<size_t... J>(const Tensor<T, I...> & lhs, 
        const Tensor<T, I...> & rhs, std::index_sequence<J...>) {

        // if all components are equal
        if ((is_equal(lhs[J], rhs[J]) && ...)) {
            // then the tensors are equal
            return true;
        }
        // then the tensors differ
        return false;
    };

    // the size of the tensor
    constexpr int D = Tensor<T, I...>::size;
    // all done
    return _is_equal(lhs, rhs, std::make_index_sequence<D> {});
}

template <typename T, int... I>
constexpr bool is_zero(const Tensor<T, I...> & A, T tolerance)
{
    // helper function (component-wise)
    constexpr auto _is_zero = []<size_t... J>(const Tensor<T, I...> & A, 
        T tolerance, std::index_sequence<J...>) {

        // if all components are zero
        if (((A[J] <= tolerance) && ...)) {
            // then the tensor is zero
            return true;
        }
        // then the tensors is not zero
        return false;
    };

    // the size of the tensor
    constexpr int D = Tensor<T, I...>::size;
    // all done
    return _is_zero(A, tolerance, std::make_index_sequence<D> {});
}

}
}

// get the inline definitions
#define pyre_algebra_Tensor_icc
#include "Tensor.icc"
#undef pyre_algebra_Tensor_icc

#endif

// end of file
