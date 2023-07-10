// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2023 all rights reserved
//

#if !defined(gsl_extension_pdf_h)
#define gsl_extension_pdf_h


// place everything in my private namespace
namespace gsl::pdf {
    // the uniform distribution
    namespace uniform {
        // sample
        extern const char * const sample__name__;
        extern const char * const sample__doc__;
        PyObject * sample(PyObject *, PyObject *);

        // density
        extern const char * const density__name__;
        extern const char * const density__doc__;
        PyObject * density(PyObject *, PyObject *);

        // fills
        extern const char * const vector__name__;
        extern const char * const vector__doc__;
        PyObject * vector(PyObject *, PyObject *);

        extern const char * const matrix__name__;
        extern const char * const matrix__doc__;
        PyObject * matrix(PyObject *, PyObject *);
    } // namespace uniform

    // the positive uniform distribution
    namespace uniform_pos {
        // sample
        extern const char * const sample__name__;
        extern const char * const sample__doc__;
        PyObject * sample(PyObject *, PyObject *);

        // fills
        extern const char * const vector__name__;
        extern const char * const vector__doc__;
        PyObject * vector(PyObject *, PyObject *);

        extern const char * const matrix__name__;
        extern const char * const matrix__doc__;
        PyObject * matrix(PyObject *, PyObject *);
    } // namespace uniform_pos

    // the gaussian distribution
    namespace gaussian {
        // sample
        extern const char * const sample__name__;
        extern const char * const sample__doc__;
        PyObject * sample(PyObject *, PyObject *);

        // density
        extern const char * const density__name__;
        extern const char * const density__doc__;
        PyObject * density(PyObject *, PyObject *);

        // fills
        extern const char * const vector__name__;
        extern const char * const vector__doc__;
        PyObject * vector(PyObject *, PyObject *);

        extern const char * const matrix__name__;
        extern const char * const matrix__doc__;
        PyObject * matrix(PyObject *, PyObject *);
    } // namespace gaussian

    // the ugaussian distribution
    namespace ugaussian {
        // sample
        extern const char * const sample__name__;
        extern const char * const sample__doc__;
        PyObject * sample(PyObject *, PyObject *);

        // density
        extern const char * const density__name__;
        extern const char * const density__doc__;
        PyObject * density(PyObject *, PyObject *);

        // fills
        extern const char * const vector__name__;
        extern const char * const vector__doc__;
        PyObject * vector(PyObject *, PyObject *);

        extern const char * const matrix__name__;
        extern const char * const matrix__doc__;
        PyObject * matrix(PyObject *, PyObject *);
    } // namespace ugaussian

    // the dirichlet distribution
    namespace dirichlet {
        // sample
        extern const char * const sample__name__;
        extern const char * const sample__doc__;
        PyObject * sample(PyObject *, PyObject *);

        // density
        extern const char * const density__name__;
        extern const char * const density__doc__;
        PyObject * density(PyObject *, PyObject *);

        // fills
        extern const char * const vector__name__;
        extern const char * const vector__doc__;
        PyObject * vector(PyObject *, PyObject *);

        extern const char * const matrix__name__;
        extern const char * const matrix__doc__;
        PyObject * matrix(PyObject *, PyObject *);
    } // namespace dirichlet

} // namespace gsl::pdf

#endif

// end of file
