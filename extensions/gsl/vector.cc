// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// externals
#include "external.h"
// dlpack
#include "dlpack.h"


namespace pyre::gsl::py {

void
vector(::py::module & m)
{
    // register the Vector type with DLPack support
    ::py::class_<pyre::gsl::Vector>(m, "Vector")
        .def(
            "__dlpack_device__",
            [](const pyre::gsl::Vector &) {
                return ::py::make_tuple(static_cast<int>(kCPU.device_type), kCPU.device_id);
            })
        .def(
            "__dlpack__",
            [](::py::object self, ::py::object /*stream*/) -> ::py::object {
                pyre::gsl::Vector & v = self.cast<pyre::gsl::Vector &>();
                // heap-allocate context: shape, strides, versioned managed tensor, owner
                struct Ctx {
                    int64_t shape[1];
                    int64_t strides[1];
                    DLManagedTensorVersioned managed;
                    PyObject * owner;   // keeps the Vector Python object alive
                };
                auto * ctx = new Ctx;
                ctx->shape[0]   = static_cast<int64_t>(v.ptr->size);
                ctx->strides[0] = static_cast<int64_t>(v.ptr->stride);
                Py_INCREF(self.ptr());
                ctx->owner = self.ptr();
                ctx->managed = DLManagedTensorVersioned {
                    { 1, 0 },               // version: major=1, minor=0
                    ctx,                    // manager_ctx
                    [](DLManagedTensorVersioned * mt) {
                        auto * c = static_cast<Ctx *>(mt->manager_ctx);
                        Py_DECREF(c->owner);
                        delete c;
                    },
                    0,                      // flags: 0 = writable
                    DLTensor {
                        v.ptr->data,        // data
                        kCPU,               // device
                        1,                  // ndim
                        kFloat64,           // dtype
                        ctx->shape,         // shape
                        ctx->strides,       // strides
                        0                   // byte_offset
                    }
                };
                // capsule destructor: only call deleter if not yet consumed by numpy
                PyObject * cap = PyCapsule_New(&ctx->managed, "dltensor_versioned",
                    [](PyObject * pycap) {
                        if (!PyCapsule_IsValid(pycap, "dltensor_versioned")) return;
                        auto * mt = static_cast<DLManagedTensorVersioned *>(
                            PyCapsule_GetPointer(pycap, "dltensor_versioned"));
                        if (mt && mt->deleter) mt->deleter(mt);
                    });
                if (!cap) {
                    Py_DECREF(ctx->owner);
                    delete ctx;
                    throw ::py::error_already_set();
                }
                return ::py::reinterpret_steal<::py::object>(cap);
            },
            ::py::arg("stream") = ::py::none(),
            "return a DLPack tensor capsule (CPU, float64)");

    // register the VectorView type
    ::py::class_<pyre::gsl::VectorView>(m, "VectorView");

    // allocate a vector of size n
    m.def(
        "vector_alloc",
        [](size_t n) {
            return std::make_unique<pyre::gsl::Vector>(n);
        },
        "n"_a,
        "allocate a vector");

    // allocate a sub-vector view; returns (VectorView, non-owning Vector)
    m.def(
        "vector_view_alloc",
        [](pyre::gsl::Vector & v, size_t origin, size_t shape) {
            // allocate view on heap; pybind11 manages via unique_ptr
            auto view = std::make_unique<pyre::gsl::VectorView>(v.ptr, origin, shape);
            // stable pointer to the embedded gsl_vector inside the view
            gsl_vector * vec_ptr = &view->view.vector;
            // package both as Python objects
            ::py::object view_py = ::py::cast(std::move(view));
            ::py::object data_py = ::py::cast(std::make_unique<pyre::gsl::Vector>(vec_ptr, false));
            // Python caller stores view_py in self.view (keeps view alive)
            return ::py::make_tuple(view_py, data_py);
        },
        "v"_a, "origin"_a, "shape"_a,
        "allocate a vector view");

    // set all elements to zero
    m.def(
        "vector_zero",
        [](pyre::gsl::Vector & v) {
            gsl_vector_set_zero(v.ptr);
        },
        "v"_a,
        "zero out the elements of a vector");

    // fill with a constant value
    m.def(
        "vector_fill",
        [](pyre::gsl::Vector & v, double value) {
            gsl_vector_set_all(v.ptr, value);
        },
        "v"_a, "value"_a,
        "set all elements of a vector to a value");

    // build a basis vector (all zeros except at index)
    m.def(
        "vector_basis",
        [](pyre::gsl::Vector & v, size_t index) {
            gsl_vector_set_basis(v.ptr, index);
        },
        "v"_a, "index"_a,
        "build a basis vector");

    // copy src into dst
    m.def(
        "vector_copy",
        [](pyre::gsl::Vector & dst, pyre::gsl::Vector & src) {
            gsl_vector_memcpy(dst.ptr, src.ptr);
        },
        "dst"_a, "src"_a,
        "build a copy of a vector");

    // return the vector as a python tuple
    m.def(
        "vector_tuple",
        [](pyre::gsl::Vector & v) {
            ::py::tuple result(v.ptr->size);
            for (size_t i = 0; i < v.ptr->size; ++i) {
                result[i] = gsl_vector_get(v.ptr, i);
            }
            return result;
        },
        "v"_a,
        "build a tuple out of a vector");

    // read from a binary file
    m.def(
        "vector_read",
        [](pyre::gsl::Vector & v, std::string filename) {
            std::FILE * f = std::fopen(filename.c_str(), "rb");
            if (!f) throw std::runtime_error("could not open file for reading: " + filename);
            gsl_vector_fread(f, v.ptr);
            std::fclose(f);
        },
        "v"_a, "filename"_a,
        "read the values of a vector from a binary file");

    // write to a binary file
    m.def(
        "vector_write",
        [](pyre::gsl::Vector & v, std::string filename) {
            std::FILE * f = std::fopen(filename.c_str(), "wb");
            if (!f) throw std::runtime_error("could not open file for writing: " + filename);
            gsl_vector_fwrite(f, v.ptr);
            std::fclose(f);
        },
        "v"_a, "filename"_a,
        "write the values of a vector to a binary file");

    // read from a text file
    m.def(
        "vector_scanf",
        [](pyre::gsl::Vector & v, std::string filename) {
            std::FILE * f = std::fopen(filename.c_str(), "r");
            if (!f) throw std::runtime_error("could not open file for reading: " + filename);
            gsl_vector_fscanf(f, v.ptr);
            std::fclose(f);
        },
        "v"_a, "filename"_a,
        "read the values of a vector from a text file");

    // write to a text file with a format string
    m.def(
        "vector_printf",
        [](pyre::gsl::Vector & v, std::string filename, std::string format) {
            std::FILE * f = std::fopen(filename.c_str(), "w");
            if (!f) throw std::runtime_error("could not open file for writing: " + filename);
            gsl_vector_fprintf(f, v.ptr, format.c_str());
            std::fclose(f);
        },
        "v"_a, "filename"_a, "format"_a,
        "write the values of a vector to a file");

    // get an element; supports negative indices
    m.def(
        "vector_get",
        [](pyre::gsl::Vector & v, long index) {
            // reflect negative indices about the end of the vector
            if (index < 0) index += static_cast<long>(v.ptr->size);
            if (index < 0 || static_cast<size_t>(index) >= v.ptr->size) {
                throw ::py::index_error("vector index out of range");
            }
            return gsl_vector_get(v.ptr, static_cast<size_t>(index));
        },
        "v"_a, "index"_a,
        "get the value of a vector element");

    // set an element; supports negative indices
    m.def(
        "vector_set",
        [](pyre::gsl::Vector & v, long index, double value) {
            // reflect negative indices about the end of the vector
            if (index < 0) index += static_cast<long>(v.ptr->size);
            if (index < 0 || static_cast<size_t>(index) >= v.ptr->size) {
                throw ::py::index_error("vector index out of range");
            }
            gsl_vector_set(v.ptr, static_cast<size_t>(index), value);
        },
        "v"_a, "index"_a, "value"_a,
        "set the value of a vector element");

    // check whether a value appears in the vector
    m.def(
        "vector_contains",
        [](pyre::gsl::Vector & v, double value) {
            for (size_t i = 0; i < v.ptr->size; ++i) {
                if (gsl_vector_get(v.ptr, i) == value) return true;
            }
            return false;
        },
        "v"_a, "value"_a,
        "check whether a given value appears in a vector");

    // return the maximum element
    m.def(
        "vector_max",
        [](pyre::gsl::Vector & v) {
            return gsl_vector_max(v.ptr);
        },
        "v"_a,
        "find the largest value contained in a vector");

    // return the minimum element
    m.def(
        "vector_min",
        [](pyre::gsl::Vector & v) {
            return gsl_vector_min(v.ptr);
        },
        "v"_a,
        "find the smallest value contained in a vector");

    // return (min, max) as a tuple
    m.def(
        "vector_minmax",
        [](pyre::gsl::Vector & v) {
            double vmin, vmax;
            gsl_vector_minmax(v.ptr, &vmin, &vmax);
            return ::py::make_tuple(vmin, vmax);
        },
        "v"_a,
        "find both the smallest and the largest value contained in a vector");

    // element-wise equality check
    m.def(
        "vector_equal",
        [](pyre::gsl::Vector & v1, pyre::gsl::Vector & v2) {
            return static_cast<bool>(gsl_vector_equal(v1.ptr, v2.ptr));
        },
        "v1"_a, "v2"_a,
        "check two vectors for equality");

    // in-place addition
    m.def(
        "vector_add",
        [](pyre::gsl::Vector & v, pyre::gsl::Vector & u) {
            gsl_vector_add(v.ptr, u.ptr);
        },
        "v"_a, "other"_a,
        "in-place addition of two vectors");

    // in-place subtraction
    m.def(
        "vector_sub",
        [](pyre::gsl::Vector & v, pyre::gsl::Vector & u) {
            gsl_vector_sub(v.ptr, u.ptr);
        },
        "v"_a, "other"_a,
        "in-place subtraction of two vectors");

    // in-place element-wise multiplication
    m.def(
        "vector_mul",
        [](pyre::gsl::Vector & v, pyre::gsl::Vector & u) {
            gsl_vector_mul(v.ptr, u.ptr);
        },
        "v"_a, "other"_a,
        "in-place multiplication of two vectors");

    // in-place element-wise division
    m.def(
        "vector_div",
        [](pyre::gsl::Vector & v, pyre::gsl::Vector & u) {
            gsl_vector_div(v.ptr, u.ptr);
        },
        "v"_a, "other"_a,
        "in-place division of two vectors");

    // add a constant to all elements
    m.def(
        "vector_shift",
        [](pyre::gsl::Vector & v, double value) {
            gsl_vector_add_constant(v.ptr, value);
        },
        "v"_a, "value"_a,
        "in-place addition of a constant to a vector");

    // scale all elements by a constant
    m.def(
        "vector_scale",
        [](pyre::gsl::Vector & v, double value) {
            gsl_vector_scale(v.ptr, value);
        },
        "v"_a, "value"_a,
        "in-place scaling of a vector by a constant");

    // sort in place
    m.def(
        "vector_sort",
        [](pyre::gsl::Vector & v) {
            gsl_sort_vector(v.ptr);
        },
        "v"_a,
        "in-place sort the elements of a vector");

    // sort and return the permutation index
    m.def(
        "vector_sortIndex",
        [](pyre::gsl::Vector & v) {
            gsl_permutation * p = gsl_permutation_alloc(v.ptr->size);
            gsl_sort_vector_index(p, v.ptr);
            return std::make_unique<pyre::gsl::Permutation>(p, true);
        },
        "v"_a,
        "construct the permutation that would sort the elements of a vector");

    // compute the mean; optionally weighted
    m.def(
        "vector_mean",
        [](pyre::gsl::Vector & v, ::py::object weights) {
            if (weights.is_none()) {
                return gsl_stats_mean(v.ptr->data, v.ptr->stride, v.ptr->size);
            }
            pyre::gsl::Vector & w = weights.cast<pyre::gsl::Vector &>();
            return gsl_stats_wmean(w.ptr->data, w.ptr->stride,
                                   v.ptr->data, v.ptr->stride, v.ptr->size);
        },
        "v"_a, "weights"_a = ::py::none(),
        "compute the mean of the elements of a vector");

    // compute the median from sorted data
    m.def(
        "vector_median",
        [](pyre::gsl::Vector & v) {
            return gsl_stats_median_from_sorted_data(v.ptr->data, v.ptr->stride, v.ptr->size);
        },
        "v"_a,
        "compute the median of the elements of a pre-sorted vector");

    // compute the variance; optionally with a provided mean
    m.def(
        "vector_variance",
        [](pyre::gsl::Vector & v, ::py::object mean) {
            if (mean.is_none()) {
                return gsl_stats_variance(v.ptr->data, v.ptr->stride, v.ptr->size);
            }
            return gsl_stats_variance_m(v.ptr->data, v.ptr->stride, v.ptr->size,
                                        mean.cast<double>());
        },
        "v"_a, "mean"_a = ::py::none(),
        "compute the variance of the elements of a vector");

    // compute the standard deviation; optionally with a provided mean
    m.def(
        "vector_sdev",
        [](pyre::gsl::Vector & v, ::py::object mean) {
            if (mean.is_none()) {
                return gsl_stats_sd(v.ptr->data, v.ptr->stride, v.ptr->size);
            }
            return gsl_stats_sd_m(v.ptr->data, v.ptr->stride, v.ptr->size, mean.cast<double>());
        },
        "v"_a, "mean"_a = ::py::none(),
        "compute the standard deviation of the elements of a vector");

    // shuffle the vector in place using a random number generator
    m.def(
        "vector_shuffle",
        [](pyre::gsl::RNG & rng, pyre::gsl::Vector & v) {
            gsl_ran_shuffle(rng.ptr, v.ptr->data, v.ptr->size, sizeof(double));
        },
        "rng"_a, "v"_a,
        "shuffle a vector to a random order");

    // return a numpy array view of the vector data; keep the Vector alive via its Python object
    m.def(
        "vector_ndarray",
        [](::py::object v_obj) {
            pyre::gsl::Vector & v = v_obj.cast<pyre::gsl::Vector &>();
            return ::py::array_t<double>(
                { v.ptr->size },
                { v.ptr->stride * sizeof(double) },
                v.ptr->data,
                v_obj);
        },
        "v"_a,
        "return a numpy array view of a vector");
}

} // namespace pyre::gsl::py

// end of file
