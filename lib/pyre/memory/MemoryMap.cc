// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// portability
#include <portinfo>
// externals
#include <fstream>
// low level stuff
#include <cstring> // for strerror
#include <fcntl.h> // for open
#include <unistd.h> // for close
#include <sys/stat.h> // for the mode flags
#include <sys/mman.h> // for mmap

// my parts
#include "public.h"

// class methods
// make a file of a specified size
void
pyre::memory::MemoryMap::
create(uri_type name, size_type size) {
    // we take advantage of the POSIX requirement that writing a byte at a file location past its
    // current size automatically fills all the locations before it with nulls

    // create a file stream
    std::ofstream file(name, std::ofstream::binary);
    // move the file pointer to the desired size
    file.seekp(size - 1);
    // make a byte
    char null = 0;
    // write a byte
    file.write(&null, sizeof(null));
    // close the stream
    file.close();

    // make a channel
    pyre::journal::debug_t channel("pyre.memory.direct");
    // show me
    channel
        << pyre::journal::at(__HERE__)
        << "created '" << name << "' (" << size << " bytes)"
        << pyre::journal::endl;

    // all done
    return;
}

// memory map the given file
void *
pyre::memory::MemoryMap::
map(uri_type name, size_type & size, offset_type offset, bool writable) {
    // deduce the mode for opening the file
    auto mode = writable ? O_RDWR : O_RDONLY;
    // open the file using low level IO, since we need its file descriptor
    auto fd = ::open(name.c_str(), mode);
    // verify the file was opened correctly
    if (fd < 0) {
        // and if not, create a channel
        pyre::journal::error_t channel("pyre.memory.direct");
        // complain
        channel
            // where
            << pyre::journal::at(__HERE__)
            // what happened
            << "while opening '" << name << "'" << pyre::journal::newline
            // why it happened
            << "  reason " << errno << ": " << std::strerror(errno)
            // flush
            << pyre::journal::endl;
            // raise an exception
        throw std::runtime_error(std::strerror(errno));
    }

    // if the {size} argument is 0, interpret it as a request to map the entire file; let's ask
    // the OS for the size of the file
    if (size == entireFile) {
        // allocate space for a {stat} buffer
        struct stat info;
        // fill it with what the OS knows about the file
        auto flag = ::fstat(fd, &info);
        // if we were unable to get file information
        if (flag) {
            // create a channel
            pyre::journal::error_t channel("pyre.memory.direct");
            // complain
            channel
                // where
                << pyre::journal::at(__HERE__)
                // what happened
                << "while querying '" << name << "'" << pyre::journal::newline
                // why it happened
                << "  reason " << errno << ": " << std::strerror(errno)
                // flush
                << pyre::journal::endl;
            // raise an exception
            throw std::runtime_error(std::strerror(errno));
        }
        // the {info} structure is now full of useful information, including the file size in bytes
        size = info.st_size;
    }

    // deduce the protection flag
    auto prot = writable ? (PROT_READ | PROT_WRITE) : PROT_READ;
    // map it
    void * buffer = ::mmap(0, size, prot, MAP_SHARED, fd, offset);
    // check it
    if (buffer == MAP_FAILED) {
        // create a channel
        pyre::journal::error_t channel("pyre.memory.direct");
        // complain
        channel
            // where
            << pyre::journal::at(__HERE__)
            // what happened
            << "failed to map '" << name << "' onto memory (" << size << " bytes)"
            << pyre::journal::newline
            // why it happened
            << "  reason " << errno << ": " << std::strerror(errno)
            // flush
            << pyre::journal::endl;
        // raise an exception
        throw std::bad_alloc();
    }

    // make a channel
    pyre::journal::debug_t channel("pyre.memory.direct");
    // show me
    channel
        << pyre::journal::at(__HERE__)
        << "mapped '" << name << "' into memory at " << buffer
        << pyre::journal::endl;

    // clean up
    // close the file
    close(fd);
    // return the payload
    return buffer;
}


// unmap the given buffer
void
pyre::memory::MemoryMap::
unmap(const void * buffer, size_type size) {
    // unmap
    int status = ::munmap(const_cast<void *>(buffer), size);

    // make a channel
    pyre::journal::debug_t channel("pyre.memory.direct");
    // show me
    channel
        << pyre::journal::at(__HERE__)
        << "unmapped " << size << " bytes from " << buffer
        << pyre::journal::endl;

    // check whether the memory was unmapped
    if (status) {
        // make a channel
        pyre::journal::error_t error("pyre.memory.direct");
        // complain
        error
            << pyre::journal::at(__HERE__)
            << "error " << errno << ": " << std::strerror(errno)
            << pyre::journal::endl;
    }

    // all done
    return;
}

// end of file
