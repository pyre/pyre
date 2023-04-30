// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_Stream_h)
#define pyre_journal_Stream_h


// a device that writes to output streams

// N.B.: the constructor of this class keeps a reference to the stream you pass in; it's your
//    responsibility to make sure that your output stream outlives this device. Its use as a
//    base class by {Console} and {ErrorConsole} is correct since {std::cout} and {std::cerr}
//    are global objects with very long lives. Do not instantiate it with anything shorter
//    lived than a local variable in your {main}

class pyre::journal::Stream : public Device {
    // types
public:
    // pointers to me
    using pointer_type = std::shared_ptr<Stream>;

    using palette_type = palette_t;
    using stream_type = outputstream_t;
    using renderer_type = renderer_t;
    using renderer_pointer = renderer_ptr;

    // metamethods
public:
    // constructor
    inline Stream(const name_type &, stream_type &);
    // destructor
    virtual ~Stream();

    // interface
public:
    // user facing messages
    virtual auto alert(const entry_type &) -> Stream & override;
    // help messages
    virtual auto help(const entry_type &) -> Stream & override;
    // developer messages
    virtual auto memo(const entry_type &) -> Stream & override;

    // configuration data
protected:
    // the color palette
    palette_type _palette;

    // data
private:
    // the stream to write to
    stream_type & _stream;

    // the renderer for alerts
    renderer_pointer _alert;
    // help messages
    renderer_pointer _help;
    // and memos
    renderer_pointer _memo;

    // disallow
private:
    Stream(const Stream &) = delete;
    Stream(const Stream &&) = delete;
    const Stream & operator=(const Stream &) = delete;
    const Stream & operator=(const Stream &&) = delete;
};


// get the inline definitions
#define pyre_journal_Stream_icc
#include "Stream.icc"
#undef pyre_journal_Stream_icc


#endif

// end of file
