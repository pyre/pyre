// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// declarations
#include "FileMap.h"


// metamethods
// implementation details
// check and get info on the file backing an existing data product given its name
void
pyre::memory::FileMap::stat()
{
    // pull an old fashioned string out of the pathname
    auto filename = _uri.c_str();
    // find out what the filesystem knows about this file
    auto status = ::stat(filename, &_info);
    // if something went wrong
    if (status) {
        // make a channel
        pyre::journal::error_t channel("pyre.memory.map");
        // complain
        channel << pyre::journal::at() << "while looking for '" << _uri
                << "':" << pyre::journal::newline << "stat: error " << errno << ": "
                << std::strerror(errno) << pyre::journal::endl;
        // unreachable, unless the user has marked this error as non-fatal
        return;
    }

    // get the file size
    auto size = static_cast<size_type>(_info.st_size);
    // if the block would hold nothing, because it starts at or past the end of the file
    if (_offset >= size) {
        // make a channel
        pyre::journal::error_t channel("pyre.memory.map");
        // complain
        channel << pyre::journal::at() << "while looking for '" << _uri
                << "':" << pyre::journal::newline << "an offset of " << _offset
                << " bytes leaves nothing to map in a file that holds " << size << " bytes"
                << pyre::journal::endl;
        // unreachable, unless the user has marked this error as non-fatal
        return;
    }
    // the block is whatever the file holds past the offset
    _bytes = size - _offset;

    // all done
    return;
}


// create the backing file for a new data product given its name and size
void
pyre::memory::FileMap::create()
{
    // a product with no bytes cannot be mapped, so there is no point in making one
    if (_bytes == 0) {
        // make a channel
        pyre::journal::error_t channel("pyre.memory.map");
        // complain
        channel << pyre::journal::at() << "while creating '" << _uri
                << "':" << pyre::journal::newline
                << "a new data product must hold at least one byte" << pyre::journal::endl;
        // unreachable, unless the user has marked this error as non-fatal
        return;
    }

    // we take advantage of the POSIX requirement that writing past the end of a file
    // automatically fills all preceding locations with nulls
    // make a stream
    std::ofstream f(_uri, std::ofstream::binary);
    // move the file pointer to the desired location
    f.seekp(_bytes - 1);
    // make a byte
    char null = 0;
    // place it into the file
    f.write(&null, sizeof(null));
    // close the stream
    f.close();
    // all done
    return;
}


// create a file backed memory map, given the name and size of the file
void
pyre::memory::FileMap::map()
{
    // deduce the access mode
    auto mode = _writable ? O_RDWR : O_RDONLY;
    // open the file using the low level IO routine; we need its file descriptor
    auto fd = ::open(_uri.c_str(), mode);
    // if something went wrong
    if (fd < 0) {
        // make a channel
        pyre::journal::error_t channel("pyre.memory.map");
        // complain
        channel << pyre::journal::at() << "while mapping '" << _uri
                << "':" << pyre::journal::newline << "open: error " << errno << ": "
                << std::strerror(errno) << pyre::journal::endl;
        // unreachable, unless the user has marked this error as non-fatal
        return;
    }

    // derive the protection flag for the mapping
    auto protection = _writable ? (PROT_READ | PROT_WRITE) : PROT_READ;
    // a mapping must start on a page boundary, so start at the one at or before the offset
    auto page = static_cast<size_type>(::sysconf(_SC_PAGESIZE));
    // the bytes between that boundary and the start of the block
    auto slack = _offset % page;
    // the mapping runs from the boundary to the end of the file
    _extent = slack + _bytes;
    // map it
    _map = ::mmap(nullptr, _extent, protection, MAP_SHARED, fd, _offset - slack);
    // hold on to the error, if any, before closing the file descriptor can clobber it
    auto error = errno;
    // the mapping keeps its own reference to the file, so the descriptor is no longer needed
    ::close(fd);
    // if something went wrong
    if (_map == MAP_FAILED) {
        // make a channel
        pyre::journal::error_t channel("pyre.memory.map");
        // complain
        channel << pyre::journal::at() << "while mapping '" << _uri
                << "':" << pyre::journal::newline << "mmap: error " << error << ": "
                << std::strerror(error) << pyre::journal::endl;
        // unreachable, unless the user has marked this error as non-fatal
        return;
    }
    // the block starts past the slack
    _data = static_cast<std::byte *>(_map) + slack;

    // make a channel
    pyre::journal::debug_t channel("pyre.memory.map");
    // and report success
    channel << pyre::journal::at() << "with '" << _uri << "':" << pyre::journal::newline
            << "mapped " << _bytes << " bytes of " << (_writable ? "read/write" : "read only")
            << " memory at " << _data << pyre::journal::endl;

    // all done
    return;
}


// unmap file backed memory
void
pyre::memory::FileMap::unmap()
{
    // if we don't have a valid map
    if (_map == MAP_FAILED || _extent == 0) {
        // nothing to do
        return;
    }

    // otherwise, unmap, from the page boundary where the mapping starts
    auto status = ::munmap(_map, _extent);
    // if something went wrong
    if (status) {
        // make a channel
        pyre::journal::warning_t channel("pyre.memory.map");
        // complain
        channel << pyre::journal::at() << "while unmapping '" << _uri
                << "':" << pyre::journal::newline << "munmap: error " << errno << ": "
                << std::strerror(errno) << pyre::journal::endl;
    }

    // make a channel
    pyre::journal::debug_t channel("pyre.memory.map");
    // and report success
    channel << pyre::journal::at() << "with '" << _uri << "':" << pyre::journal::newline
            << "unmapped " << _bytes << " bytes of " << (_writable ? "read/write" : "read only")
            << " memory at " << _data << pyre::journal::endl;

    // invalidate the mapping
    _map = MAP_FAILED;
    _extent = 0;
    // the pointer
    _data = nullptr;
    // and the size
    _bytes = 0;

    // all done
    return;
}


// end of file
