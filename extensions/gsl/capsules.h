// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2023 all rights reserved
//

#if !defined(gsl_extension_capsules_h)
#define gsl_extension_capsules_h

// capsules
namespace gsl {

    // histogram
    namespace histogram {
        const char * const capsule_t = "gsl.histogram";
        void free(PyObject *);
    } // namespace histogram
    // matrix
    namespace matrix {
        const char * const capsule_t = "gsl.matrix";
        const char * const view_t = "gsl.matrix.view";
        void free(PyObject *);
        void freeview(PyObject *);
    } // namespace matrix
    // rng
    namespace rng {
        const char * const capsule_t = "gsl.rng";
        void free(PyObject *);
    } // namespace rng
    // permutations
    namespace permutation {
        const char * const capsule_t = "gsl.permutation";
        void free(PyObject *);
    } // namespace permutation
    // vectors
    namespace vector {
        const char * const capsule_t = "gsl.vector";
        const char * const view_t = "gsl.vector.view";
        void free(PyObject *);
        void freeview(PyObject *);
    } // namespace vector
} // namespace gsl
// local

#endif

// end of file
