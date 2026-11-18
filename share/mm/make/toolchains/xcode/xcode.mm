# -*- makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# xcode: apple's developer tools, which build swift code, assemble app bundles for macOS and iOS,
# sign them and drive the simulator. apple distributes them, so mm only locates them and verifies
# that what a build needs is present. every tool is reached through {xcrun}, which picks it out of
# the active developer directory and, given {--sdk}, points it at the sdk of a platform
toolchain.xcode.doc := "apple's developer tools: swift, sdks, bundles, signing (vendor-installed)"
toolchain.xcode.kind := vendor
toolchain.xcode.url := https://developer.apple.com/xcode/
toolchain.xcode.cli := xcrun

# the developer directory of the xcode installation to use; when left empty, the tools come from
# the one the environment selects, through {DEVELOPER_DIR} or {xcode-select}. the command line
# tools alone carry neither the ios sdks nor the bundle and simulator tools, so a machine whose
# environment selects them names its xcode here, e.g. /Applications/Xcode.app/Contents/Developer
toolchain.xcode.developer ?=
# the environment every tool runs in: the chosen developer directory, when there is one
toolchain.xcode.env = ${if $(toolchain.xcode.developer),DEVELOPER_DIR=$(toolchain.xcode.developer),}

# the tools a build needs; each one is looked up without being run, since the first run of some of
# them installs components of a freshly updated xcode
toolchain.xcode.tools ?= swiftc actool codesign simctl
# the platforms whose sdks a build needs
toolchain.xcode.platforms ?= macosx iphoneos iphonesimulator

# xcode is not version-pinned, so report the installed release; lazy, so the shell runs only when
# a recipe asks for it
toolchain.xcode.version = \
    $(shell $(toolchain.xcode.env) $(toolchain.xcode.cli) xcodebuild -version 2>/dev/null | head -1)
# the location and the version of the sdk of a platform
#   usage: toolchain.xcode.sdk {platform}
toolchain.xcode.sdk = \
    $(shell $(toolchain.xcode.env) $(toolchain.xcode.cli) --sdk $(1) --show-sdk-path 2>/dev/null)
toolchain.xcode.sdk.version = \
    $(shell $(toolchain.xcode.env) $(toolchain.xcode.cli) --sdk $(1) --show-sdk-version 2>/dev/null)
# the app that shows simulated and attached devices in a window; it ships inside xcode, beside
# the developer directory
toolchain.xcode.devicehub = \
    ${abspath $(shell $(toolchain.xcode.env) xcode-select -p 2>/dev/null)/../Applications/DeviceHub.app}


# report the developer directory, the device window and the sdk of each platform, beside the
# settings every vendor tool reports
define toolchain.xcode.report =
	@${call log.var,developer,"${if $(toolchain.xcode.developer),$(toolchain.xcode.developer),(from the environment)}"}
	@${call log.var,devicehub,"$${toolchain.xcode.devicehub}"}
	@${foreach platform,$(toolchain.xcode.platforms),${call log.var,$(platform),"$${call toolchain.xcode.sdk.version,$(platform)} $${call toolchain.xcode.sdk,$(platform)}"};}
endef

# beyond the presence of {xcrun}, which every mac has, a build needs each of the tools and the sdk
# of each of the platforms in the selected developer directory. this text is expanded once when the
# recipe is made and again when it runs, so the shell's own variables carry four dollar signs
define toolchain.xcode.checks =
	@for tool in $(toolchain.xcode.tools); do \
	    $(toolchain.xcode.env) $(toolchain.xcode.cli) --find $$$$tool > /dev/null 2>&1 || { \
	        ${call log.error,"the xcode tool '$$$$tool' is not in the active developer directory"} ; \
	        ${call log.info,"the command line tools lack it; xcode has it"} ; \
	        ${call log.info,"name an xcode with: toolchain.xcode.developer := <xcode>/Contents/Developer"} ; \
	        exit 1 ; \
	    } ; \
	done
	@for platform in $(toolchain.xcode.platforms); do \
	    $(toolchain.xcode.env) $(toolchain.xcode.cli) --sdk $$$$platform --show-sdk-path > /dev/null 2>&1 || { \
	        ${call log.error,"the sdk for '$$$$platform' is not in the active developer directory"} ; \
	        ${call log.info,"install the platform from the 'Components' settings of xcode"} ; \
	        exit 1 ; \
	    } ; \
	done
	@${call log.action,"verify","the xcode tools and the sdks of $(toolchain.xcode.platforms) are available"}
endef


# install: mm cannot fetch xcode; send the user to the vendor's download page
xcode.install:
	@${call log.sec,"xcode","xcode is a vendor-distributed tool; mm cannot install it for you"}
	@${call log.info,"download and install it from:"}
	@${call log.info,"    $(toolchain.xcode.url)"}

# update: same story as install; there is nothing for mm to fetch
xcode.update: xcode.install


# end of file
