// -*- c++ -*-
//
// bianca giovanardi
// (c) 1998-2023 all rights reserved


// code guard
#if !defined(pyre_tensor_utilities_h)
#define pyre_tensor_utilities_h


namespace pyre::tensor {

    // helper functions for print
    template <typename Arg, typename... Args>
    inline std::ostream & _print(std::ostream & os, Arg && arg, Args &&... args)
    {
        os << std::forward<Arg>(arg);
        ((os << ", " << std::forward<Args>(args)), ...);
        return os;
    }

    template <int D, typename T, int... J>
    inline std::ostream & _print_vector(
        std::ostream & os, const pyre::tensor::vector_t<D, T> & vector, integer_sequence<J...>)
    {
        os << "[ ";
        if (sizeof...(J) > 0)
            _print(os, vector[J]...);
        os << " ]";
        return os;
    }

    template <int D1, int D2, typename T, class packingT, int... J>
    std::ostream & _print_row(
        std::ostream & os, const matrix_t<D1, D2, T, packingT> & tensor, int row,
        integer_sequence<J...>)
    {
        os << "[ ";
        if (sizeof...(J) > 0)
            _print(os, tensor[{ row, J }]...);
        os << " ]";
        return os;
    }

    template <int D1, int D2, typename T, class packingT, int... J>
    std::ostream & _print_comma_row(
        std::ostream & os, const matrix_t<D1, D2, T, packingT> & tensor, int row,
        integer_sequence<J...>)
    {
        os << ",";
        return _print_row(os, tensor, row, make_integer_sequence<D2> {});
    }

    template <int D1, int D2, typename T, class packingT, int... J>
    std::ostream & _print_matrix(
        std::ostream & os, const matrix_t<D1, D2, T, packingT> & tensor, integer_sequence<J...>)
    {
        os << "[ ";
        _print_row(os, tensor, 0, make_integer_sequence<D2> {});
        ((_print_comma_row(os, tensor, J + 1, make_integer_sequence<D2> {})), ...);
        os << " ]";
        return os;
    }

    // overload operator<< for vectors
    template <int D, typename T>
    std::ostream & operator<<(std::ostream & os, const pyre::tensor::vector_t<D, T> & vector)
    {
        return _print_vector(os, vector, make_integer_sequence<D> {});
    }

    // overload operator<< for second order tensors
    template <int D1, int D2, typename T, class packingT>
    std::ostream & operator<<(
        std::ostream & os, const pyre::tensor::matrix_t<D1, D2, T, packingT> & tensor)
    {
        return _print_matrix(os, tensor, make_integer_sequence<D1 - 1> {});
    }

    template <typename T>
    constexpr bool is_equal(T lhs, T rhs)
    {
        if ((lhs < rhs + epsilon_right(rhs)) && (lhs > rhs - epsilon_left(rhs))) {
            return true;
        }

        return false;
    }

    template <typename T, class packingT, int... I>
    constexpr bool is_equal(
        const Tensor<T, packingT, I...> & lhs, const Tensor<T, packingT, I...> & rhs)
    {
        // helper function (component-wise)
        constexpr auto _is_equal = []<int... J>(
            const Tensor<T, packingT, I...> & lhs, const Tensor<T, packingT, I...> & rhs,
            integer_sequence<J...>)
        {
            // if all components are equal
            if ((is_equal(lhs[J], rhs[J]) && ...)) {
                // then the tensors are equal
                return true;
            }
            // then the tensors differ
            return false;
        };

        // the size of the tensor
        constexpr int D = Tensor<T, packingT, I...>::size;
        // all done
        return _is_equal(lhs, rhs, make_integer_sequence<D> {});
    }

    template <typename T, class packingT, int... I>
    constexpr bool is_zero(const Tensor<T, packingT, I...> & A, T tolerance)
    {
        // helper function (component-wise)
        constexpr auto _is_zero =
            []<int... J>(const Tensor<T, packingT, I...> & A, T tolerance, integer_sequence<J...>)
        {
            // if all components are zero
            if (((A[J] <= tolerance) && ...)) {
                // then the tensor is zero
                return true;
            }
            // then the tensors is not zero
            return false;
        };

        // the size of the tensor
        constexpr int D = Tensor<T, packingT, I...>::size;
        // all done
        return _is_zero(A, tolerance, make_integer_sequence<D> {});
    }

    // helper function (compare J-th component)
    template <int J, typename T, class packingT, int... I>
    constexpr auto is_less(
        const Tensor<T, packingT, I...> & lhs, const Tensor<T, packingT, I...> & rhs) -> bool
        requires(J < Tensor<T, packingT, I...>::size)
    {
        // if the J-th component of {lhs} is less than J-th component of {rhs}
        if ((lhs[J] < rhs[J])) {
            // then {lhs} is less than {rhs}
            return true;
        }
        // if the J-th component of {lhs} is greater than J-th component of {rhs}
        if (lhs[J] != rhs[J]) {
            // then {lhs} is not less than {rhs}
            return false;
        }
        // if the J-th component of {lhs} is equal to J-th component of {rhs},
        // then compare the next component
        return is_less<J + 1>(lhs, rhs);
    }

    // helper function (compare J-th component)
    template <int J, typename T, class packingT, int... I>
    constexpr auto is_less(
        const Tensor<T, packingT, I...> & lhs, const Tensor<T, packingT, I...> & rhs) -> bool
        requires(J == Tensor<T, packingT, I...>::size)
    {
        // base case for recursion: all components are equal
        return false;
    }

    template <typename T, class packingT, int... I>
    inline bool operator<(
        const Tensor<T, packingT, I...> & lhs, const Tensor<T, packingT, I...> & rhs)
    {
        // recursively compare all components starting from component 0
        return is_less<0>(lhs, rhs);
    }

} // namespace pyre::tensor


#endif

// end of file
