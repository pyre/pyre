# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the coverage registry summary
coverage.info-target:
	@${call log.sec,"coverage","code coverage reporting for a {cov} build"}
	@${call log.var,"active",${if $(coverage.active),"yes","no -- add 'cov' to the target variants"}}
	@${call log.var,"backend","$(coverage.backend)"}
	@${call log.var,"raw data","$(coverage.raw)"}
	@${call log.var,"report","$(coverage.report)"}
	@${call log.var,"lcov","$(coverage.info)"}
	@${call log.sec,"  actions",}
	@${call log.help,"coverage","merge the collected data and render the report"}
	@${call log.help,"coverage.clean","discard the collected data and the rendered report"}
	@${call log.help,"coverage.info","show these settings"}

# the user facing info alias, matching the {<thing>.info} convention of the other registries
coverage.info: coverage.info-target


# the report generator dispatches on the instrumentation back end; the {coverage} target that ties it
# to the resolved back end is emitted from the model pass, where {coverage.backend} is final. each
# recipe first refuses to run outside a {cov} build, since without the instrumentation there is no
# data to gather and the tools would only emit confusing errors

# the llvm back end: fold the per-run raw profiles into one indexed profile, then read it against the
# instrumented binaries to produce a terminal summary, a browsable html tree, and an lcov file for
# the editor. the shared libraries are discovered under the install tree; a header-only template
# library adds its compiled drivers through {coverage.objects}, since its code lives only there
coverage.llvm:
	@${if $(coverage.active),,${call log.error,"not a coverage build; add cov to the target variants and rerun"}; exit 1}
	@command -v llvm-profdata >/dev/null 2>&1 || { ${call log.error,"'llvm-profdata' not found on the PATH"}; ${call log.info,"it ships with the llvm toolchain; see the coverage notes for the package name"}; exit 1; }
	@${if $(strip $(coverage.raws)),,${call log.error,"no profile data under $(coverage.raw); build and run the tests under the same coverage target first"}; exit 1}
	@${if $(strip $(coverage.binaries)),,${call log.error,"found no instrumented binaries; add compiled drivers or libraries through 'coverage.objects'"}; exit 1}
	@${call log.action,"merge","$(coverage.profdata)"}
	@$(mkdirp) ${dir $(coverage.profdata)}
	@llvm-profdata merge -sparse $(coverage.raws) -o $(coverage.profdata)
	@${call log.action,"report","coverage summary"}
	@llvm-cov report -instr-profile=$(coverage.profdata) $(coverage.objargs)
	@${call log.action,"html","$(coverage.report)"}
	@llvm-cov show -instr-profile=$(coverage.profdata) -format=html -output-dir=$(coverage.report) $(coverage.objargs)
	@${call log.action,"lcov","$(coverage.info)"}
	@llvm-cov export -instr-profile=$(coverage.profdata) -format=lcov $(coverage.objargs) > $(coverage.info)

# the gcov back end: {gcovr} discovers the {.gcno}/{.gcda} pairs and renders both an html tree and an
# lcov file in one pass, keeping the two back ends interchangeable downstream. it searches two roots
# because the coverage data is split: a test driver's data lands next to its in-tree source under the
# project home, while a library object's data lands next to the object in the staging tree
coverage.gcov:
	@${if $(coverage.active),,${call log.error,"not a coverage build; add cov to the target variants and rerun"}; exit 1}
	@command -v gcovr >/dev/null 2>&1 || ( \
	    ${call log.error,"'gcovr' not found on the PATH"}; \
	    ${call log.info,"see the coverage notes for the package name"}; \
	    exit 1 )
	@$(mkdirp) $(coverage.report)
	@${call log.action,"report","coverage summary"}
	@gcovr --root $(project.home) --print-summary \
	    --html-details $(coverage.report)index.html \
	    --lcov $(coverage.info) \
	    $(project.home) $(builder.staging)

# discard the collected data and the rendered report, leaving the instrumented objects in place so a
# fresh measurement run does not force a rebuild
coverage.clean:
	@${call log.action,"rm","$(builder.staging)coverage"}
	@$(rm.force-recurse) $(builder.staging)coverage

# these are phony bookkeeping targets, never files
.PHONY: coverage coverage.llvm coverage.gcov coverage.clean coverage.info coverage.info-target


# end of file
