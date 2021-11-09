// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 2021 all rights reserved
//

#include "Tensor.h"
#include <cassert>
#include <cmath>
#include <functional>

namespace pyre {
    namespace algebra {

        template <typename T, int... I>
        constexpr inline bool operator==(const Tensor<T, I...> & lhs, const Tensor<T, I...> & rhs)
        {
            // helper function (operator== component-wise)
            constexpr auto _operatorEqualEqual = []<size_t... J>(std::index_sequence<J...>, 
                const Tensor<T, I...> & lhs, const Tensor<T, I...> & rhs) {
                // if all components are equal
                if (((lhs[J] == rhs[J]) && ...)) {
                    // then the tensors are equal
                    return true;
                }
                // then the tensors differ
                return false;
            };

            // the size of the tensor
            constexpr int D = Tensor<T, I...>::size;
            // all done
            return _operatorEqualEqual(std::make_index_sequence<D> {}, lhs, rhs);
        }

        // Algebraic operations on vectors, tensors, ...
        // vector_t times scalar
        template <typename T, int... I, size_t... J>
        constexpr inline void _vector_times_scalar(
            const T & a, const Tensor<T, I...> & y, Tensor<T, I...> & result,
            std::index_sequence<J...>)
        {
            ((result[J] = y[J] * a), ...);
            return;
        }
        template <typename T, int... I>
        constexpr inline Tensor<T, I...> && operator*(const T & a, Tensor<T, I...> && y) 
            requires(Tensor<T, I...>::size != 1)
        {
            constexpr int D = Tensor<T, I...>::size;
            _vector_times_scalar(a, y, y, std::make_index_sequence<D> {});
            return std::move(y);
        }
        template <typename T, int... I>
        constexpr inline Tensor<T, I...> operator*(const T & a, const Tensor<T, I...> & y) 
            requires(Tensor<T, I...>::size != 1)
        {
            Tensor<T, I...> result;
            constexpr int D = Tensor<T, I...>::size;
            _vector_times_scalar(a, y, result, std::make_index_sequence<D> {});
            return result;
        }
        template <typename T, int... I>
        constexpr inline Tensor<T, I...> && operator*(Tensor<T, I...> && y, const T & a) 
            requires(Tensor<T, I...>::size != 1)
        {
            return a * std::move(y);
        }
        template <typename T, int... I>
        constexpr inline Tensor<T, I...> operator*(const Tensor<T, I...> & y, const T & a) 
            requires(Tensor<T, I...>::size != 1)
        {
            return a * y;
        }

        // sum of vector_t
        template <typename T, int... I, std::size_t... J>
        constexpr inline void _vector_sum(
            const Tensor<T, I...> & y1, const Tensor<T, I...> & y2,
            Tensor<T, I...> & result, std::index_sequence<J...>)
        {
            ((result[J] = y1[J] + y2[J]), ...);
            return;
        }
        template <typename T, int... I>
        constexpr inline Tensor<T, I...> operator+(
            const Tensor<T, I...> & y1, const Tensor<T, I...> & y2)
        {
            // std::cout << "operator+ new temp" << std::endl;
            Tensor<T, I...> result;
            constexpr int D = Tensor<T, I...>::size;
            _vector_sum(y1, y2, result, std::make_index_sequence<D> {});
            return result;
        }
        template <typename T, int... I>
        constexpr inline Tensor<T, I...> && operator+(
            Tensor<T, I...> && y1, const Tensor<T, I...> & y2)
        {
            // std::cout << "operator+ no temp && &" << std::endl;
            constexpr int D = Tensor<T, I...>::size;
            _vector_sum(y1, y2, y1, std::make_index_sequence<D> {});
            return std::move(y1);
        }
        template <typename T, int... I>
        constexpr inline Tensor<T, I...> && operator+(
            const Tensor<T, I...> & y1, Tensor<T, I...> && y2)
        {
            // std::cout << "operator+ no temp & &&" << std::endl;
            return std::move(y2) + y1;
        }
        template <typename T, int... I>
        constexpr inline Tensor<T, I...> && operator+(Tensor<T, I...> && y1, Tensor<T, I...> && y2)
        {
            // std::cout << "operator+ no temp && &&" << std::endl;
            constexpr int D = Tensor<T, I...>::size;
            _vector_sum(y1, y2, y1, std::make_index_sequence<D> {});
            return std::move(y1);
        }

        // vector_t operator-
        template <typename T, int... I, std::size_t... J>
        constexpr inline void _vector_minus(
            const Tensor<T, I...> & y, Tensor<T, I...> & result, std::index_sequence<J...>)
        {
            ((result[J] = -y[J]), ...);
            return;
        }
        template <typename T, int... I>
        constexpr inline Tensor<T, I...> operator-(const Tensor<T, I...> & y)
        {
            // std::cout << "unary operator- new temp" << std::endl;
            Tensor<T, I...> result;
            constexpr int D = Tensor<T, I...>::size;
            _vector_minus(y, result, std::make_index_sequence<D> {});
            return result;
        }
        template <typename T, int... I>
        constexpr inline Tensor<T, I...> && operator-(Tensor<T, I...> && y)
        {
            // std::cout << "unary operator- no temp &&" << std::endl;
            constexpr int D = Tensor<T, I...>::size;
            _vector_minus(y, y, std::make_index_sequence<D> {});
            return std::move(y);
        }
        template <typename T, int... I, std::size_t... J>
        constexpr inline void _vector_minus(
            const Tensor<T, I...> & y1, const Tensor<T, I...> & y2,
            Tensor<T, I...> & result, std::index_sequence<J...>)
        {
            ((result[J] = y1[J] - y2[J]), ...);
            return;
        }
        template <typename T, int... I>
        constexpr inline Tensor<T, I...> operator-(
            const Tensor<T, I...> & y1, const Tensor<T, I...> & y2)
        {
            // std::cout << "binary operator- new temp" << std::endl;
            Tensor<T, I...> result;
            constexpr int D = Tensor<T, I...>::size;
            _vector_minus(y1, y2, result, std::make_index_sequence<D> {});
            return result;
            // return y1 + (-y2);
        }
        template <typename T, int... I>
        constexpr inline Tensor<T, I...> && operator-(
            Tensor<T, I...> && y1, const Tensor<T, I...> & y2)
        {
            // std::cout << "binary operator- no temp && &" << std::endl;
            constexpr int D = Tensor<T, I...>::size;
            _vector_minus(y1, y2, y1, std::make_index_sequence<D> {});
            return std::move(y1);
            // return std::move(y1) + (-y2);
        }
        template <typename T, int... I>
        constexpr inline Tensor<T, I...> && operator-(
            const Tensor<T, I...> & y1, Tensor<T, I...> && y2)
        {
            // std::cout << "binary operator- no temp & &&" << std::endl;
            constexpr int D = Tensor<T, I...>::size;
            _vector_minus(y1, y2, y2, std::make_index_sequence<D> {});
            return std::move(y2);
            // return y1 + (-std::move(y2));
        }
        template <typename T, int... I>
        constexpr inline Tensor<T, I...> && operator-(Tensor<T, I...> && y1, Tensor<T, I...> && y2)
        {
            // std::cout << "binary operator- no temp && &&" << std::endl;
            constexpr int D = Tensor<T, I...>::size;
            _vector_minus(y1, y2, y1, std::make_index_sequence<D> {});
            return std::move(y1);
            // return std::move(y1) + (-std::move(y2));
        }

        template <typename T, int... I>
        constexpr inline Tensor<T, I...> operator/(const Tensor<T, I...> & y, const T & a) requires(
            Tensor<T, I...>::size != 1)
        {
            return (1.0 / a) * y;
        }

        template <typename T, int... I>
        constexpr inline Tensor<T, I...> && operator/(Tensor<T, I...> && y, const T & a) requires(
            Tensor<T, I...>::size != 1)
        {
            return (1.0 / a) * std::move(y);
        }

        // builds a square matrix with all zeros except the K-th row is equal to v
        template <int K, int D, typename T>
        constexpr inline matrix_t<D, D, T> matrix_row(const vector_t<D, T> & v)
        {
            constexpr auto _fill_matrix_row = []<size_t... I>(
                matrix_t<D, D, T> A, const vector_t<D, T> & v, std::index_sequence<I...>) 
                -> matrix_t<D, D, T>
            {
                ((A[{K, I}] = v[{ I }]), ...);
                return A;
            };

            // fill row K of a zero matrix with vector v
            return _fill_matrix_row(matrix_t<D, D, T>::zero, v, std::make_index_sequence<D> {});
        }

        // builds a square matrix with all zeros except the K-th column is equal to v
        template <int K, int D, typename T>
        constexpr inline matrix_t<D, D, T> matrix_column(const vector_t<D, T> & v)
        {
            constexpr auto _fill_matrix_column = []<size_t... I>(
                matrix_t<D, D, T> A, const vector_t<D, T> & v, std::index_sequence<I...>) 
                -> matrix_t<D, D, T>
            {
                ((A[{I, K}] = v[{ I }]), ...);
                return A;
            };

            // fill column K of a zero matrix with vector v
            return _fill_matrix_column(matrix_t<D, D, T>::zero, v, std::make_index_sequence<D> {});
        }

        // builds a square matrix with all zeros except the diagonal is equal to v
        template <int D, typename T>
        constexpr inline matrix_t<D, D, T> matrix_diagonal(const vector_t<D, T> & v)
        {
            constexpr auto _fill_matrix_diagonal = []<size_t... I>(
                matrix_t<D, D, T> A, const vector_t<D, T> & v, std::index_sequence<I...>) 
                -> matrix_t<D, D, T>
            {
                ((A[{I, I}] = v[{ I }]), ...);
                return A;
            };

            // fill diagonal of a zero matrix with vector v
            return _fill_matrix_diagonal(matrix_t<D, D, T>::zero, v, 
                std::make_index_sequence<D> {});
        }

        // builds the vector with the diagonal entries of a matrix
        template <int D, typename T>
        constexpr inline vector_t<D, T> matrix_diagonal(const matrix_t<D, D, T> & A)
        {

            auto _fill_vector_with_matrix_diagonal = [&A]<size_t... J>(std::index_sequence<J...>) -> vector_t<D, T>
            {
                auto wrap = [&A]<size_t K>()->T { return  A[{K, K}]; };
                return vector_t<D, T>(wrap.template operator()<J>()...);
            };

            // fill a vector with the diagonal of A and return it
            return _fill_vector_with_matrix_diagonal(std::make_index_sequence<D> {});
        }

        // row-column vector product
        template <int D, typename T>
        constexpr inline T operator*(
            const vector_t<D, T> & v1, const vector_t<D, T> & v2) 
        {
            // helper function (scalar product)
            constexpr auto _vector_times_vector = []<size_t... K>(
                const vector_t<D, T> & v1, const vector_t<D, T> & v2, 
                std::index_sequence<K...>) ->T 
            { 
                return ((v1[{ K }] * v2[{ K }]) + ...);
            };

            return _vector_times_vector(v1, v2, std::make_index_sequence<D> {});
        }
        // matrix-vector multiplication
        template <int D1, int D2, typename T>
        constexpr inline vector_t<D1, T> operator*(
            const matrix_t<D1, D2, T> & A, const vector_t<D2, T> & v) 
        {
            // helper function
            constexpr auto _matrix_times_vector = []<size_t... K>(
                const matrix_t<D1, D2, T> & A, const vector_t<D2, T> & v, 
                std::index_sequence<K...>) -> vector_t<D1, T> 
            { 
                return vector_t<D1, T>((row<K>(A) * v)...);
            };
            return _matrix_times_vector(A, v, std::make_index_sequence<D2> {});
        }
        // vector-matrix multiplication
        template <int D1, int D2, typename T>
        constexpr inline vector_t<D1, T> operator*(const vector_t<D2, T> & v, 
            const matrix_t<D1, D2, T> & A) 
        {
            return transpose(A) * v;
        }
        // matrix-matrix multiplication
        template <int D1, int D2, int D3, typename T>
        constexpr inline matrix_t<D1, D3, T> operator*(
            const matrix_t<D1, D2, T> & A1, const matrix_t<D2, D3, T> & A2) 
            requires(D1 != 1 && D2 != 1 && D3 != 1)
        {
            // helper function
            constexpr auto _matrix_times_matrix = []<size_t... K>(
                const matrix_t<D1, D2, T> & A1, const matrix_t<D2, D3, T> & A2, 
                std::index_sequence<K...>) -> matrix_t<D1, D3, T> 
            {
                // for each K build the matrix whose column K is equal to A1 * col<K>(A2)
                // then add them all up
                return (matrix_column<K>(A1 * col<K>(A2)) + ...);
            };

            return _matrix_times_matrix(A1, A2, std::make_index_sequence<D3> {});
        }

        // the skew symmetric matrix representing vector a  
        template <typename T>
        constexpr inline matrix_t<3, 3, T> skew(const vector_t<3, T> & a)
        {
            matrix_t<3, 3, T> A = zero_matrix<3>;
            A[{0, 1}] = -a[2];
            A[{0, 2}] = a[1];
            A[{1, 0}] = a[2];
            A[{1, 2}] = -a[0];
            A[{2, 0}] = -a[1];
            A[{2, 1}] = a[0];

            return A;
        }

        template <typename T>
        constexpr inline auto cross(const vector_t<3, T> & a, const vector_t<3, T> & b)
        {
            return skew(a) * b;
        }

        template <typename T>
        constexpr inline T cross(const vector_t<2, T> & a, const vector_t<2, T> & b)
        {
            vector_t<3, T> a3 {a[0], a[1], 0.0};
            vector_t<3, T> b3 {b[0], b[1], 0.0};
            return cross(a3, b3)[2];
        }

        // factorial
        template <int D>
        constexpr inline int factorial()
        {
            return D * factorial<int(D - 1)>();
        }
        template <>
        constexpr inline int factorial<1>()
        {
            return 1;
        }

        template <typename T>
        constexpr inline T determinant(const matrix_t<4, 4, T> & A)
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

        template <typename T>
        constexpr inline T determinant(const matrix_t<3, 3, T> & A)
        {
            return A[{0, 0}] * (A[{1, 1}] * A[{2, 2}] - A[{1, 2}] * A[{2, 1}]) 
                 - A[{0, 1}] * (A[{1, 0}] * A[{2, 2}] - A[{1, 2}] * A[{2, 0}])
                 + A[{0, 2}] * (A[{1, 0}] * A[{2, 1}] - A[{1, 1}] * A[{2, 0}]);
        }

        template <typename T>
        constexpr inline T determinant(const matrix_t<2, 2, T> & A)
        {
            return A[{0, 0}] * A[{1, 1}] - A[{0, 1}] * A[{1, 0}];
        }

        template <typename T>
        constexpr inline matrix_t<3, 3, T> inverse(const matrix_t<3, 3, T> & A)
        {
            matrix_t<3, 3, T> invA;

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

        template <typename T>
        constexpr inline matrix_t<2, 2, T> inverse(const matrix_t<2, 2, T> & A)
        {
            matrix_t<2, 2, T> invA;

            T det = determinant(A);
            assert(det != 0.0);

            T detinv = 1.0 / det;
            invA[{0, 0}] = detinv * (A[{1, 1}]);
            invA[{0, 1}] = detinv * (-A[{0, 1}]);
            invA[{1, 0}] = detinv * (-A[{1, 0}]);
            invA[{1, 1}] = detinv * (A[{0, 0}]);

            return invA;
        }

        template <int D, typename T>
        constexpr inline T trace(const matrix_t<D, D, T> & A)
        {
            auto _trace = [&A]<size_t... J>(std::index_sequence<J...>) ->T
            {
                return (A[{J, J}]+ ... );
            };

            return _trace(std::make_index_sequence<D> {});
        }

        template <int D1, int D2, typename T>
        constexpr inline matrix_t<D2, D1, T> transpose(const matrix_t<D1, D2, T> & A)
        {
            // A transposed
            matrix_t<D2, D1, T> AT;

            auto _transposeJ = [&A, &AT]<size_t... J>(std::index_sequence<J...>){
                auto _transposeI = [&A, &AT]<size_t K, size_t... I>(std::index_sequence<I...>)
                {
                    ((AT[{K, I}] = A [{I, K}]), ... );
                    return;
                };

                (_transposeI.template operator()<J>(std::make_index_sequence<D1> {}), ...);
            };

            _transposeJ(std::make_index_sequence<D2> {});

            return AT;
        }

        // TOFIX: This still does a complete loop while it should do a upper-diagonal loop
        template <int D, typename T>
        constexpr inline symmetric_matrix_t<D, T> symmetric(const matrix_t<D, D, T> & A)
        {
            symmetric_matrix_t<D, T> sym;

            auto _fill_column = [&A, &sym]<size_t... K>(std::index_sequence<K...>){
                auto _fill_row = [&A, &sym]<size_t J, size_t... I>(std::index_sequence<I...>)
                {
                    ((sym[{I, J}] = 0.5 * (A[{I, J}] + A[{J, I}])), ... );
                    return;
                };

                (_fill_row.template operator()<K>(std::make_index_sequence<D> {}), ...);
            };

            _fill_column(std::make_index_sequence<D> {});
            return sym;
        }

        template <int D, typename T>
        constexpr inline matrix_t<D, D, T> skew(const matrix_t<D, D, T> & A)
        {
            return 0.5 * (A - transpose(A));
        }

        template <typename T>
        constexpr inline vector_t<2, T> eigenvalues(const symmetric_matrix_t<2, T> & A)
        {
            T delta = sqrt(4.0 * A[{0, 1}] * A[{0, 1}] 
                + (A[{0, 0}] - A[{1, 1}]) * (A[{0, 0}] - A[{1, 1}]));
            return vector_t<2, T>{
                0.5 * (A[{0, 0}] + A[{1, 1}] + delta), 
                0.5 * (A[{0, 0}] + A[{1, 1}] - delta)};
        }

        template <typename T>
        constexpr inline matrix_t<2, 2, T> eigenvectors(const symmetric_matrix_t<2, T> & A)
        {
            T delta = sqrt(4.0 * A[{0, 1}] * A[{0, 1}] 
                + (A[{0, 0}] - A[{1, 1}]) * (A[{0, 0}] - A[{1, 1}]));

            return matrix_t<2, 2, T>{
                (A[{0, 0}] - A[{1, 1}] + delta) / (2.0 * A[{1, 0}]), 
                (A[{0, 0}] - A[{1, 1}] - delta) / (2.0 * A[{1, 0}]),
                1.0, 
                1.0};
        }

        template <typename T>
        constexpr inline vector_t<3, T> eigenvalues(const matrix_t<3, 3, T> & A)
        {
            // https://hal.archives-ouvertes.fr/hal-01501221
            T x1 = A[{0, 0}] * A[{0, 0}] + A[{1, 1}] * A[{1, 1}] + A[{2, 2}] * A[{2, 2}] 
                - A[{0, 0}] * A[{1, 1}] - A[{0, 0}] * A[{2, 2}] - A[{1, 1}] * A[{2, 2}]
                + 3.0 * (A[{0, 1}] * A[{0, 1}] + A[{0, 2}] * A[{0, 2}] + A[{1, 2}] * A[{1, 2}]);

            T a = 2.0 * A[{0, 0}] - A[{1, 1}] - A[{2, 2}];
            T b = 2.0 * A[{1, 1}] - A[{0, 0}] - A[{2, 2}];
            T c = 2.0 * A[{2, 2}] - A[{0, 0}] - A[{1, 1}];

            T x2 =  - a * b * c
                    + 9.0 * (c * A[{0, 1}] * A[{0, 1}] + b * A[{0, 2}] * A[{0, 2}] 
                        + a * A[{1, 2}] * A[{1, 2}])
                    - 54.0 * A[{0, 1}] * A[{0, 2}] * A[{1, 2}];

            T d = (A[{0, 0}] + A[{1, 1}] + A[{2, 2}]) / 3.0;
            T e = 2.0 * sqrt(x1) / 3.0;

            double PI = 4.0 * atan(1.0);
            double tol = 1.e-16; //TOFIX
            T phi = 0.0;
            if (fabs(x2) < tol) {
                phi = 0.5 * PI;
            } 
            else{
                T two_sqrt_x1 = 2.0 * sqrt(x1);
                phi = atan(sqrt((two_sqrt_x1 * x1 - x2) * (two_sqrt_x1 * x1 + x2)) / x2);
                if (x2 < 0) phi += PI;
            }

            return vector_t<3, T>{ 
                d - e * cos(phi / 3.0), 
                d + e * cos((phi - PI) / 3.0), 
                d + e * cos((phi + PI) / 3.0)
            };
        }

        template <typename T>
        constexpr inline matrix_t<3, 3, T> eigenvectors(const symmetric_matrix_t<3, T> & A)
        {
            // TODO: Manage special cases f = 0, denominators = 0
            auto lambda = eigenvalues(A);
            T m0 = (A[{0, 1}] * (A[{2, 2}] - lambda[0]) - A[{1, 2}] * A[{0, 2}]) / 
                (A[{0, 2}] * (A[{1, 1}] - lambda[0]) - A[{0, 1}] * A[{1, 2}]);

            T m1 = (A[{0, 1}] * (A[{2, 2}] - lambda[1]) - A[{1, 2}] * A[{0, 2}]) / 
                (A[{0, 2}] * (A[{1, 1}] - lambda[1]) - A[{0, 1}] * A[{1, 2}]);

            T m2 = (A[{0, 1}] * (A[{2, 2}] - lambda[2]) - A[{1, 2}] * A[{0, 2}]) / 
                (A[{0, 2}] * (A[{1, 1}] - lambda[2]) - A[{0, 1}] * A[{1, 2}]);

            return matrix_t<3, 3, T>{
                (lambda[0] - A[{2, 2}] - A[{1, 2}] * m0) / A[{0, 2}], 
                (lambda[1] - A[{2, 2}] - A[{1, 2}] * m1) / A[{0, 2}],
                (lambda[2] - A[{2, 2}] - A[{1, 2}] * m2) / A[{0, 2}],
                m0,
                m1,
                m2,
                1.0, 
                1.0,
                1.0};
        }

        template <int D, typename T>
        constexpr inline auto eigenvalues(const diagonal_matrix_t<D, T> & A)
        {
            // the diagonal entries are the eigenvalues
            return matrix_diagonal(A);
        }

        template <int D, typename T>
        constexpr inline auto eigenvectors(const diagonal_matrix_t<D, T> & A)
        {
            // the canonical basis is the set of eigenvectors
            return identity_matrix<D>;
        }

        template <int I, int D1, int D2, typename T>
        constexpr inline vector_t<D2, T> row(const matrix_t<D1, D2, T> & A)
        {
            auto _row = [&A]<size_t... J>(std::index_sequence<J...>) -> vector_t<D2, T>
            {
                auto wrap = [&A]<size_t K>()->T { return  A[{I, K}]; };
                return vector_t<D2, T>(wrap.template operator()<J>()...);
            };

            return _row(std::make_index_sequence<D1> {});
        }

        template <int I, int D1, int D2, typename T>
        constexpr inline vector_t<D1, T> col(const matrix_t<D1, D2, T> & A)
        {
            auto _col = [&A]<size_t... J>(std::index_sequence<J...>) -> vector_t<D1, T>
            {
                auto wrap = [&A]<size_t K>()->T { return A[{K, I}]; };
                return vector_t<D1, T>(wrap.template operator()<J>()...);
            };

            return _col(std::make_index_sequence<D2> {});
        }

        template <int D, typename T>
        constexpr inline symmetric_matrix_t<D, T> function(const symmetric_matrix_t<D, T> & A, auto f)
        {
            // compute eigenvalues
            auto lambda = matrix_diagonal(eigenvalues(A));

            // compute eigenvectors
            auto P = eigenvectors(A);

            // helper function (component-wise)
            constexpr auto _apply_f_to_diagonal = []<size_t... I>(matrix_t<D, D, T> & lambda, 
                auto f, std::index_sequence<I...>)
            {
                // apply f to diagonal
                ((lambda[{I, I}] = f(lambda[{I, I}])), ...);

                // all done
                return;
            };

            // change eigenvalues into f(eigenvalues)
            _apply_f_to_diagonal(lambda, f, std::make_index_sequence<D> {});

            // rebuild matrix
            return P * lambda * inverse(P);
        }

    }
}

// end of file
