// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 2021 all rights reserved
//

#include "Tensor.h"
#include <cassert>
#include <cmath>

namespace pyre {
    namespace algebra {

        template <typename T, int... I>
        constexpr inline bool operator==(const Tensor<T, I...> & lhs, const Tensor<T, I...> & rhs)
        {
            constexpr int D = Tensor<T, I...>::size;

            // helper function
            constexpr auto _operatorEqualEqual = []<size_t... J>(std::index_sequence<J...>, 
                const Tensor<T, I...> & lhs, const Tensor<T, I...> & rhs) {
                if (((lhs[J] == rhs[J]) && ...))
                    return true;
                return false;
            };

            // all done
            return _operatorEqualEqual(std::make_index_sequence<D> {}, lhs, rhs);
        }


        // Algebraic operations on vectors, tensors, ...
        // TOFIX: generalize with respect to scalar type (in this case real)

        // vector_t times scalar
        template <typename T, int... I, size_t... J>
        inline void _vector_times_scalar(
            const T & a, const Tensor<T, I...> & y, Tensor<T, I...> & result,
            std::index_sequence<J...>)
        {
            ((result[J] = y[J] * a), ...);
            return;
        }
        template <typename T, int... I>
        inline Tensor<T, I...> && operator*(const T & a, Tensor<T, I...> && y) requires(
            Tensor<T, I...>::size != 1)
        {
            constexpr int D = Tensor<T, I...>::size;
            _vector_times_scalar(a, y, y, std::make_index_sequence<D> {});
            return std::move(y);
        }
        template <typename T, int... I>
        inline Tensor<T, I...> operator*(const T & a, const Tensor<T, I...> & y) requires(
            Tensor<T, I...>::size != 1)
        {
            Tensor<T, I...> result;
            constexpr int D = Tensor<T, I...>::size;
            _vector_times_scalar(a, y, result, std::make_index_sequence<D> {});
            return result;
        }
        template <typename T, int... I>
        inline Tensor<T, I...> && operator*(Tensor<T, I...> && y, const T & a) requires(
            Tensor<T, I...>::size != 1)
        {
            return a * std::move(y);
        }
        template <typename T, int... I>
        inline Tensor<T, I...> operator*(const Tensor<T, I...> & y, const T & a) requires(
            Tensor<T, I...>::size != 1)
        {
            return a * y;
        }

        // sum of vector_t
        template <typename T, int... I, std::size_t... J>
        inline void _vector_sum(
            const Tensor<T, I...> & y1, const Tensor<T, I...> & y2,
            Tensor<T, I...> & result, std::index_sequence<J...>)
        {
            ((result[J] = y1[J] + y2[J]), ...);
            return;
        }
        template <typename T, int... I>
        inline Tensor<T, I...> operator+(
            const Tensor<T, I...> & y1, const Tensor<T, I...> & y2)
        {
            // std::cout << "operator+ new temp" << std::endl;
            Tensor<T, I...> result;
            constexpr int D = Tensor<T, I...>::size;
            _vector_sum(y1, y2, result, std::make_index_sequence<D> {});
            return result;
        }
        template <typename T, int... I>
        inline Tensor<T, I...> && operator+(
            Tensor<T, I...> && y1, const Tensor<T, I...> & y2)
        {
            // std::cout << "operator+ no temp && &" << std::endl;
            constexpr int D = Tensor<T, I...>::size;
            _vector_sum(y1, y2, y1, std::make_index_sequence<D> {});
            return std::move(y1);
        }
        template <typename T, int... I>
        inline Tensor<T, I...> && operator+(
            const Tensor<T, I...> & y1, Tensor<T, I...> && y2)
        {
            // std::cout << "operator+ no temp & &&" << std::endl;
            return std::move(y2) + y1;
        }
        template <typename T, int... I>
        inline Tensor<T, I...> && operator+(Tensor<T, I...> && y1, Tensor<T, I...> && y2)
        {
            // std::cout << "operator+ no temp && &&" << std::endl;
            constexpr int D = Tensor<T, I...>::size;
            _vector_sum(y1, y2, y1, std::make_index_sequence<D> {});
            return std::move(y1);
        }

        // vector_t operator-
        template <typename T, int... I, std::size_t... J>
        inline void _vector_minus(
            const Tensor<T, I...> & y, Tensor<T, I...> & result, std::index_sequence<J...>)
        {
            ((result[J] = -y[J]), ...);
            return;
        }
        template <typename T, int... I>
        inline Tensor<T, I...> operator-(const Tensor<T, I...> & y)
        {
            // std::cout << "unary operator- new temp" << std::endl;
            Tensor<T, I...> result;
            constexpr int D = Tensor<T, I...>::size;
            _vector_minus(y, result, std::make_index_sequence<D> {});
            return result;
        }
        template <typename T, int... I>
        inline Tensor<T, I...> && operator-(Tensor<T, I...> && y)
        {
            // std::cout << "unary operator- no temp &&" << std::endl;
            constexpr int D = Tensor<T, I...>::size;
            _vector_minus(y, y, std::make_index_sequence<D> {});
            return std::move(y);
        }
        template <typename T, int... I, std::size_t... J>
        inline void _vector_minus(
            const Tensor<T, I...> & y1, const Tensor<T, I...> & y2,
            Tensor<T, I...> & result, std::index_sequence<J...>)
        {
            ((result[J] = y1[J] - y2[J]), ...);
            return;
        }
        template <typename T, int... I>
        inline Tensor<T, I...> operator-(
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
        inline Tensor<T, I...> && operator-(
            Tensor<T, I...> && y1, const Tensor<T, I...> & y2)
        {
            // std::cout << "binary operator- no temp && &" << std::endl;
            constexpr int D = Tensor<T, I...>::size;
            _vector_minus(y1, y2, y1, std::make_index_sequence<D> {});
            return std::move(y1);
            // return std::move(y1) + (-y2);
        }
        template <typename T, int... I>
        inline Tensor<T, I...> && operator-(
            const Tensor<T, I...> & y1, Tensor<T, I...> && y2)
        {
            // std::cout << "binary operator- no temp & &&" << std::endl;
            constexpr int D = Tensor<T, I...>::size;
            _vector_minus(y1, y2, y2, std::make_index_sequence<D> {});
            return std::move(y2);
            // return y1 + (-std::move(y2));
        }
        template <typename T, int... I>
        inline Tensor<T, I...> && operator-(Tensor<T, I...> && y1, Tensor<T, I...> && y2)
        {
            // std::cout << "binary operator- no temp && &&" << std::endl;
            constexpr int D = Tensor<T, I...>::size;
            _vector_minus(y1, y2, y1, std::make_index_sequence<D> {});
            return std::move(y1);
            // return std::move(y1) + (-std::move(y2));
        }

        template <typename T, int... I>
        inline Tensor<T, I...> operator/(const Tensor<T, I...> & y, const T & a) requires(
            Tensor<T, I...>::size != 1)
        {
            return (1.0 / a) * y;
        }

        template <typename T, int... I>
        inline Tensor<T, I...> && operator/(Tensor<T, I...> && y, const T & a) requires(
            Tensor<T, I...>::size != 1)
        {
            return (1.0 / a) * std::move(y);
        }

        // TODO: FORWARD!!!!!
        // matrix-vector multiplication
        // row-column product
        template <int I /* row */, int J /* col */, int D1, int D2, int D3, typename T, size_t... K>
        inline T _row_times_column(
            const tensor_t<D1, D2, T> A1, tensor_t<D2, D3, T> A2, std::index_sequence<K...>)
        {
            return ((A1[{ I, K }] * A2[{ K, J }]) + ...);
        }
        template <int I /* row */, int D1, int D2, int D3, typename T, size_t... J>
        inline tensor_t<D1, D3, T> _matrix_times_column(
            const tensor_t<D1, D2, T> A1, tensor_t<D2, D3, T> A2, std::index_sequence<J...>)
        {
            tensor_t<D1, D3, T> result;
            ((result[{I, J}] = _row_times_column<I, J>(A1, A2, std::make_index_sequence<D2> {})), ...);
            return result;
        }
        template <int D1, int D2, int D3, typename T, size_t... I>
        inline tensor_t<D1, D3, T> _matrix_times_matrix(const tensor_t<D1, D2, T> A1, const tensor_t<D2, D3, T> A2, std::index_sequence<I...>)
        {
            return (_matrix_times_column<I>(A1, A2, std::make_index_sequence<D3> {}) + ... );
        }
        template <int D1, int D2, int D3, typename T>
        inline tensor_t<D1, D3, T> operator*(const tensor_t<D1, D2, T> A1, const tensor_t<D2, D3, T> A2)
        {
            return _matrix_times_matrix(A1, A2, std::make_index_sequence<D1> {});
        }

        // factorial
        template <int D>
        int factorial()
        {
            return D * factorial<int(D - 1)>();
        }
        template <>
        int factorial<1>()
        {
            return 1;
        }

        template <typename T>
        T det(const tensor_t<4, 4, T> & A)
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
        T det(const tensor_t<3, 3, T> & A)
        {
            return A[{0, 0}] * (A[{1, 1}] * A[{2, 2}] - A[{1, 2}] * A[{2, 1}]) - A[{0, 1}] * (A[{1, 0}] * A[{2, 2}] - A[{1, 2}] * A[{2, 0}])
                 + A[{0, 2}] * (A[{1, 0}] * A[{2, 1}] - A[{1, 1}] * A[{2, 0}]);
        }

        template <typename T>
        T det(const tensor_t<2, 2, T> & A)
        {
            return A[{0, 0}] * A[{1, 1}] - A[{0, 1}] * A[{1, 0}];
        }

        template <typename T>
        T inv(const tensor_t<3, 3, T> & A, tensor_t<3, 3, T> & invA)
        {
            real det = det(A);
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

            return det;
        }

        template <typename T>
        T inv(const tensor_t<2, 2, T> & A, tensor_t<2, 2, T> & invA)
        {
            T det = det(A);
            assert(det != 0.0);

            T detinv = 1.0 / det;
            invA[{0, 0}] = detinv * (A[{1, 1}]);
            invA[{0, 1}] = detinv * (-A[{0, 1}]);
            invA[{1, 0}] = detinv * (-A[{1, 0}]);
            invA[{1, 1}] = detinv * (A[{0, 0}]);

            return det;
        }

        template <int D, typename T>
        T tr(const tensor_t<D, D, T> & A)
        {
            auto _tr = [&A]<size_t... J>(std::index_sequence<J...>) ->T
            {
                return (A[{J, J}]+ ... );
            };

            return _tr(std::make_index_sequence<D> {});
        }

        template <int D1, int D2, typename T>
        tensor_t<D2, D1, T> transpose(const tensor_t<D1, D2, T> & A)
        {
            // A transposed
            tensor_t<D2, D1, T> AT;

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

        template <int D, typename T>
        tensor_t<D, D, T> sym(const tensor_t<D, D, T> & A)
        {
            return 0.5 * (A + transpose(A));
        }

        template <int D, typename T>
        tensor_t<D, D, T> skew(const tensor_t<D, D, T> & A)
        {
            return 0.5 * (A - transpose(A));
        }

        template <typename T>
        vector_t<2, T> eigenvalues(const tensor_t<2, 2, T> & A)
        {
            T a = A[{0, 0}] * A[{0, 0}] + 4.0 * A[{0, 1}] * A[{1, 0}] - 2.0 * A[{0, 0}] * A[{1, 1}] + A[{1, 1}] * A[{1, 1}];
            return vector_t<2, T>{0.5 * (A[{0, 0}] + A[{1, 1}] - sqrt(a)), 0.5 * (A[{0, 0}] + A[{1, 1}] + sqrt(a))};
        }

        // QUESTION: should these be returned in a matrix? 
        template <typename T>
        tensor_t<2, 2, T> eigenvectors(const tensor_t<2, 2, T> & A)
        {
            T a = sqrt(A[{0, 0}] * A[{0, 0}] + 4.0 * A[{0, 1}] * A[{1, 0}] - 2.0 * A[{0, 0}] * A[{1, 1}] + A[{1, 1}] * A[{1, 1}]);
            return tensor_t<2, 2, T>{
                (A[{0, 0}] - A[{1, 1}] - a) / (2.0 * A[{1, 0}]), 
                (A[{0, 0}] - A[{1, 1}] + a) / (2.0 * A[{1, 0}]),
                1.0, 
                1.0};
        }
        template <int I, int D1, int D2, typename T>
        vector_t<D2, T> row(const tensor_t<D1, D2, T> & A)
        {
            auto _row = [&A]<size_t... J>(std::index_sequence<J...>) -> vector_t<D2, T>
            {
                auto wrap = [&A]<size_t K>()->T { return  A[{I, K}]; };
                return vector_t<D2, T>(wrap.template operator()<J>()...);
            };

            return _row(std::make_index_sequence<D1> {});
        }

        template <int I, int D1, int D2, typename T>
        vector_t<D1, T> col(const tensor_t<D1, D2, T> & A)
        {
            auto _col = [&A]<size_t... J>(std::index_sequence<J...>) -> vector_t<D1, T>
            {
                auto wrap = [&A]<size_t K>()->T { return A[{K, I}]; };
                return vector_t<D1, T>(wrap.template operator()<J>()...);
            };

            return _col(std::make_index_sequence<D2> {});
        }
    }
}

// end of file
