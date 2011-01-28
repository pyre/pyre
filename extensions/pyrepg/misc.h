// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#if !defined(pypyrepg_misc_h)
#define pypyrepg_misc_h

// copyright note
const char * const pypyrepg_copyright__name__ = "copyright";
const char * const pypyrepg_copyright__doc__ = "the module copyright string";

extern "C"
PyObject * pypyrepg_copyright(PyObject *, PyObject *);

// version string
const char * const pypyrepg_version__name__ = "version";
const char * const pypyrepg_version__doc__ = "the module version string";

extern "C"
PyObject * pypyrepg_version(PyObject *, PyObject *);

#endif

// end of file
