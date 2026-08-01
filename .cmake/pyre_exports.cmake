# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add {target} to the set of things we hand downstream, under the name {component}
# consumers ask for the optional pieces by name, as in {find_package(pyre COMPONENTS mpi)}, and
# the generated configuration publishes a {pyre_<component>_FOUND} flag for each one that this
# installation actually carries
function(pyre_exportTarget target component)
  # make sure we are still allowed to record
  pyre_exportGate("${target}")
  # remember the target, so the audit knows what to inspect
  set_property(GLOBAL APPEND PROPERTY PYRE_EXPORT_TARGETS "${target}")
  # and the name it goes by
  set_property(GLOBAL APPEND PROPERTY PYRE_EXPORT_COMPONENTS "${component}")
  # all done
endfunction(pyre_exportTarget)


# record an external package that one of our core targets names in its link interface
# {package} is what to look for, {target} is the imported target the search must produce, and
# the remaining arguments are handed to {find_dependency} verbatim
function(pyre_exportRequirement package target)
  # make sure we are still allowed to record
  pyre_exportGate("${package}")
  # flatten the search arguments into a single blank separated string so the entry survives
  # the trip through the property as one piece
  string(REPLACE ";" " " arguments "${ARGN}")
  # and stash it
  set_property(GLOBAL APPEND PROPERTY PYRE_EXPORT_REQUIREMENTS "${package} ${target} ${arguments}")
  # all done
endfunction(pyre_exportRequirement)


# record an external package that only the optional target {component} needs
# the search lands behind a test on the component list, so a consumer that never asks for the
# add-on is never asked to have its dependencies installed; an exported target that nobody links
# costs nothing, since cmake resolves a link interface only when something actually uses it
function(pyre_exportOptionalRequirement component package target)
  # make sure we are still allowed to record
  pyre_exportGate("${package}")
  # flatten the search arguments, as above
  string(REPLACE ";" " " arguments "${ARGN}")
  # and stash the entry, tagged with the component that needs it
  set_property(GLOBAL APPEND PROPERTY
    PYRE_EXPORT_OPTIONAL "${component} ${package} ${target} ${arguments}")
  # all done
endfunction(pyre_exportOptionalRequirement)


# complain if the package configuration has already been rendered; {what} names whatever was
# being recorded, so the diagnostic can point at it
function(pyre_exportGate what)
  # ask
  get_property(sealed GLOBAL PROPERTY PYRE_EXPORT_SEALED)
  # if the file is already written, this record would never reach it
  if(sealed)
    # so complain loudly instead of shipping a package nobody can consume
    message(FATAL_ERROR
      "'${what}' joined the {pyre} exports after the package configuration was rendered; move "
      "the call ahead of {pyre_exportRequirements}")
  endif()
  # all done
endfunction(pyre_exportGate)


# render the code that locates {package} and confirms it produced {target}, into {variable}
function(pyre_exportSearch package target arguments variable)
  # assemble the search, keeping it tidy when the package takes no extra arguments
  set(call "${package}")
  if(arguments)
    string(APPEND call " ${arguments}")
  endif()
  # start with the search itself
  set(text "find_dependency(${call})\n")
  # a successful search is not proof that the imported target exists: a consumer running with
  # {CMAKE_FIND_PACKAGE_PREFER_CONFIG} can resolve the package's own configuration file, which
  # may well publish the target under a different name; catch that here, while we can still
  # say something useful, rather than at the consumer's generate step
  string(APPEND text "if(NOT TARGET ${target})\n")
  string(APPEND text "  set(pyre_FOUND FALSE)\n")
  string(APPEND text "  set(pyre_NOT_FOUND_MESSAGE\n")
  string(APPEND text
    "      \"{pyre} was built against ${package}, but locating it did not define the imported "
    "target '${target}' that the {pyre} targets name; check whether "
    "CMAKE_FIND_PACKAGE_PREFER_CONFIG is steering the search towards a different "
    "${package} package\")\n")
  string(APPEND text "  return()\n")
  string(APPEND text "endif()\n")
  # publish
  set(${variable} "${text}" PARENT_SCOPE)
  # all done
endfunction(pyre_exportSearch)


# verify that every external package our exported targets name has been recorded, render the
# recorded requirements as cmake code, and hand the text back through {variable}
function(pyre_exportRequirements variable)
  # retrieve what the build recorded
  get_property(targets GLOBAL PROPERTY PYRE_EXPORT_TARGETS)
  get_property(components GLOBAL PROPERTY PYRE_EXPORT_COMPONENTS)
  get_property(requirements GLOBAL PROPERTY PYRE_EXPORT_REQUIREMENTS)
  get_property(optional GLOBAL PROPERTY PYRE_EXPORT_OPTIONAL)

  # the imported targets we know how to resolve, the subset of those that every consumer gets
  # unconditionally, and the code that resolves them
  set(known "")
  set(core "")
  set(text "")

  # tell consumers which pieces this installation carries, so that {check_required_components}
  # can answer {find_package(pyre COMPONENTS ...)} correctly
  foreach(component IN LISTS components)
    string(APPEND text "set(pyre_${component}_FOUND TRUE)\n")
  endforeach()

  # the core dependencies, which every consumer of {pyre::pyre} needs
  foreach(requirement IN LISTS requirements)
    # take the entry apart
    string(REPLACE " " ";" fields "${requirement}")
    # the first two fields name the package and the imported target it must produce
    list(POP_FRONT fields package target)
    # and whatever is left is the argument list for the search
    list(JOIN fields " " arguments)
    # remember the target so the audit below can account for it, and note that every consumer
    # gets this one whether they ask for it or not
    list(APPEND known ${target})
    list(APPEND core ${target})
    # render the search and take it as is
    pyre_exportSearch("${package}" "${target}" "${arguments}" search)
    string(APPEND text "${search}")
  endforeach()

  # and the add-on dependencies, each behind a test on what the consumer asked for
  foreach(requirement IN LISTS optional)
    # take the entry apart; this one leads with the component that needs it
    string(REPLACE " " ";" fields "${requirement}")
    list(POP_FRONT fields component package target)
    list(JOIN fields " " arguments)
    # the audit accounts for it just the same
    list(APPEND known ${target})
    # but if every consumer already resolves it, saying so again buys nothing; note that this
    # only skips searches the core covers, so two add-ons that share a package each keep theirs
    if(target IN_LIST core)
      continue()
    endif()
    # render the search
    pyre_exportSearch("${package}" "${target}" "${arguments}" search)
    # drop the trailing newline and indent the body to sit inside the test
    string(REGEX REPLACE "\n$" "" search "${search}")
    string(REPLACE "\n" "\n  " search "${search}")
    # and gate it on the component
    string(APPEND text "if(\"${component}\" IN_LIST pyre_FIND_COMPONENTS)\n  ${search}\nendif()\n")
  endforeach()

  # now audit the exported targets: anything they name that we cannot resolve is a target the
  # consumer will be asked to supply, and the whole point of the exercise is that it shouldn't
  foreach(exported IN LISTS targets)
    # collect the link interface
    get_target_property(interface ${exported} INTERFACE_LINK_LIBRARIES)
    # an empty interface has nothing to answer for
    if(NOT interface)
      continue()
    endif()
    # otherwise, look at each entry
    foreach(dependency IN LISTS interface)
      # a private link on a static library rides along wrapped, and would still have to be
      # resolved by the consumer; unwrap it so it gets the same scrutiny as the rest
      string(REGEX REPLACE "^\\$<LINK_ONLY:(.*)>$" "\\1" dependency "${dependency}")
      # only namespaced imported targets place a burden on the consumer
      if(NOT dependency MATCHES "^([A-Za-z0-9_+.-]+)::")
        continue()
      endif()
      # and our own are resolved by the targets file itself
      if(CMAKE_MATCH_1 STREQUAL "pyre")
        continue()
      endif()
      # everything else must have been recorded at the point of the link
      if(NOT dependency IN_LIST known)
        message(FATAL_ERROR
          "the exported target '${exported}' names the imported target '${dependency}', but "
          "nothing taught the {pyre} package configuration how to find it; add a matching "
          "{pyre_exportRequirement} call next to the {target_link_libraries} that introduced it")
      endif()
    endforeach()
  endforeach()

  # refuse any further recording, so a link established after this point cannot slip past the
  # file we are about to render
  set_property(GLOBAL PROPERTY PYRE_EXPORT_SEALED TRUE)
  # publish the rendered text
  set(${variable} "${text}" PARENT_SCOPE)
  # all done
endfunction(pyre_exportRequirements)


# end of file
