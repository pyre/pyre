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
matrix(::py::module & m)
{
    // register the Matrix type with DLPack support
    ::py::class_<pyre::gsl::Matrix>(m, "Matrix")
        .def(
            "__dlpack_device__",
            [](const pyre::gsl::Matrix &) {
                return ::py::make_tuple(static_cast<int>(kCPU.device_type), kCPU.device_id);
            })
        .def(
            "__dlpack__",
            [](::py::object self, ::py::object /*stream*/) -> ::py::object {
                pyre::gsl::Matrix & mat = self.cast<pyre::gsl::Matrix &>();
                struct Ctx {
                    int64_t shape[2];
                    int64_t strides[2];
                    DLManagedTensorVersioned managed;
                    PyObject * owner;
                };
                auto * ctx = new Ctx;
                ctx->shape[0]   = static_cast<int64_t>(mat.ptr->size1);
                ctx->shape[1]   = static_cast<int64_t>(mat.ptr->size2);
                // GSL matrices are row-major; tda is the leading dimension (stride of row)
                ctx->strides[0] = static_cast<int64_t>(mat.ptr->tda);
                ctx->strides[1] = 1;
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
                        mat.ptr->data,      // data
                        kCPU,               // device
                        2,                  // ndim
                        kFloat64,           // dtype
                        ctx->shape,         // shape
                        ctx->strides,       // strides
                        0                   // byte_offset
                    }
                };
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
            "return a DLPack tensor capsule (CPU, float64, row-major)");

    // register the MatrixView type
    ::py::class_<pyre::gsl::MatrixView>(m, "MatrixView");

    // allocate a matrix with the given dimensions
    m.def(
        "matrix_alloc",
        [](size_t rows, size_t cols) {
            return std::make_unique<pyre::gsl::Matrix>(rows, cols);
        },
        "rows"_a, "cols"_a,
        "allocate a matrix");

    // allocate a sub-matrix view; returns (MatrixView, non-owning Matrix)
    m.def(
        "matrix_view_alloc",
        [](pyre::gsl::Matrix & mat,
           size_t origin0, size_t origin1,
           size_t shape0,  size_t shape1) {
            // allocate view on heap; pybind11 manages via unique_ptr
            auto view = std::make_unique<pyre::gsl::MatrixView>(
                mat.ptr, origin0, origin1, shape0, shape1);
            // stable pointer to the embedded gsl_matrix inside the view
            gsl_matrix * mat_ptr = &view->view.matrix;
            // package both as Python objects
            ::py::object view_py = ::py::cast(std::move(view));
            ::py::object data_py = ::py::cast(std::make_unique<pyre::gsl::Matrix>(mat_ptr, false));
            // Python caller stores view_py in self.view (keeps view alive)
            return ::py::make_tuple(view_py, data_py);
        },
        "mat"_a, "origin0"_a, "origin1"_a, "shape0"_a, "shape1"_a,
        "allocate a matrix view");

    // set all elements to zero
    m.def(
        "matrix_zero",
        [](pyre::gsl::Matrix & mat) {
            gsl_matrix_set_zero(mat.ptr);
        },
        "mat"_a,
        "zero out the elements of a matrix");

    // fill with a constant value
    m.def(
        "matrix_fill",
        [](pyre::gsl::Matrix & mat, double value) {
            gsl_matrix_set_all(mat.ptr, value);
        },
        "mat"_a, "value"_a,
        "set all elements of a matrix to a value");

    // set to identity matrix
    m.def(
        "matrix_identity",
        [](pyre::gsl::Matrix & mat) {
            gsl_matrix_set_identity(mat.ptr);
        },
        "mat"_a,
        "set a matrix to the identity");

    // copy src into dst
    m.def(
        "matrix_copy",
        [](pyre::gsl::Matrix & dst, pyre::gsl::Matrix & src) {
            gsl_matrix_memcpy(dst.ptr, src.ptr);
        },
        "dst"_a, "src"_a,
        "build a copy of a matrix");

    // return the matrix as a tuple of tuples (row-major)
    m.def(
        "matrix_tuple",
        [](pyre::gsl::Matrix & mat) {
            ::py::tuple rows(mat.ptr->size1);
            for (size_t i = 0; i < mat.ptr->size1; ++i) {
                ::py::tuple row(mat.ptr->size2);
                for (size_t j = 0; j < mat.ptr->size2; ++j) {
                    row[j] = gsl_matrix_get(mat.ptr, i, j);
                }
                rows[i] = row;
            }
            return rows;
        },
        "mat"_a,
        "build a tuple of tuples out of a matrix");

    // read from a binary file
    m.def(
        "matrix_read",
        [](pyre::gsl::Matrix & mat, std::string filename) {
            std::FILE * f = std::fopen(filename.c_str(), "rb");
            if (!f) throw std::runtime_error("could not open file for reading: " + filename);
            gsl_matrix_fread(f, mat.ptr);
            std::fclose(f);
        },
        "mat"_a, "filename"_a,
        "read the values of a matrix from a binary file");

    // write to a binary file
    m.def(
        "matrix_write",
        [](pyre::gsl::Matrix & mat, std::string filename) {
            std::FILE * f = std::fopen(filename.c_str(), "wb");
            if (!f) throw std::runtime_error("could not open file for writing: " + filename);
            gsl_matrix_fwrite(f, mat.ptr);
            std::fclose(f);
        },
        "mat"_a, "filename"_a,
        "write the values of a matrix to a binary file");

    // read from a text file
    m.def(
        "matrix_scanf",
        [](pyre::gsl::Matrix & mat, std::string filename) {
            std::FILE * f = std::fopen(filename.c_str(), "r");
            if (!f) throw std::runtime_error("could not open file for reading: " + filename);
            gsl_matrix_fscanf(f, mat.ptr);
            std::fclose(f);
        },
        "mat"_a, "filename"_a,
        "read the values of a matrix from a text file");

    // write to a text file with a format string
    m.def(
        "matrix_printf",
        [](pyre::gsl::Matrix & mat, std::string filename, std::string format) {
            std::FILE * f = std::fopen(filename.c_str(), "w");
            if (!f) throw std::runtime_error("could not open file for writing: " + filename);
            gsl_matrix_fprintf(f, mat.ptr, format.c_str());
            std::fclose(f);
        },
        "mat"_a, "filename"_a, "format"_a,
        "write the values of a matrix to a file");

    // transpose in place
    m.def(
        "matrix_transpose",
        [](pyre::gsl::Matrix & mat) {
            gsl_matrix_transpose(mat.ptr);
        },
        "mat"_a,
        "transpose a matrix in place");

    // get an element; supports negative (cyclic) indices
    m.def(
        "matrix_get",
        [](pyre::gsl::Matrix & mat, ssize_t row, ssize_t col) {
            // reflect negative indices
            if (row < 0) row += (ssize_t)mat.ptr->size1;
            if (col < 0) col += (ssize_t)mat.ptr->size2;
            // bounds check
            if (row < 0 || (size_t)row >= mat.ptr->size1) {
                throw std::out_of_range("matrix row index out of range");
            }
            if (col < 0 || (size_t)col >= mat.ptr->size2) {
                throw std::out_of_range("matrix column index out of range");
            }
            return gsl_matrix_get(mat.ptr, (size_t)row, (size_t)col);
        },
        "mat"_a, "row"_a, "col"_a,
        "get the value of a matrix element");

    // set an element; supports negative (cyclic) indices
    m.def(
        "matrix_set",
        [](pyre::gsl::Matrix & mat, ssize_t row, ssize_t col, double value) {
            // reflect negative indices
            if (row < 0) row += (ssize_t)mat.ptr->size1;
            if (col < 0) col += (ssize_t)mat.ptr->size2;
            // bounds check
            if (row < 0 || (size_t)row >= mat.ptr->size1) {
                throw std::out_of_range("matrix row index out of range");
            }
            if (col < 0 || (size_t)col >= mat.ptr->size2) {
                throw std::out_of_range("matrix column index out of range");
            }
            gsl_matrix_set(mat.ptr, (size_t)row, (size_t)col, value);
        },
        "mat"_a, "row"_a, "col"_a, "value"_a,
        "set the value of a matrix element");

    // extract a column as a newly allocated vector
    m.def(
        "matrix_get_col",
        [](pyre::gsl::Matrix & mat, size_t col) {
            gsl_vector * v = gsl_vector_alloc(mat.ptr->size1);
            gsl_matrix_get_col(v, mat.ptr, col);
            return std::make_unique<pyre::gsl::Vector>(v, true);
        },
        "mat"_a, "col"_a,
        "get a column of a matrix as a vector");

    // extract a row as a newly allocated vector
    m.def(
        "matrix_get_row",
        [](pyre::gsl::Matrix & mat, size_t row) {
            gsl_vector * v = gsl_vector_alloc(mat.ptr->size2);
            gsl_matrix_get_row(v, mat.ptr, row);
            return std::make_unique<pyre::gsl::Vector>(v, true);
        },
        "mat"_a, "row"_a,
        "get a row of a matrix as a vector");

    // set a column from a vector
    m.def(
        "matrix_set_col",
        [](pyre::gsl::Matrix & mat, size_t col, pyre::gsl::Vector & v) {
            gsl_matrix_set_col(mat.ptr, col, v.ptr);
        },
        "matrix"_a, "col"_a, "vector"_a,
        "set a column of a matrix from a vector");

    // set a row from a vector
    m.def(
        "matrix_set_row",
        [](pyre::gsl::Matrix & mat, size_t row, pyre::gsl::Vector & v) {
            gsl_matrix_set_row(mat.ptr, row, v.ptr);
        },
        "matrix"_a, "row"_a, "vector"_a,
        "set a row of a matrix from a vector");

    // check whether a value appears in the matrix
    m.def(
        "matrix_contains",
        [](pyre::gsl::Matrix & mat, double value) {
            for (size_t i = 0; i < mat.ptr->size1; ++i) {
                for (size_t j = 0; j < mat.ptr->size2; ++j) {
                    if (gsl_matrix_get(mat.ptr, i, j) == value) return true;
                }
            }
            return false;
        },
        "mat"_a, "value"_a,
        "check whether a given value appears in a matrix");

    // return the maximum element
    m.def(
        "matrix_max",
        [](pyre::gsl::Matrix & mat) {
            return gsl_matrix_max(mat.ptr);
        },
        "mat"_a,
        "find the largest value contained in a matrix");

    // return the minimum element
    m.def(
        "matrix_min",
        [](pyre::gsl::Matrix & mat) {
            return gsl_matrix_min(mat.ptr);
        },
        "mat"_a,
        "find the smallest value contained in a matrix");

    // return (min, max) as a tuple
    m.def(
        "matrix_minmax",
        [](pyre::gsl::Matrix & mat) {
            double vmin, vmax;
            gsl_matrix_minmax(mat.ptr, &vmin, &vmax);
            return ::py::make_tuple(vmin, vmax);
        },
        "mat"_a,
        "find both the smallest and the largest value contained in a matrix");

    // element-wise equality check
    m.def(
        "matrix_equal",
        [](pyre::gsl::Matrix & m1, pyre::gsl::Matrix & m2) {
            return static_cast<bool>(gsl_matrix_equal(m1.ptr, m2.ptr));
        },
        "m1"_a, "m2"_a,
        "check two matrices for equality");

    // in-place addition
    m.def(
        "matrix_add",
        [](pyre::gsl::Matrix & mat, pyre::gsl::Matrix & other) {
            gsl_matrix_add(mat.ptr, other.ptr);
        },
        "mat"_a, "other"_a,
        "in-place addition of two matrices");

    // in-place subtraction
    m.def(
        "matrix_sub",
        [](pyre::gsl::Matrix & mat, pyre::gsl::Matrix & other) {
            gsl_matrix_sub(mat.ptr, other.ptr);
        },
        "mat"_a, "other"_a,
        "in-place subtraction of two matrices");

    // in-place element-wise multiplication
    m.def(
        "matrix_mul",
        [](pyre::gsl::Matrix & mat, pyre::gsl::Matrix & other) {
            gsl_matrix_mul_elements(mat.ptr, other.ptr);
        },
        "mat"_a, "other"_a,
        "in-place element-wise multiplication of two matrices");

    // in-place element-wise division
    m.def(
        "matrix_div",
        [](pyre::gsl::Matrix & mat, pyre::gsl::Matrix & other) {
            gsl_matrix_div_elements(mat.ptr, other.ptr);
        },
        "mat"_a, "other"_a,
        "in-place element-wise division of two matrices");

    // add a constant to all elements
    m.def(
        "matrix_shift",
        [](pyre::gsl::Matrix & mat, double value) {
            gsl_matrix_add_constant(mat.ptr, value);
        },
        "mat"_a, "value"_a,
        "in-place addition of a constant to a matrix");

    // scale all elements by a constant
    m.def(
        "matrix_scale",
        [](pyre::gsl::Matrix & mat, double value) {
            gsl_matrix_scale(mat.ptr, value);
        },
        "mat"_a, "value"_a,
        "in-place scaling of a matrix by a constant");

    // symmetric eigenvalue decomposition
    m.def(
        "matrix_eigen_symmetric",
        [](pyre::gsl::Matrix & mat) {
            size_t n = mat.ptr->size1;
            // allocate eigenvalue vector and eigenvector matrix
            gsl_vector * eval = gsl_vector_alloc(n);
            gsl_matrix * evec = gsl_matrix_alloc(n, n);
            // allocate the workspace
            gsl_eigen_symmv_workspace * w = gsl_eigen_symmv_alloc(n);
            // compute
            gsl_eigen_symmv(mat.ptr, eval, evec, w);
            // free the workspace
            gsl_eigen_symmv_free(w);
            // sort by eigenvalue descending
            gsl_eigen_symmv_sort(eval, evec, GSL_EIGEN_SORT_VAL_DESC);
            // wrap results and return as a tuple
            return ::py::make_tuple(
                std::make_unique<pyre::gsl::Vector>(eval, true),
                std::make_unique<pyre::gsl::Matrix>(evec, true));
        },
        "mat"_a,
        "compute the eigenvalues and eigenvectors of a real symmetric matrix");

    // return a numpy array view of the matrix data; keep Matrix alive via its Python object
    m.def(
        "matrix_ndarray",
        [](::py::object mat_obj) {
            pyre::gsl::Matrix & mat = mat_obj.cast<pyre::gsl::Matrix &>();
            // require contiguous storage
            if (mat.ptr->tda != mat.ptr->size2) {
                throw ::py::value_error("matrix is not contiguous: tda != size2");
            }
            return ::py::array_t<double>(
                { mat.ptr->size1, mat.ptr->size2 },
                { mat.ptr->tda * sizeof(double), sizeof(double) },
                mat.ptr->data,
                mat_obj);
        },
        "mat"_a,
        "return a numpy array view of a matrix");
}

} // namespace pyre::gsl::py

// end of file
