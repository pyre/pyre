// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2023 all rights reserved
//


#if !defined(pyre_tensor_tensor_algebra_h)
#define pyre_tensor_tensor_algebra_h


namespace pyre::tensor {

    // compute 2-norm of tensor
    template <typename T, class packingT, int... I>
    constexpr auto norm(const Tensor<T, packingT, I...> & tensor) -> T
    {
        using tensor_t = Tensor<T, packingT, I...>;

        // helper function
        constexpr auto _norm_square = []<int... J>(const tensor_t & tensor, integer_sequence<J...>) 
            -> T
        {
            // return sum of all square components
            return ((tensor[J] * tensor[J]) + ...);
        };

        // return 
        constexpr int D = tensor_t::size;
        return std::sqrt(_norm_square(tensor, make_integer_sequence<D> {}));
    }

    // normalize a tensor with its 2-norm
    template <typename T, class packingT, int... I>
    constexpr auto normalize(const Tensor<T, packingT, I...> & tensor) 
        -> Tensor<T, packingT, I...>
    {
        return tensor / norm(tensor);
    }

    // tensors operator==
    template <typename T, class packingT1, class packingT2, int... I>
    constexpr auto operator==(const Tensor<T, packingT1, I...> & lhs, 
        const Tensor<T, packingT2, I...> & rhs) -> bool
    {
        // the repacking type
        using repacking_t = typename repacking<packingT1, packingT2>::packing_type;
        // the repacked tensor type
        using repacked_tensor_t = Tensor<T, repacking_t, I...>;
        // the number of components of the repacked tensor
        constexpr int D = repacked_tensor_t::size;
        // the type of tensor {lhs}
        using tensor1_t = Tensor<T, packingT1, I...>;
        // the type of tensor {rhs}
        using tensor2_t = Tensor<T, packingT2, I...>;
           
        // helper function to perform component-by-component comparison
        constexpr auto _component_wise_comparison = []<int... J>
        (const auto & lhs, const auto & rhs, integer_sequence<J...>) -> bool
        {
            // helper function to sum of component K (enumeration relative to the repacking)
            constexpr auto _component_equal = []<int K>(const auto & lhs, const auto & rhs)
                -> bool
            {
                // get the index corresponding to the offset K in the repacking
                constexpr auto index = repacked_tensor_t::layout().index(K);
                // map the index into the offset for the packing of y1 
                constexpr auto K1 = tensor1_t::layout().offset(index);
                // map the index into the offset for the packing of y2 
                constexpr auto K2 = tensor2_t::layout().offset(index);
                // all done
                return lhs[K1] == rhs[K2];
            };

            // return component-wise comparison
            return (((_component_equal.template operator()<J>(lhs, rhs)) && ...));
        };

        // perform component-by-component comparison
        return _component_wise_comparison(lhs, rhs, make_integer_sequence<D> {});
    }

    namespace {
        // tensor times scalar (implementation)
        template <typename T2, typename T, class packingT, int... I, int... J>
        constexpr void _tensor_times_scalar(T2 a, const Tensor<T, packingT, I...> & y, 
            Tensor<T, packingT, I...> & result, integer_sequence<J...>) 
            requires (std::convertible_to<T2, T>)
        {
            ((result[J] = y[J] * a), ...);
            return;
        }
    }

    // scalar times tensor
    template <typename T2, typename T, class packingT, int... I>
    constexpr auto operator*(T2 a, const Tensor<T, packingT, I...> & y)
        -> Tensor<T, packingT, I...>
        requires(Tensor<T, packingT, I...>::size != 1 && std::convertible_to<T2, T>)
    {
        // instantiate the result
        Tensor<T, packingT, I...> result;
        constexpr int D = Tensor<T, packingT, I...>::size;
        _tensor_times_scalar(a, y, result, make_integer_sequence<D> {});
        return result;
    }

    // tensor times scalar
    template <typename T2, typename T, class packingT, int... I>
    constexpr auto operator*(const Tensor<T, packingT, I...> & y, T2 a)
        -> Tensor<T, packingT, I...>
        requires(Tensor<T, packingT, I...>::size != 1 && std::convertible_to<T2, T>)
    {
        return a * y;
    }

    // scalar times (temporary) tensor
    template <typename T2, typename T, class packingT, int... I>
    constexpr auto operator*(T2 a, Tensor<T, packingT, I...> && y)
        -> Tensor<T, packingT, I...>
        requires(Tensor<T, packingT, I...>::size != 1 && std::convertible_to<T2, T>)
    {
        constexpr int D = Tensor<T, packingT, I...>::size;
        _tensor_times_scalar(a, y, y, make_integer_sequence<D> {});
        return y;
    }

    // (temporary) tensor times scalar 
    template <typename T2, typename T, class packingT, int... I>
    constexpr auto operator*(Tensor<T, packingT, I...> && y, T2 a)
        -> Tensor<T, packingT, I...>
        requires(Tensor<T, packingT, I...>::size != 1 && std::convertible_to<T2, T>)
    {
        return a * std::move(y);
    }

    namespace
    {
        // tensor plus tensor (implementation)
        template <typename T, class packingT1, class packingT2, int... I>
        constexpr auto _tensor_sum(
            const Tensor<T, packingT1, I...> & y1, 
            const Tensor<T, packingT2, I...> & y2, 
            Tensor<T, typename repacking<packingT1, packingT2>::packing_type, I...> & result)
            -> Tensor<T, typename repacking<packingT1, packingT2>::packing_type, I...>
        {
            // the repacking type
            using repacking_t = typename repacking<packingT1, packingT2>::packing_type;
            // the repacked tensor type
            using repacked_tensor_t = Tensor<T, repacking_t, I...>;
            // the number of components of the repacked tensor
            constexpr int D = repacked_tensor_t::size;
            // the type of tensor y1
            using tensor1_t = Tensor<T, packingT1, I...>;
            // the type of tensor y2
            using tensor2_t = Tensor<T, packingT2, I...>;

            // helper function to perform component-by-component sum
            constexpr auto _component_wise_sums = []<int... J>
            (const auto & y1, const auto & y2, auto & result, integer_sequence<J...>)
            {
                // helper function to sum of component K (enumeration relative to the repacking)
                constexpr auto _component_sum = []<int K>(const auto & y1, const auto & y2, 
                    auto & result)
                {
                    // get the index corresponding to the offset K in the repacking
                    constexpr auto index = repacked_tensor_t::layout().index(K);
                    // map the index into the offset for the packing of y1 
                    constexpr auto K1 = tensor1_t::layout().offset(index);
                    // map the index into the offset for the packing of y2 
                    constexpr auto K2 = tensor2_t::layout().offset(index);

                    // perform the sum of the corresponding entries
                    result[K] = y1[K1] + y2[K2];

                    // all done
                    return;
                };

                // sum over each component J = 0, ..., size of repacking
                ((_component_sum.template operator()<J>(y1, y2, result)), ...);

                // all done
                return;
            };

            // perform component-by-component sum
            _component_wise_sums(y1, y2, result, make_integer_sequence<D> {});

            // all done
            return result;
        }
    }

    // tensor plus tensor
    template <typename T, class packingT1, class packingT2, int... I>
    constexpr auto operator+(const Tensor<T, packingT1, I...> & y1, 
        const Tensor<T, packingT2, I...> & y2) 
        -> Tensor<T, typename repacking<packingT1, packingT2>::packing_type, I...>
    {
        // the repacking type
        using repacking_t = typename repacking<packingT1, packingT2>::packing_type;
        // typedef for the repacked tensor based on {packingT1} and {packingT2}
        using repacked_tensor_t = Tensor<T, repacking_t, I...>;
        // instantiate the result
        repacked_tensor_t result;

        // compute component-wise summation
        return _tensor_sum(y1, y2, result);
    }

    // tensor plus (temporary) tensor
    template <typename T, class packingT1, class packingT2, int... I>
    constexpr auto operator+(const Tensor<T, packingT1, I...> & y1, 
        Tensor<T, packingT2, I...> && y2) -> Tensor<T, packingT2, I...>
        requires (std::is_same_v<typename repacking<packingT1, packingT2>::packing_type, packingT2>)
    {
        // compute component-wise summation and write the result on y2
        return _tensor_sum(y1, y2, y2);
    }

    // (temporary) tensor plus tensor
    template <typename T, class packingT1, class packingT2, int... I>
    constexpr auto operator+(Tensor<T, packingT1, I...> && y1, 
        const Tensor<T, packingT2, I...> & y2)
        -> auto
    {
        // easy enough
        return y2 + std::move(y1);
    }

    // (temporary) tensor plus (temporary) tensor
    template <typename T, class packingT1, class packingT2, int... I>
    constexpr auto operator+(Tensor<T, packingT1, I...> && y1, Tensor<T, packingT2, I...> && y2)
        -> auto
    {
        // typedef for the repacked tensor based on {packingT1} and {packingT2}
        using repacking_t = typename repacking<packingT1, packingT2>::packing_type;
        // if the repacking type is the packing type of y1
        if constexpr(std::is_same_v<repacking_t, packingT1>) {
            // pass down y1 as temporary and y2 as const reference 
            return std::move(y1) + std::as_const(y2);
        }
        else {
            // pass down y2 as temporary and y1 as const reference 
            return std::move(y2) + std::as_const(y1);
        }        
    }

    // (unary) minus tensor
    template <typename T, class packingT, int... I>
    constexpr auto operator-(const Tensor<T, packingT, I...> & y) -> Tensor<T, packingT, I...>
    {
        // typedef the tensor
        using tensor_t = Tensor<T, packingT, I...>;
        // get the tensor size (number of components)
        constexpr int D = tensor_t::size;

        // helper function to do component-wise operation
        constexpr auto _operator_minus = []<int... J>(const tensor_t & tensor, 
            integer_sequence<J...>) -> tensor_t
        {
            // return sum of all square components
            return tensor_t {-tensor[J] ...};
        };

        // return the result of the component-wise operation
        return _operator_minus(y, make_integer_sequence<D> {});
    }

    // (unary) minus (temporary) tensor
    template <typename T, class packingT, int... I>
    constexpr auto operator-(Tensor<T, packingT, I...> && y) -> auto
    {
        // write the result on the temporary
        y = -std::as_const(y);
        // all done
        return y;
    }  

    // tensor minus tensor
    template <typename T, class packingT1, class packingT2, int... I>
    constexpr auto operator-(const Tensor<T, packingT1, I...> & y1, 
        const Tensor<T, packingT2, I...> & y2) -> auto
    {
        // std::cout << "operator- & &" << std::endl;
        return y1 + (-y2);
    }

    // (temporary) tensor minus tensor
    template <typename T, class packingT1, class packingT2, int... I>
    constexpr auto operator-(Tensor<T, packingT1, I...> && y1, 
        const Tensor<T, packingT2, I...> & y2) -> auto
    {
        // std::cout << "operator- && &" << std::endl;
        return std::move(y1) + (-y2);
    }

    // tensor minus (temporary) tensor
    template <typename T, class packingT1, class packingT2, int... I>
    constexpr auto operator-(const Tensor<T, packingT1, I...> & y1, 
        Tensor<T, packingT2, I...> && y2) -> auto
    {
        // std::cout << "operator- & &&" << std::endl;
        return y1 + (-std::move(y2));
    }

    // (temporary) tensor minus (temporary) tensor
    template <typename T, class packingT1, class packingT2, int... I>
    constexpr auto operator-(Tensor<T, packingT1, I...> && y1, Tensor<T, packingT2, I...> && y2)
        -> auto
    {
        // std::cout << "operator- && &&" << std::endl;
        return std::move(y1) + std::move(-std::move(y2));
    }

    // tensor plus equal tensor
    template <typename T, class packingT1, int... I, class TENSOR>
    constexpr auto operator+=(Tensor<T, packingT1, I...> & lhs, 
        TENSOR && rhs) -> Tensor<T, packingT1, I...> & 
    {
        lhs = std::move(lhs) + std::forward<TENSOR>(rhs);
        return lhs;
    }

    // tensor minus equal tensor
    template <typename T, class packingT1, int... I, class TENSOR>
    constexpr auto operator-=(Tensor<T, packingT1, I...> & lhs, TENSOR && rhs)
    -> Tensor<T, packingT1, I...> &
    {
        lhs = std::move(lhs) - std::forward<TENSOR>(rhs);
        return lhs;
    }

    // tensor divided scalar
    template <typename T2, typename T, class packingT, int... I>
    constexpr auto operator/(const Tensor<T, packingT, I...> & y, T2 a) -> Tensor<T, packingT, I...>
    requires(Tensor<T, packingT, I...>::size != 1 && std::convertible_to<T2, T>)
    {
        return (1.0 / a) * y;
    }

    // (temporary) tensor divided scalar
    template <typename T2, typename T, class packingT, int... I>
    constexpr auto operator/(Tensor<T, packingT, I...> && y, T2 a) -> Tensor<T, packingT, I...>
    requires(Tensor<T, packingT, I...>::size != 1 && std::convertible_to<T2, T>)
    {
        return (1.0 / a) * std::move(y);
    }

    // builds a square matrix with all zeros except the K-th row is equal to v
    template <int K, int D, typename T, class packingT>
    constexpr auto matrix_row(const vector_t<D, T> & v) -> matrix_t<D, D, T, packingT>
    {
        constexpr auto _fill_matrix_row = []<int... I>(
            matrix_t<D, D, T, packingT> & A, const vector_t<D, T> & v, integer_sequence<I...>) 
            -> matrix_t<D, D, T, packingT>
        {
            ((A[{K, I}] = v[{ I }]), ...);
            return A;
        };
        // fill row K of a zero matrix with vector v
        return _fill_matrix_row(matrix_t<D, D, T, packingT>::zero, v, 
            make_integer_sequence<D> {});
    }

    // builds a square matrix with all zeros except the K-th column is equal to v
    template <int K, int D, typename T>
    constexpr auto matrix_column(const vector_t<D, T> & v) -> matrix_t<D, D, T>
    {
        constexpr auto _fill_matrix_column = []<int... I>(
            matrix_t<D, D, T> A, const vector_t<D, T> & v, integer_sequence<I...>) 
            -> matrix_t<D, D, T>
        {
            ((A[{I, K}] = v[{ I }]), ...);
            return A;
        };
        // fill column K of a zero matrix with vector v
        return _fill_matrix_column(matrix_t<D, D, T>::zero, v, make_integer_sequence<D> {});
    }

    // builds a square matrix with all zeros except the diagonal is equal to v
    template <int D, typename T>
    constexpr auto matrix_diagonal(const vector_t<D, T> & v) -> diagonal_matrix_t<D, T>
    {
        constexpr auto _fill_matrix_diagonal = []<int... I>(
            diagonal_matrix_t<D, T> A, const vector_t<D, T> & v, integer_sequence<I...>) 
            -> diagonal_matrix_t<D, T>
        {
            ((A[{I, I}] = v[{ I }]), ...);
            return A;
        };
        // instantiate a diagonal matrix
        diagonal_matrix_t<D, T> A;
        // fill diagonal of a zero matrix with vector v
        return _fill_matrix_diagonal(A, v, make_integer_sequence<D> {});
    }

    // builds the vector with the diagonal entries of a matrix
    template <int D, typename T, class packingT>
    constexpr auto matrix_diagonal(const matrix_t<D, D, T, packingT> & A) -> vector_t<D, T>
    {
        auto _fill_vector_with_matrix_diagonal = [&A]<int... J>(integer_sequence<J...>) 
            -> vector_t<D, T>
        {
            auto wrap = [&A]<int K>()->T { return  A[{K, K}]; };
            return vector_t<D, T>(wrap.template operator()<J>()...);
        };
        // fill a vector with the diagonal of A and return it
        return _fill_vector_with_matrix_diagonal(make_integer_sequence<D> {});
    }

    // row-column vector product
    template <int D, typename T>
    constexpr auto operator*(const vector_t<D, T> & v1, const vector_t<D, T> & v2) -> T
    {
        // helper function (scalar product)
        constexpr auto _vector_times_vector = []<int... K>(
            const vector_t<D, T> & v1, const vector_t<D, T> & v2, 
            integer_sequence<K...>) ->T 
        { 
            return ((v1[{ K }] * v2[{ K }]) + ...);
        };
        return _vector_times_vector(v1, v2, make_integer_sequence<D> {});
    }

    // matrix-vector multiplication
    template <int D1, int D2, typename T, class packingT>
    constexpr auto operator*(const matrix_t<D1, D2, T, packingT> & A, const vector_t<D2, T> & v)
    -> vector_t<D1, T>
    {
        // helper function
        constexpr auto _matrix_times_vector = []<int... K>(
            const matrix_t<D1, D2, T, packingT> & A, const vector_t<D2, T> & v, 
            integer_sequence<K...>) -> vector_t<D1, T> 
        { 
            return vector_t<D1, T>((row<K>(A) * v)...);
        };
        return _matrix_times_vector(A, v, make_integer_sequence<D2> {});
    }

    // vector-matrix multiplication
    template <int D1, int D2, typename T, class packingT>
    constexpr auto operator*(const vector_t<D2, T> & v, const matrix_t<D1, D2, T, packingT> & A)
    -> vector_t<D1, T>
    {
        return transpose(A) * v;
    }

    // matrix-matrix multiplication
    template <int D1, int D2, int D3, typename T, class packingT1, class packingT2>
    constexpr auto operator*(const matrix_t<D1, D2, T, packingT1> & A1, 
        const matrix_t<D2, D3, T, packingT2> & A2) -> matrix_t<D1, D3, T>
    requires(D1 != 1 && D2 != 1 && D3 != 1)
    {
        // helper function
        constexpr auto _matrix_times_matrix = []<int... K>(
            const matrix_t<D1, D2, T, packingT1> & A1, 
            const matrix_t<D2, D3, T, packingT2> & A2, 
            integer_sequence<K...>) -> matrix_t<D1, D3, T> 
        {
            // for each K build the matrix whose column K is equal to A1 * col<K>(A2)
            // then add them all up
            return (matrix_column<K>(A1 * col<K>(A2)) + ...);
        };
        return _matrix_times_matrix(A1, A2, make_integer_sequence<D3> {});
    }

    // Tensor operator*=
    template <typename T, class packingT1, int... I, class TENSOR>
    constexpr auto operator*=(Tensor<T, packingT1, I...> & lhs, TENSOR && rhs)
    -> Tensor<T, packingT1, I...> &
    {
        lhs = std::move(lhs) * std::forward<TENSOR>(rhs);
        return lhs;
    }

    // Tensor operator/=
    template <typename T, class packingT1, int... I, class SCALAR>
    constexpr auto operator/=(Tensor<T, packingT1, I...> & lhs, SCALAR && rhs)
    -> Tensor<T, packingT1, I...> &
    {
        lhs = std::move(lhs) / std::forward<SCALAR>(rhs);
        return lhs;
    }

    // the skew symmetric matrix representing vector a  
    template <typename T>
    constexpr auto skew(const vector_t<3, T> & a) -> matrix_t<3, 3, T>
    {
        matrix_t<3, 3, T> A = matrix_t<3, 3, T>::zero;
        A[{0, 1}] = -a[2];
        A[{0, 2}] = a[1];
        A[{1, 0}] = a[2];
        A[{1, 2}] = -a[0];
        A[{2, 0}] = -a[1];
        A[{2, 1}] = a[0];
        return A;
    }

    template <typename T>
    constexpr auto cross(const vector_t<3, T> & a, const vector_t<3, T> & b) -> auto
    {
        return skew(a) * b;
    }

    template <typename T>
    constexpr auto cross(const vector_t<2, T> & a, const vector_t<2, T> & b) -> T
    {
        vector_t<3, T> a3 {a[0], a[1], 0.0};
        vector_t<3, T> b3 {b[0], b[1], 0.0};
        return cross(a3, b3)[2];
    }

    // factorial
    template <int D>
    constexpr auto factorial() -> int
    {
        return D * factorial<int(D - 1)>();
    }

    template <>
    constexpr auto factorial<1>() -> int
    {
        return 1;
    }

    template <typename T, class packingT>
    constexpr auto determinant(const matrix_t<4, 4, T, packingT> & A) -> T
    {
        return A[{0, 1}] * A[{2, 3}] * A[{3, 2}] * A[{1, 0}] - A[{0, 1}] * A[{2, 2}] * A[{3, 3}]
                 * A[{1, 0}]
             - A[{2, 3}] * A[{3, 1}] * A[{0, 2}] * A[{1, 0}] + A[{2, 2}] * A[{3, 1}] * A[{0, 3}]
                 * A[{1, 0}]
             - A[{0, 0}] * A[{2, 3}] * A[{3, 2}] * A[{1, 1}] + A[{0, 0}] * A[{2, 2}] * A[{3, 3}]
                 * A[{1, 1}]
             + A[{2, 3}] * A[{3, 0}] * A[{0, 2}] * A[{1, 1}] - A[{2, 2}] * A[{3, 0}] * A[{0, 3}]
                 * A[{1, 1}]
             - A[{0, 1}] * A[{2, 3}] * A[{3, 0}] * A[{1, 2}] + A[{0, 0}] * A[{2, 3}] * A[{3, 1}]
                 * A[{1, 2}]
             + A[{0, 1}] * A[{2, 2}] * A[{3, 0}] * A[{1, 3}] - A[{0, 0}] * A[{2, 2}] * A[{3, 1}]
                 * A[{1, 3}]
             - A[{3, 3}] * A[{0, 2}] * A[{1, 1}] * A[{2, 0}] + A[{3, 2}] * A[{0, 3}] * A[{1, 1}]
                 * A[{2, 0}]
             + A[{0, 1}] * A[{3, 3}] * A[{1, 2}] * A[{2, 0}] - A[{3, 1}] * A[{0, 3}] * A[{1, 2}]
                 * A[{2, 0}]
             - A[{0, 1}] * A[{3, 2}] * A[{1, 3}] * A[{2, 0}] + A[{3, 1}] * A[{0, 2}] * A[{1, 3}]
                 * A[{2, 0}]
             + A[{3, 3}] * A[{0, 2}] * A[{1, 0}] * A[{2, 1}] - A[{3, 2}] * A[{0, 3}] * A[{1, 0}]
                 * A[{2, 1}]
             - A[{0, 0}] * A[{3, 3}] * A[{1, 2}] * A[{2, 1}] + A[{3, 0}] * A[{0, 3}] * A[{1, 2}]
                 * A[{2, 1}]
             + A[{0, 0}] * A[{3, 2}] * A[{1, 3}] * A[{2, 1}] - A[{3, 0}] * A[{0, 2}] * A[{1, 3}]
                 * A[{2, 1}];
    }

    template <typename T, class packingT>
    constexpr auto determinant(const matrix_t<3, 3, T, packingT> & A) -> T
    {
        return A[{0, 0}] * (A[{1, 1}] * A[{2, 2}] - A[{1, 2}] * A[{2, 1}]) 
             - A[{0, 1}] * (A[{1, 0}] * A[{2, 2}] - A[{1, 2}] * A[{2, 0}])
             + A[{0, 2}] * (A[{1, 0}] * A[{2, 1}] - A[{1, 1}] * A[{2, 0}]);
    }

    template <typename T, class packingT>
    constexpr auto determinant(const matrix_t<2, 2, T, packingT> & A) -> T
    {
        return A[{0, 0}] * A[{1, 1}] - A[{0, 1}] * A[{1, 0}];
    }

    template <typename T, class packingT>
    constexpr auto inverse(const matrix_t<3, 3, T, packingT> & A) -> matrix_t<3, 3, T, packingT>
    {
        matrix_t<3, 3, T, packingT> invA;
        T det = determinant(A);
        assert(det != 0.0);
        T detinv = 1.0 / det;
        invA[{0, 0}] = detinv * (A[{1, 1}] * A[{2, 2}] - A[{1, 2}] * A[{2, 1}]);
        invA[{0, 1}] = detinv * (-A[{0, 1}] * A[{2, 2}] + A[{0, 2}] * A[{2, 1}]);
        invA[{0, 2}] = detinv * (A[{0, 1}] * A[{1, 2}] - A[{0, 2}] * A[{1, 1}]);
        invA[{1, 0}] = detinv * (-A[{1, 0}] * A[{2, 2}] + A[{1, 2}] * A[{2, 0}]);
        invA[{1, 1}] = detinv * (A[{0, 0}] * A[{2, 2}] - A[{0, 2}] * A[{2, 0}]);
        invA[{1, 2}] = detinv * (-A[{0, 0}] * A[{1, 2}] + A[{0, 2}] * A[{1, 0}]);
        invA[{2, 0}] = detinv * (A[{1, 0}] * A[{2, 1}] - A[{1, 1}] * A[{2, 0}]);
        invA[{2, 1}] = detinv * (-A[{0, 0}] * A[{2, 1}] + A[{0, 1}] * A[{2, 0}]);
        invA[{2, 2}] = detinv * (A[{0, 0}] * A[{1, 1}] - A[{0, 1}] * A[{1, 0}]);
        return invA;
    }

    template <typename T, class packingT>
    constexpr auto inverse(const matrix_t<2, 2, T, packingT> & A) -> matrix_t<2, 2, T, packingT>
    {
        matrix_t<2, 2, T, packingT> invA;
        T det = determinant(A);
        assert(det != 0.0);
        T detinv = 1.0 / det;
        invA[{0, 0}] = detinv * (A[{1, 1}]);
        invA[{0, 1}] = detinv * (-A[{0, 1}]);
        invA[{1, 0}] = detinv * (-A[{1, 0}]);
        invA[{1, 1}] = detinv * (A[{0, 0}]);
        return invA;
    }

    template <int D, typename T, class packingT>
    constexpr auto trace(const matrix_t<D, D, T, packingT> & A) -> T
    {
        auto _trace = [&A]<int... J>(integer_sequence<J...>) -> T
        {
            return (A[{J, J}]+ ... );
        };
        return _trace(make_integer_sequence<D> {});
    }

    template <int D1, int D2, typename T, class packingT>
    constexpr auto transpose(const matrix_t<D1, D2, T, packingT> & A)
    {
        // A transposed
        matrix_t<D2, D1, T, packingT> AT;
        auto _transposeJ = [&A, &AT]<int... J>(integer_sequence<J...>){
            auto _transposeI = [&A, &AT]<int K, int... I>(integer_sequence<I...>)
            {
                ((AT[{K, I}] = A [{I, K}]), ... );
                return;
            };
            (_transposeI.template operator()<J>(make_integer_sequence<D1> {}), ...);
        };
        _transposeJ(make_integer_sequence<D2> {});
        return AT;
    }

    template <int D, typename T, class packingT>
    constexpr auto symmetric(const matrix_t<D, D, T, packingT> & A) -> symmetric_matrix_t<D, T>
    {
        symmetric_matrix_t<D, T> sym;
        auto _fill_column = [&A, &sym]<int... K>(integer_sequence<K...>){
            auto _fill_row = [&A, &sym]<int J, int... I>(integer_sequence<I...>)
            {
                ((sym[{I, J}] = 0.5 * (A[{I, J}] + A[{J, I}])), ... );
                return;
            };
            (_fill_row.template operator()<K>(make_integer_sequence<D> {}), ...);
        };
        _fill_column(make_integer_sequence<D> {});
        return sym;
    }

    template <int D, typename T, class packingT>
    constexpr auto skew(const matrix_t<D, D, T, packingT> & A) -> auto
    requires (!std::is_same_v<packingT, pyre::grid::symmetric_t<2>>) 
    {
        return 0.5 * (A - transpose(A));
    }

    template <int D, typename T>
    constexpr auto skew(const symmetric_matrix_t<D, T> & A) -> auto
    {
        return symmetric_matrix_t<D, T>::zero;
    }

    template <typename T>
    constexpr auto eigenvalues(const symmetric_matrix_t<2, T> & A) -> vector_t<2, T>
    {
        T delta = sqrt(4.0 * A[{0, 1}] * A[{0, 1}] 
            + (A[{0, 0}] - A[{1, 1}]) * (A[{0, 0}] - A[{1, 1}]));
        return vector_t<2, T>{
            0.5 * (A[{0, 0}] + A[{1, 1}] + delta), 
            0.5 * (A[{0, 0}] + A[{1, 1}] - delta)};
    }

    template <typename T>
    constexpr auto eigenvectors(const symmetric_matrix_t<2, T> & A) -> matrix_t<2, 2, T>
    {
        T delta = sqrt(4.0 * A[{0, 1}] * A[{0, 1}] 
            + (A[{0, 0}] - A[{1, 1}]) * (A[{0, 0}] - A[{1, 1}]));
        matrix_t<2, 2, T> eigenvector_matrix;
        eigenvector_matrix[{0, 0}] = A[{0, 0}] - A[{1, 1}] + delta;
        eigenvector_matrix[{0, 1}] = A[{0, 0}] - A[{1, 1}] - delta;
        eigenvector_matrix[{1, 0}] = 2.0 * A[{1, 0}];
        eigenvector_matrix[{1, 1}] = 2.0 * A[{1, 0}];
        return eigenvector_matrix;
    }

    template <typename T>
    constexpr auto eigenvalues(const symmetric_matrix_t<3, T> & A) -> vector_t<3, T>
    {
        T a11 = A[{0, 0}];
        T a22 = A[{1, 1}];
        T a33 = A[{2, 2}];
        T a12 = A[{0, 1}];
        T a13 = A[{0, 2}];
        T a23 = A[{1, 2}];

        // Formula from Kopp 2008, "Efficient numerical diagonalization of hermitian 3 × 3 matrices"
        T c0 = a11 * a23 * a23 
            + a22 * a13 * a13 
            + a33 * a12 * a12 
            - a11 * a22 * a33 
            - 2.0 * a13 * a12 * a23;
        T c1 = a11 * a22 
            + a11 * a33 
            + a22 * a33 
            - a12 * a12 
            - a13 * a13 
            - a23 * a23;
        T c2 = - a11 - a22 - a33;

        T p = c2 * c2 - 3.0 * c1;
        T q = - 13.5 * c0 - c2 * c2 * c2 + 4.5 * c1 * c2;
        T num = sqrt(27.0 * (0.25 * c1 * c1 * (p - c1) + c0 * (q + 6.75 * c0)));
        T den = q;
        T phi = 1.0 / 3.0 * atan2(num, den);

        T x1 = 2.0 * cos(phi);
        T x2 = - cos(phi) - sqrt(3.0) * sin(phi);
        T x3 = - cos(phi) + sqrt(3.0) * sin(phi);

        T p_sqrt_3 = sqrt(p) / 3.0;

        return vector_t<3, T>{ 
            p_sqrt_3 * x1 - c2 / 3.0, 
            p_sqrt_3 * x2 - c2 / 3.0, 
            p_sqrt_3 * x3 - c2 / 3.0
        };
    }

    template <typename T>
    constexpr auto eigenvectors(const symmetric_matrix_t<3, T> & A) -> matrix_t<3, 3, T>
    {
        // get the eigenvalues
        auto lambda = eigenvalues(A);
        auto eps = pyre::algebra::epsilon(norm(A));

        // first eigenvector
        vector_t<3, T> v0;
        auto a = col<0>(A) - lambda[0] * vector_t<3, T>{1, 0, 0};
        auto b = col<1>(A) - lambda[0] * vector_t<3, T>{0, 1, 0};
        if (norm(a) <= eps) {
            v0 = vector_t<3, T>{1, 0, 0};
        }
        else if (norm(b) <= eps) {
            v0 = vector_t<3, T>{0, 1, 0};
        }
        else {
            v0 = cross(a, b);
            if (norm(v0) <= eps) {
                auto mu = norm(a) / norm(b);
                v0 = vector_t<3, T>{1, -mu, 0};
            }
        }

        // second eigenvector
        vector_t<3, T> v1;
        // second eigenvalue is repeated
        if(lambda[1] == lambda[0]) {
            auto a = col<0>(A) - lambda[0] * vector_t<3, T>{1, 0, 0};
            if (norm(a) <= eps) {
                auto b = col<1>(A) - lambda[0] * vector_t<3, T>{0, 1, 0};
                if (norm(b) <= eps) {
                    v1 = vector_t<3, T>{0, 1, 0};
                }
                else {
                    v1 = cross(v0, b);
                }
            }
            else {
                v1 = cross(v0, a);      
            }
        }
        else { // lambda[1] != lambda[0]
            auto a = col<0>(A) - lambda[1] * vector_t<3, T>{1, 0, 0};
            auto b = col<1>(A) - lambda[1] * vector_t<3, T>{0, 1, 0};
            if (norm(a) <= eps) {
                v1 = vector_t<3, T>{1, 0, 0};
            }
            else if (norm(b) <= eps) {
                v1 = vector_t<3, T>{0, 1, 0};
            }
            else {
                v1 = cross(a, b);
                if (norm(v1) <= eps) {
                    auto mu = norm(a) / norm(b);
                    v1 = vector_t<3, T>{1, -mu, 0};
                }
            }
        }

        // third eigenvector
        vector_t<3, T> v2 = cross(v0, v1);

        // build and return the matrix of eigenvectors
        return matrix_column<0>(v0) + matrix_column<1>(v1) + matrix_column<2>(v2);
    }

    template <int D, typename T>
    constexpr auto eigenvalues(const diagonal_matrix_t<D, T> & A) -> auto
    {
        // the diagonal entries are the eigenvalues
        return matrix_diagonal(A);
    }

    template <int D, typename T>
    constexpr auto eigenvectors(const diagonal_matrix_t<D, T> & A) -> auto
    {
        // the canonical basis is the set of eigenvectors
        return diagonal_matrix_t<D, T>::identity;
    }

    template <int I, int D1, int D2, typename T, class packingT>
    constexpr auto row(const matrix_t<D1, D2, T, packingT> & A) -> vector_t<D2, T>
    {
        auto _row = [&A]<int... J>(integer_sequence<J...>) -> vector_t<D2, T>
        {
            auto wrap = [&A]<int K>()->T { return  A[{I, K}]; };
            return vector_t<D2, T>(wrap.template operator()<J>()...);
        };
        return _row(make_integer_sequence<D1> {});
    }

    template <int I, int D1, int D2, typename T, class packingT>
    constexpr auto col(const matrix_t<D1, D2, T, packingT> & A) -> vector_t<D1, T>
    {
        auto _col = [&A]<int... J>(integer_sequence<J...>) -> vector_t<D1, T>
        {
            auto wrap = [&A]<int K>()->T { return A[{K, I}]; };
            return vector_t<D1, T>(wrap.template operator()<J>()...);
        };
        return _col(make_integer_sequence<D2> {});
    }

    template <int D, typename T, class packingT>
    constexpr auto function(const matrix_t<D, D, T, packingT> & A, auto f) -> auto
    {
        // compute eigenvalues
        auto lambda = matrix_diagonal(eigenvalues(A));
        // compute eigenvectors
        auto P = eigenvectors(A);
        // helper function (component-wise)
        constexpr auto _apply_f_to_diagonal = []<int... I>(auto & lambda, auto f, 
            integer_sequence<I...>)
        {
            // apply f to diagonal
            ((lambda[{I, I}] = f(lambda[{I, I}])), ...);
            // all done
            return;
        };
        // change eigenvalues into f(eigenvalues)
        _apply_f_to_diagonal(lambda, f, make_integer_sequence<D> {});
        // rebuild matrix
        return symmetric(P * lambda * inverse(P));
    }
}


#endif

// end of file
