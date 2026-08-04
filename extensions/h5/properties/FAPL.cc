// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// file access property lists
void
pyre::h5::py::properties::fapl(py::module & m)
{
    // add bindings for hdf5 file access property lists
    auto cls = py::class_<FAPL, PropList>(
        // in scope
        m,
        // class name
        "fapl",
        // docstring
        "a file access property list");

    // static properties
    cls.def_property_readonly_static(
        // the name
        "default",
        // the implementation
        [](const py::object &) -> const FAPL & {
            // easy enough
            return FAPL::theDefault();
        },
        // we hand back a reference to a shared, library-owned object
        py::return_value_policy::reference,
        // docstring
        "the default file access property list");

    // constructor
    cls.def(
        // the implementation
        py::init(),
        // the docstring
        "create a file access property list");

    // interface
    // the metadata block size
    cls.def_property(
        // the name
        "metaBlockSize",
        // the getter
        &FAPL::metaBlockSize,
        // the setter
        &FAPL::setMetaBlockSize,
        // the docstring
        "the size of the blocks my metadata is allocated in");

    // the page buffer characteristics
    cls.def_property(
        // the name
        "pageBufferSize",
        // the getter
        &FAPL::pageBufferSize,
        // the setter, which unpacks the {(bytes, metadata percent, raw percent)} triplet
        [](FAPL & self,
           const std::tuple<std::size_t, unsigned int, unsigned int> & buffer) -> void {
            // spread the triplet
            auto [bytes, meta, raw] = buffer;
            // and hand it to the property list
            self.setPageBufferSize(bytes, meta, raw);
            // all done
            return;
        },
        // the docstring
        "my page buffer, as {(bytes, metadata percent, raw data percent)}");

    // the alignment of objects in the file
    cls.def_property(
        // the name
        "alignment",
        // the getter
        &FAPL::alignment,
        // the setter, which unpacks the {(threshold, alignment)} pair
        [](FAPL & self, const std::tuple<hsize_t, hsize_t> & alignment) -> void {
            // spread the pair
            auto [threshold, boundary] = alignment;
            // and hand it to the property list
            self.setAlignment(threshold, boundary);
            // all done
            return;
        },
        // the docstring
        "where objects start in my file, as {(threshold, alignment)} bytes");

    // the sieve buffer
    cls.def_property(
        // the name
        "sieveBufferSize",
        // the getter
        &FAPL::sieveBufferSize,
        // the setter
        &FAPL::setSieveBufferSize,
        // the docstring
        "the size of the buffer that gathers small writes to contiguous datasets");

    // the file close degree
    cls.def_property(
        // the name
        "closeDegree",
        // the getter
        &FAPL::closeDegree,
        // the setter
        &FAPL::setCloseDegree,
        // the docstring
        "what becomes of my file when its handle closes with objects still open");

    // the default caches
    cls.def_property(
        // the name
        "cache",
        // the getter
        &FAPL::cache,
        // the setter, which unpacks the
        // {(metadata elements, chunk slots, chunk bytes, preemption)} quadruple
        [](FAPL & self,
           const std::tuple<int, std::size_t, std::size_t, double> & cache) -> void {
            // spread the quadruple
            auto [elements, slots, bytes, w0] = cache;
            // and hand it to the property list
            self.setCache(elements, slots, bytes, w0);
            // all done
            return;
        },
        // the docstring
        "my default caches, as {(metadata elements, chunk slots, chunk bytes, preemption)}");

    // the file format version bounds
    cls.def_property(
        // the name
        "libverBounds",
        // the getter
        &FAPL::libverBounds,
        // the setter, which unpacks the {(low, high)} pair
        [](FAPL & self, const std::tuple<H5F_libver_t, H5F_libver_t> & bounds) -> void {
            // spread the pair
            auto [low, high] = bounds;
            // and hand it to the property list
            self.setLibverBounds(low, high);
            // all done
            return;
        },
        // the docstring
        "the file format versions i may use, as {(low, high)}; asking for a recent one "
        "buys newer features and narrows who can read the result");

#if defined(H5_HAVE_ROS3_VFD)
    // populate the property list with ros3 parameters
    cls.def(
        // the name
        "ros3",
        // the implementation
        &FAPL::ros3,
        // the signature
        "authenticate"_a = true, "region"_a = "", "id"_a = "", "key"_a = "", "token"_a = "",
        // we hand back a reference to the list we just configured
        py::return_value_policy::reference,
        // the docstring
        "populate the property list with ros3 parameters");
#endif

    // all done
    return;
}


// end of file
