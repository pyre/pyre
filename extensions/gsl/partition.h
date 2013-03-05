// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2013 all rights reserved
// 

#if !defined(gsl_extension_partition_h)
#define gsl_extension_partition_h


// place everything in my private namespace
namespace gsl {
    namespace mpi {

        // matrix gather
        extern const char * const gatherMatrix__name__;
        extern const char * const gatherMatrix__doc__;
        PyObject * gatherMatrix(PyObject *, PyObject *);

        // matrix scatter
        extern const char * const scatterMatrix__name__;
        extern const char * const scatterMatrix__doc__;
        PyObject * scatterMatrix(PyObject *, PyObject *);

        // matrix gather
        extern const char * const gatherVector__name__;
        extern const char * const gatherVector__doc__;
        PyObject * gatherVector(PyObject *, PyObject *);

        // matrix scatter
        extern const char * const scatterVector__name__;
        extern const char * const scatterVector__doc__;
        PyObject * scatterVector(PyObject *, PyObject *);

    } // of namespace mpi
} // of namespace gsl

#endif

// end of file
