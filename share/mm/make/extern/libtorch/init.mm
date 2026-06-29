# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved

# add to extern list unless already present
extern += ${if ${filter libtorch,$(extern)},,libtorch}

# # find my configuration file
libtorch.config := ${dir ${call extern.config,libtorch}}


# compiler flags
libtorch.flags ?=
# enable {libtorch} aware code
libtorch.defines ?= WITH_TORCH
# include path (PyTorch uses nested include/torch/csrc)
libtorch.incpath ?= $(libtorch.dir)/include $(libtorch.dir)/include/torch/csrc/api/include
# header marker(s): files that must resolve on {incpath}; absence proves breakage
libtorch.markers.headers ?= torch/torch.h

# linker flags
libtorch.ldflags ?=
# the canonical form of the lib directory
libtorch.libpath ?= $(libtorch.dir)/lib
# its rpath
libtorch.rpath = $(libtorch.libpath)
# set libtorch.cuda := 1 in the user config to link against a CUDA-enabled
# libtorch distribution (must contain libtorch_cuda.so and libc10_cuda.so)
libtorch.cuda ?=
libtorch.libraries ?= torch torch_cpu c10 ${if $(libtorch.cuda),torch_cuda c10_cuda,}

# my dependencies
libtorch.dependencies :=

# end of file
