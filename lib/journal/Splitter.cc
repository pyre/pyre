// -*- c++ -*-
//
// the pyre authors
// (c) 1998-2023 all rights reserved

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
// MGA 20230429:
//   seems to me that anonymous devices would imply state that is not shareable
//   this is a change that i have contemplated for timers, where sometimes sharing is overkill
//   it would require some non-trivial restructuring of the implementation, since state sharing
//   is baked in rather deeply. worth thinking through...
static auto
nonce()
{
    static int id = 0;
    return "Splitter" + std::to_string(id++);
}

pyre::journal::Splitter::Splitter() : Device { nonce() } {}

pyre::journal::Splitter::Splitter(std::vector<output_t> o) : Device { nonce() }, _outputs { o } {}

void
pyre::journal::Splitter::attach(output_t output)
{
    outputs().push_back(output);
}

// the interface simply forwards to the outputs' interfaces
auto
pyre::journal::Splitter::alert(const entry_type & entry) -> Splitter &
{
    for (auto & output : outputs()) {
        output->alert(entry);
    }
    return *this;
}

auto
pyre::journal::Splitter::help(const entry_type & entry) -> Splitter &
{
    for (auto & output : outputs()) {
        output->alert(entry);
    }
    return *this;
}

auto
pyre::journal::Splitter::memo(const entry_type & entry) -> Splitter &
{
    for (auto & output : outputs()) {
        output->memo(entry);
    }
    return *this;
}

// end of file
