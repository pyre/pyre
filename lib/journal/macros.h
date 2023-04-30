// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_macros_h)
#define pyre_journal_macros_h


// define __HERE__, which has to be a preprocessor macro
// c++20 has <source_location>, so this will soon be obsolete

// used by the locator to communicate the source of a message
#define __HERE__ __FILE__,__LINE__,__func__
// used for the C/FORTRAN bindings
#define __HERE_ARGS__ filename, lineno, funcname
#define __HERE_DECL__ const char * filename, long lineno, const char * funcname


#endif

// end of file
