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
#include <sstream>
// my parts
#include "public.h"

// meta-methods
pyre::memory::MemoryMap::
MemoryMap(uri_type uri, size_type size) :
    _uri {uri},
    _info {}
{
    // if no filename were given
    if (uri.empty()) {
        // nothing further to do
        return;
    }

    // otherwise, ask the file system for what known about it
    int status = ::stat(_uri.data(), &_info);
    // if this failed
    if (status) {
        // the only case we handle is the file not existing; complain about everything else
        if (errno != ENOENT) {
            // create a channel
            pyre::journal::error_t channel("pyre.memory.direct");
            // complain
            channel
                // where
                << pyre::journal::at(__HERE__)
                // what happened
                << "while opening '" << _uri << "'" << pyre::journal::newline
                // why it happened
                << "  reason " << errno << ": " << std::strerror(errno)
                // flush
                << pyre::journal::endl;
            // raise an exception
            throw std::system_error(errno, std::system_category());
        }
        // so, the file doesn't exist; if the caller did not specify a desired map size
        if (size == 0) {
            // we have a problem
            std::stringstream problem;
            // describe it
            problem << "while creating '" << uri << "': unknown size";
            // create a channel
            pyre::journal::error_t channel("pyre.memory.direct");
            // complain
            channel
                // where
                << pyre::journal::at(__HERE__)
                // what happened
                << problem.str()
                // flush
                << pyre::journal::endl;
            // raise an exception
            throw std::runtime_error(problem.str());
        }
        // if we have size information, create the file
        create(uri, size);
        // and get the file information
        ::stat(_uri.data(), &_info);
    }

    // all done
    return;
}


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
map(uri_type name, size_type & size, size_type offset, bool writable) {
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
        throw std::system_error(errno, std::system_category());
    }

    // deduce the protection flag
    auto prot = writable ? (PROT_READ | PROT_WRITE) : PROT_READ;
    // map it
    void * buffer = ::mmap(0, size, prot, MAP_SHARED, fd, static_cast<offset_t>(offset));
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
