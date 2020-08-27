// -*- c++ -*-
//
// the pyre authors
// (c) 1998-2020 all rights reserved

// external support
#include "externals.h"
// get the forward declarations
#include "forward.h"
// type aliases
#include "api.h"

// global settings
#include "Chronicler.h"
// message contents
#include "Entry.h"

// renderer support
#include "Renderer.h"
#include "Memo.h"
#include "Alert.h"

// my superclass
#include "Device.h"
// my header
#include "Splitter.h"

// create a nonce name to satisfy the device constructor
// TODO permit anonymous devices?
static auto nonce()
{
    static int id = 0;
    return "Splitter" + std::to_string(id++);
}

pyre::journal::Splitter::
Splitter() :
    Device{nonce()}
{}

pyre::journal::Splitter::
Splitter(std::vector<output_t> o) :
    Device{nonce()},
    _outputs{o}
{}

// the interface simply forwards to the outputs' interfaces
auto
pyre::journal::Splitter::
memo(const entry_type & entry) -> Splitter &
{
    for (auto & output : outputs()) {
        output->memo(entry);
    }
    return *this;
}

auto
pyre::journal::Splitter::
alert(const entry_type & entry) -> Splitter &
{
    for (auto & output : outputs()) {
        output->alert(entry);
    }
    return *this;
}

// end of file
