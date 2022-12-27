// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_File_h)
#define pyre_journal_File_h


// a device that writes to output files
class pyre::journal::File : public Device {
    // types
public:
    // pointers to me
    using pointer_type = std::shared_ptr<File>;
    // for my data members
    using path_type = path_t;
    using file_type = filestream_t;
    using palette_type = palette_t;
    using renderer_type = renderer_t;
    using renderer_pointer = renderer_ptr;

    // metamethods
public:
    // constructor
    inline File(const path_type &, filemode_t = std::ios_base::out);
    // destructor
    virtual ~File();

    // accessors
public:
    inline auto path() const -> const path_type &;

    // interface
public:
    // user facing messages
    virtual auto alert(const entry_type &) -> File & override;
    // help screens
    virtual auto help(const entry_type &) -> File & override;
    // developer messages
    virtual auto memo(const entry_type &) -> File & override;

    // configuration data
protected:
    // the annotation palette
    palette_type _palette;

    // data
private:
    // my file name
    path_type _path;
    // the file to write to
    file_type _file;

    // the renderer for alerts
    renderer_pointer _alert;
    // help screens
    renderer_pointer _help;
    // and memos
    renderer_pointer _memo;

    // disallow
private:
    File(const File &) = delete;
    File(const File &&) = delete;
    const File & operator=(const File &) = delete;
    const File & operator=(const File &&) = delete;
};


// get the inline definitions
#define pyre_journal_File_icc
#include "File.icc"
#undef pyre_journal_File_icc


#endif

// end of file
