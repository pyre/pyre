// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// code guard
#if !defined(pyre_memory_public_h)
#define pyre_memory_public_h

// externals
#include <stdexcept>
#include <fstream>
#include <utility>
// low level stuff
#include <cstring> // for strerror
#include <fcntl.h> // for open
#include <unistd.h> // for close
#include <sys/stat.h> // for the mode flags
#include <sys/mman.h> // for mmap
// support
#include <pyre/journal.h>

// forward declarations
namespace pyre {
    namespace memory {
        // local type aliases
        // for filenames
        typedef std::string uri_t;
        // for describing shapes and regions
        typedef off_t offset_t;
        typedef std::size_t size_t;
        // file information
        typedef struct stat info_t;

        class MemoryMap; // infrastructure

        // buffer types
        typedef class View view_t;               // view over existing memory
        typedef class ConstView constview_t;     // view over existing constant memory
        typedef class Heap heap_t;               // dynamically allocated memory
        typedef class Direct direct_t;           // memory mapped file
        typedef class ConstDirect constdirect_t; // const access to a memory mapped file
    }
}

// the object model
#include "View.h"
#include "ConstView.h"
#include "Heap.h"
#include "MemoryMap.h"
#include "Direct.h"
#include "ConstDirect.h"

// the implementations
// views over existing memory
#define pyre_memory_View_icc
#include "View.icc"
#undef pyre_memory_View_icc

// views over existing const memory
#define pyre_memory_ConstView_icc
#include "ConstView.icc"
#undef pyre_memory_ConstView_icc

// dynamically allocated memory
#define pyre_memory_Heap_icc
#include "Heap.icc"
#undef pyre_memory_Heap_icc

// support for memory backed by files
#define pyre_memory_MemoryMap_icc
#include "MemoryMap.icc"
#undef pyre_memory_MemoryMap_icc

#define pyre_memory_Direct_icc
#include "Direct.icc"
#undef pyre_memory_Direct_icc

#define pyre_memory_ConstDirect_icc
#include "ConstDirect.icc"
#undef pyre_memory_ConstDirect_icc

#endif

// end of file
