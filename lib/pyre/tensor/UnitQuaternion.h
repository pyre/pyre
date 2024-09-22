// -*- C++ -*-
//
// bianca giovanardi
// (c) 1998-2024 all rights reserved
//


#if !defined(pyre_tensor_UnitQuaternion_h)
#define pyre_tensor_UnitQuaternion_h


namespace pyre::tensor {

    template <typename T>
    class UnitQuaternion {
    public:
        // my type
        using unit_quaternion_type = UnitQuaternion<T>;
        // my complex type
        using complex_type = T;
        // my real type
        using real_type = typename T::value_type;

    private:
        // my matrix representation type
        using matrix_representation_type = matrix_t<2, 2, T, pyre::grid::canonical_t<2>>;
        // representation type as a rotation matrix
        using rotation_matrix_type = matrix_t<3, 3, real_type, pyre::grid::canonical_t<2>>;
        // the axis type
        using rotation_axis_type = vector_t<3>;

    public:
        // constructor from four real arguments
        constexpr UnitQuaternion(real_type (&&)[4]);

        // constructor with an angle and an axis of rotation
        constexpr UnitQuaternion(const real_type &, const rotation_axis_type &);

        // copy constructor
        constexpr UnitQuaternion(const UnitQuaternion &) = default;

        // move constructor
        constexpr UnitQuaternion(UnitQuaternion &&) = default;

        // copy assignment operator
        constexpr UnitQuaternion & operator=(const UnitQuaternion &) = default;

        // move assignment operator
        constexpr UnitQuaternion & operator=(UnitQuaternion &&) = default;

        // destructor
        constexpr ~UnitQuaternion() = default;

    public:
        // get the rotation matrix associated with this quaternion
        constexpr auto rotation() const -> rotation_matrix_type;

        // get the rotation axis associated with this quaternion
        constexpr auto axis() const -> rotation_axis_type;

        // get the rotation angle associated with this quaternion
        constexpr auto angle() const -> real_type;

    private:
        // the components of the quaternion
        real_type _qr, _qi, _qj, _qk;

        // the matrix representation of the quaternion
        matrix_representation_type _matrix;
    };
} // namespace pyre::tensor


// get the inline definitions
#define pyre_tensor_UnitQuaternion_icc
#include "UnitQuaternion.icc"
#undef pyre_tensor_UnitQuaternion_icc


#endif

// end of file
